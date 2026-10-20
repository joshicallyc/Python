"""
reader.py: turn the DNA (or RNA) sequences in a FASTA file into proteins.

For every sequence in the file, this program:
  1. glues all of its lines into one long sequence,
  2. turns the DNA into mRNA (T becomes U),
  3. finds the open reading frames (ORFs): stretches that start with a start
     codon (AUG) and end at a stop codon, in all three reading frames
     (six with --both-strands),
  4. translates them into proteins,
and saves everything as an HTML page you can open in any web browser.

Examples (run these in a terminal, inside the CLI_project folder):
    python3 reader.py -f fasta.txt
    python3 reader.py -f fasta.txt -o my_proteins.html
    python3 reader.py -f fasta.txt --fasta proteins.fasta
    python3 reader.py -f humandna.fasta.html --min-length 100

How to read this file: main() at the bottom runs everything, in this order:
    read_fasta()  ->  analyze() for each record  ->  build_page()  ->  save the page
Everything above main() is a helper that one of those steps uses.

Works best with mRNA or cDNA records (for example RefSeq "NM_" sequences).
In genomic DNA, genes are interrupted by introns, which this program can't cut
out, so a protein found there is often only part of the real one.
"""

import argparse
import html
import sys
from pathlib import Path   # Path: a file path that knows its own name, folder and extension


# ---------------------------------------------------------------------------
# 1. The genetic code
# ---------------------------------------------------------------------------
# Same idea as the amino_acid_groups dictionary you wrote: each amino acid
# (one-letter code) and the mRNA codons that code for it. "*" means "stop".
CODONS_FOR = {
    "A": ("GCU", "GCC", "GCA", "GCG"),                 # Alanine
    "R": ("CGU", "CGC", "CGA", "CGG", "AGA", "AGG"),   # Arginine
    "N": ("AAU", "AAC"),                               # Asparagine
    "D": ("GAU", "GAC"),                               # Aspartic acid
    "C": ("UGU", "UGC"),                               # Cysteine
    "Q": ("CAA", "CAG"),                               # Glutamine
    "E": ("GAA", "GAG"),                               # Glutamic acid
    "G": ("GGU", "GGC", "GGA", "GGG"),                 # Glycine
    "H": ("CAU", "CAC"),                               # Histidine
    "I": ("AUU", "AUC", "AUA"),                        # Isoleucine
    "L": ("UUA", "UUG", "CUU", "CUC", "CUA", "CUG"),   # Leucine
    "K": ("AAA", "AAG"),                               # Lysine
    "M": ("AUG",),                                     # Methionine (also the start codon)
    "F": ("UUU", "UUC"),                               # Phenylalanine
    "P": ("CCU", "CCC", "CCA", "CCG"),                 # Proline
    "S": ("UCU", "UCC", "UCA", "UCG", "AGU", "AGC"),   # Serine
    "T": ("ACU", "ACC", "ACA", "ACG"),                 # Threonine
    "W": ("UGG",),                                     # Tryptophan
    "Y": ("UAU", "UAC"),                               # Tyrosine
    "V": ("GUU", "GUC", "GUA", "GUG"),                 # Valine
    "*": ("UAA", "UAG", "UGA"),                        # Stop
}

# Flip the dictionary around ONCE, at the start, so any codon can be looked up
# directly: CODON_TABLE["AUG"] gives "M". (Your version rebuilt this table for
# every codon; building it once gives the same result, much faster.)
CODON_TABLE = {}
for amino_acid, codons in CODONS_FOR.items():
    for codon in codons:
        CODON_TABLE[codon] = amino_acid

# Sequencing files sometimes use letters that mean "one of several bases"
# (IUPAC codes). Each one, and the bases it could be. N means "any base".
AMBIGUOUS_BASES = {
    "R": "AG", "Y": "CU", "S": "CG", "W": "AU", "K": "GU", "M": "AC",
    "B": "CGU", "D": "AGU", "H": "ACU", "V": "ACG", "N": "ACGU",
}

# Each base and the base it pairs with on the opposite strand
# (the ambiguous letters pair up too: R = A or G pairs with Y = U or C).
PAIRS = {
    "A": "U", "U": "A", "G": "C", "C": "G",
    "R": "Y", "Y": "R", "S": "S", "W": "W", "K": "M", "M": "K",
    "B": "V", "V": "B", "D": "H", "H": "D", "N": "N",
}

AMINO_ACID_NAMES = {
    "A": "Alanine", "R": "Arginine", "N": "Asparagine", "D": "Aspartic acid",
    "C": "Cysteine", "Q": "Glutamine", "E": "Glutamic acid", "G": "Glycine",
    "H": "Histidine", "I": "Isoleucine", "L": "Leucine", "K": "Lysine",
    "M": "Methionine", "F": "Phenylalanine", "P": "Proline", "S": "Serine",
    "T": "Threonine", "W": "Tryptophan", "Y": "Tyrosine", "V": "Valine",
    "X": "Unknown (an ambiguous codon)",
}

# Average mass of each amino acid once it's inside a protein, in daltons
# (values from ExPASy). A protein's mass = the sum of these + one water.
RESIDUE_MASS = {
    "A": 71.0788, "R": 156.1875, "N": 114.1038, "D": 115.0886, "C": 103.1388,
    "E": 129.1155, "Q": 128.1307, "G": 57.0519, "H": 137.1411, "I": 113.1594,
    "L": 113.1594, "K": 128.1741, "M": 131.1926, "F": 147.1766, "P": 97.1167,
    "S": 87.0782, "T": 101.1051, "W": 186.2132, "Y": 163.1760, "V": 99.1326,
    "X": 110.0,  # unknown amino acid: use a typical average
}
WATER_MASS = 18.0153


# ---------------------------------------------------------------------------
# 2. Reading the FASTA file
# ---------------------------------------------------------------------------
def guess_encoding(path):
    """Most files are UTF-8. Some Windows tools save UTF-16 instead, which
    starts with two special bytes, so check for those first."""
    with open(path, "rb") as f:          # "rb" = read the raw bytes
        first_two_bytes = f.read(2)
    if first_two_bytes == b"\xff\xfe" or first_two_bytes == b"\xfe\xff":
        return "utf-16"
    return "utf-8-sig"                   # UTF-8, skipping an invisible "BOM" marker at the start if there is one


def keep_letters(text):
    """Return only the plain A-Z letters in `text`, uppercased (drops spaces and numbers)."""
    letters = ""
    for character in text:
        if "a" <= character <= "z" or "A" <= character <= "Z":
            letters += character.upper()
    return letters


def save_record(records, header, sequence):
    """Add one (header, sequence) pair to the list, giving it a name if it has none."""
    if header is None or header == "":
        header = "(no name)"
    records.append((header, sequence))


def read_fasta(path):
    """Read a FASTA file and return a list of (header, sequence) pairs.

    Every line starting with ">" begins a new record. All the lines after a
    header are glued into ONE string, so a codon that crosses a line break
    stays whole. Blank lines and old-style ";" comment lines are skipped.
    """
    records = []
    header = None        # the current record's name (None = no header seen yet)
    sequence = ""        # the current record's sequence, built up line by line
    started = False      # have we seen anything for the current record yet?

    # errors="replace": a character that can't be read becomes a "?" instead of crashing
    with open(path, encoding=guess_encoding(path), errors="replace") as f:
        for line in f:
            line = line.strip()
            if line == "" or line.startswith(";"):
                continue
            if line.startswith(">"):
                # A new header: first save the record we were building, if any.
                if started:
                    save_record(records, header, sequence)
                header = line[1:].strip()
                sequence = ""
                started = True
            else:
                sequence += keep_letters(line)
                started = True

    # Save the last record (there's no next ">" line to trigger it).
    if started:
        save_record(records, header, sequence)
    return records


# ---------------------------------------------------------------------------
# 3. From DNA to mRNA to protein
# ---------------------------------------------------------------------------
def to_rna(dna):
    """Turn a DNA sequence from a FASTA file into mRNA.

    For mRNA and cDNA records, GenBank's FASTA is the coding (sense) strand,
    written with T. The mRNA is the SAME sequence with U instead of T, so no
    base pairing is needed. (In genomic DNA a gene can be on the other strand;
    that's what --both-strands is for.) Ambiguous IUPAC letters (R, Y, N, ...)
    are kept; any other letter becomes N.
    """
    rna = ""
    for base in dna:
        if base == "T":
            rna += "U"
        elif base in "ACGU" or base in AMBIGUOUS_BASES:
            rna += base
        else:
            rna += "N"
    return rna


def reverse_complement(rna):
    """The opposite strand, read in its own 5' -> 3' direction."""
    result = ""
    for base in reversed(rna):
        result += PAIRS[base]
    return result


def translate_codon(codon):
    """One codon -> one amino acid letter ("*" = stop, "X" = can't tell).

    A codon with an ambiguous letter, like "UAR" (R = A or G), is translated
    only if every possible reading gives the same answer. UAA and UAG are
    both stops, so "UAR" is a stop; "GGN" is always glycine (G).
    """
    if codon in CODON_TABLE:
        return CODON_TABLE[codon]

    answers = []
    # AMBIGUOUS_BASES.get(base, base): the bases a letter could be (a plain
    # A, C, G or U isn't in the dictionary, so it just stands for itself).
    for first in AMBIGUOUS_BASES.get(codon[0], codon[0]):
        for second in AMBIGUOUS_BASES.get(codon[1], codon[1]):
            for third in AMBIGUOUS_BASES.get(codon[2], codon[2]):
                answer = CODON_TABLE[first + second + third]
                if answer not in answers:
                    answers.append(answer)
    if len(answers) == 1:
        return answers[0]
    return "X"


def translate_from(rna, start):
    """Translate codon by codon, beginning at index `start`, until a stop codon.

    Returns (protein, found_stop). found_stop is False if the sequence ran
    out before a stop codon.
    """
    protein = ""
    for i in range(start, len(rna) - 2, 3):      # stop while a full codon is still left
        amino_acid = translate_codon(rna[i:i + 3])
        if amino_acid == "*":
            return protein, True
        protein += amino_acid
    return protein, False


def find_orfs(rna, strand, min_length):
    """Find the open reading frames (AUG ... stop) in all three reading frames.

    strand is "+" for the sequence as given, or "-" for its reverse
    complement (then the frame counts from the start of the reverse
    complement). Returns a list of dictionaries, one per ORF with at least
    `min_length` amino acids. Positions are 1-based, like in GenBank, and
    always refer to the original (+) sequence.
    """
    orfs = []
    for frame in range(3):                 # reading frames start at index 0, 1 or 2
        i = frame
        while i <= len(rna) - 3:           # while a full codon is still left
            if rna[i:i + 3] != "AUG":
                i += 3                     # not a start codon: move to the next codon
            else:
                protein, found_stop = translate_from(rna, i)
                codons_used = len(protein)
                if found_stop:
                    codons_used += 1       # the stop codon counts too

                start = i + 1              # 1-based position of the first base
                end = i + 3 * codons_used  # 1-based position of the last base
                if strand == "-":
                    # Convert to + strand positions. Use new names so we don't
                    # overwrite `start` before we've used it to work out `end`.
                    plus_start = len(rna) - end + 1
                    plus_end = len(rna) - start + 1
                    start = plus_start
                    end = plus_end

                if len(protein) >= min_length:
                    orfs.append({
                        "strand": strand,
                        "frame": frame + 1,
                        "start": start,
                        "end": end,
                        "protein": protein,
                        "complete": found_stop,
                    })

                # Jump past this ORF, so an AUG inside it (a methionine in the
                # middle of the protein) isn't reported as a separate, shorter protein.
                i += 3 * codons_used
    return orfs


def protein_length(orf):
    """Sort key: the number of amino acids in an ORF's protein."""
    return len(orf["protein"])


def pick_main(orfs):
    """Choose the protein to show first. `orfs` must be sorted longest first.

    Forward-strand ORFs win if there are any: for mRNA, the forward strand is
    the real one. Among those, the longest ORF that ends at a stop codon; if
    none ends at a stop codon, the longest one. None if there are no ORFs.
    """
    candidates = []
    for orf in orfs:
        if orf["strand"] == "+":
            candidates.append(orf)
    if len(candidates) == 0:
        candidates = orfs

    for orf in candidates:
        if orf["complete"]:
            return orf               # the list is longest first, so this is the longest complete one
    if len(candidates) > 0:
        return candidates[0]         # nothing reaches a stop codon: take the longest anyway
    return None


def molecular_weight(protein):
    """Approximate mass of a protein in daltons."""
    total = WATER_MASS
    for amino_acid in protein:
        total += RESIDUE_MASS[amino_acid]
    return total


def analyze(header, dna, min_length, both_strands):
    """Everything we want to know about one FASTA record, in a dictionary."""
    rna = to_rna(dna)
    orfs = find_orfs(rna, "+", min_length)
    if both_strands:
        orfs += find_orfs(reverse_complement(rna), "-", min_length)
    orfs.sort(key=protein_length, reverse=True)        # longest first

    known_bases = rna.count("A") + rna.count("C") + rna.count("G") + rna.count("U")
    gc = None                                          # None = can't tell (no known bases)
    if known_bases > 0:
        gc = (rna.count("G") + rna.count("C")) / known_bases

    return {
        "header": header,
        "length": len(rna),
        "known_bases": known_bases,
        "gc": gc,
        "orfs": orfs,
        "main": pick_main(orfs),
    }


# ---------------------------------------------------------------------------
# 4. Writing the results
# ---------------------------------------------------------------------------
def with_commas(number):
    """1234567 -> "1,234,567". (The ":," inside the braces is what adds the commas.)"""
    return f"{number:,}"


def plural(count, word):
    """plural(1, "sequence") -> "1 sequence";  plural(3, "sequence") -> "3 sequences"."""
    if count == 1:
        return with_commas(count) + " " + word
    return with_commas(count) + " " + word + "s"


def short(text, limit):
    """Cut `text` to at most `limit` characters, adding "…" if it was cut."""
    if len(text) <= limit:
        return text
    return text[:limit - 1] + "…"


def format_protein(protein):
    """Lay out a protein like a GenBank record: 60 letters per line in blocks
    of 10, each line starting with the position of its first letter."""
    lines = []
    for i in range(0, len(protein), 60):
        line = protein[i:i + 60]
        blocks = []
        for j in range(0, len(line), 10):
            blocks.append(line[j:j + 10])
        # rjust(5): pad the number on the left to 5 characters so the columns line up
        lines.append(str(i + 1).rjust(5) + "  " + " ".join(blocks))
    return "\n".join(lines)


def describe_location(orf):
    """A short HTML description like 'bases 11–547 · forward (+) strand, frame 2'."""
    if orf["strand"] == "+":
        strand = "forward (+) strand"
    else:
        strand = "opposite (−) strand"
    bases = with_commas(orf["start"]) + "–" + with_commas(orf["end"])
    return '<span class="nowrap">bases ' + bases + "</span> · " + strand + ", frame " + str(orf["frame"])


def orf_table(result, min_length):
    """The collapsible table that lists every ORF in a record."""
    rows = []
    number = 1
    for orf in result["orfs"]:
        protein = orf["protein"]
        if orf["complete"]:
            stop_text = "yes"
            row_start = "<tr>"
        else:
            stop_text = "no"
            row_start = '<tr class="incomplete">'
        if orf["strand"] == "+":
            strand = "+"
        else:
            strand = "−"
        rows.append(
            row_start
            + "<td>" + str(number) + "</td>"
            + "<td>" + with_commas(len(protein)) + "</td>"
            + "<td>" + strand + "</td>"
            + "<td>" + str(orf["frame"]) + "</td>"
            + "<td>" + with_commas(orf["start"]) + "–" + with_commas(orf["end"]) + "</td>"
            + "<td>" + stop_text + "</td>"
            + '<td class="seq">' + short(protein, 30) + "</td>"
            + "</tr>"
        )
        number += 1

    return (
        "<details>\n"
        + "<summary>All " + plural(len(result["orfs"]), "open reading frame")
        + " of at least " + plural(min_length, "amino acid") + "</summary>\n"
        + '<p class="facts">Longest first. Grey rows have no stop codon before the sequence ends.</p>\n'
        + '<div class="table-wrap"><table>\n'
        + "<tr><th>#</th><th>Amino acids</th><th>Strand</th><th>Frame</th>"
        + "<th>Bases</th><th>Stop codon?</th><th>Start of protein</th></tr>\n"
        + "\n".join(rows)
        + "\n</table></div>\n</details>"
    )


def record_html(result, min_length, both_strands):
    """The HTML section for one FASTA record."""
    # Split the header into its first word (usually the ID) and the rest.
    words = result["header"].split(" ", 1)
    record_id = words[0]
    description = ""
    if len(words) > 1:
        description = words[1]

    parts = ['<section class="record">', "<h2>" + html.escape(record_id) + "</h2>"]
    if description != "":
        safe_description = html.escape(description)
        parts.append('<p class="desc" title="' + safe_description + '">' + safe_description + "</p>")

    # The basic facts about the sequence.
    if result["gc"] is None:
        gc_text = "GC content n/a"
    else:
        gc_text = "GC content " + str(round(result["gc"] * 100, 1)) + "%"
    facts = plural(result["length"], "base") + " · " + gc_text
    other_letters = result["length"] - result["known_bases"]
    if other_letters > 0:
        facts += " · " + with_commas(other_letters) + " unknown or ambiguous (N, R, Y…)"
    parts.append('<p class="facts">' + facts + "</p>")

    # The main protein (or why there isn't one).
    main = result["main"]
    if result["length"] == 0:
        parts.append('<p class="empty">This record has no sequence.</p>')
    elif result["known_bases"] < result["length"] / 2:
        parts.append('<p class="empty">This doesn\'t look like DNA or RNA: most of its letters '
                     "aren't A, C, G, T or U. Is it a protein FASTA file?</p>")
    elif main is None:
        hint = "Try a smaller <code>--min-length</code>"
        if not both_strands:
            hint += ", or add <code>--both-strands</code> if this is genomic DNA"
        parts.append('<p class="empty">No protein of at least ' + plural(min_length, "amino acid")
                     + " was found. " + hint + ".</p>")

    if main is not None:
        protein = main["protein"]
        if main["strand"] == "-":
            title = "Longest open reading frame (opposite strand)"
        elif main["complete"]:
            title = "Main protein"
        else:
            title = "Main protein (incomplete)"
        if main["complete"]:
            ending = "ends at a stop codon"
        else:
            ending = "no stop codon before the sequence ends"
        kda = round(molecular_weight(protein) / 1000, 1)
        parts.append(
            '<div class="protein">\n<h3>' + title + "</h3>\n"
            + '<p class="facts">' + plural(len(protein), "amino acid") + " · " + str(kda) + " kDa · "
            + describe_location(main) + " · " + ending + "</p>\n"
            + "<pre>" + format_protein(protein) + "</pre>\n</div>"
        )

    if len(result["orfs"]) > 1:
        parts.append(orf_table(result, min_length))

    parts.append("</section>")
    return "\n".join(parts)


# The page's look (CSS), kept in its own variable so build_page() stays readable.
PAGE_STYLE = """
:root {
  color-scheme: light dark;
  --bg: #fcfcfb; --card: #ffffff; --text: #1f1f1d; --muted: #5f5e5a;
  --border: #e3e2de; --accent: #1d65c1; --code-bg: #f4f3f0;
}
@media (prefers-color-scheme: dark) {
  :root {
    color-scheme: dark;
    --bg: #1a1a19; --card: #222220; --text: #f0efec; --muted: #b3b2aa;
    --border: #3a3936; --accent: #62a0ef; --code-bg: #2a2a28;
  }
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--text);
       font-family: system-ui, -apple-system, "Segoe UI", sans-serif; line-height: 1.5; }
main { max-width: 960px; margin: 0 auto; padding: 24px 16px 48px; }
h1 { margin: 0 0 4px; font-size: 1.6rem; overflow-wrap: anywhere; }
h2 { margin: 0 0 2px; font-size: 1.2rem; overflow-wrap: anywhere; }
h3 { margin: 0 0 4px; font-size: 1rem; color: var(--accent); }
.desc { margin: 0 0 6px; color: var(--muted); overflow: hidden; display: -webkit-box;
        -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow-wrap: anywhere; }
.facts { margin: 0 0 12px; color: var(--muted); font-size: 0.92rem; }
.nowrap { white-space: nowrap; }
.record { background: var(--card); border: 1px solid var(--border); border-radius: 10px;
          padding: 16px; margin: 16px 0; }
.protein { border-left: 3px solid var(--accent); padding-left: 12px; margin: 12px 0; }
pre { background: var(--code-bg); border-radius: 6px; padding: 12px; margin: 0;
      overflow-x: auto; font-size: 0.9rem; line-height: 1.6; }
@media (max-width: 600px) { pre { white-space: pre-wrap; } }
code, pre, .seq { font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace; }
details { margin-top: 12px; }
summary { cursor: pointer; color: var(--accent); }
.table-wrap { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; margin-top: 8px; font-size: 0.88rem; }
th, td { border-bottom: 1px solid var(--border); padding: 6px 8px; text-align: left; white-space: nowrap; }
th { color: var(--muted); font-weight: 600; }
tr.incomplete td { color: var(--muted); }
.empty { color: var(--muted); }
.legend { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 2px 16px;
          margin-top: 8px; font-size: 0.9rem; }
.legend code { font-weight: 700; color: var(--accent); }
footer { color: var(--muted); font-size: 0.85rem; margin-top: 24px; }
"""


def build_page(results, input_name, min_length, both_strands):
    """Put the whole HTML page together."""
    found = 0
    for result in results:
        if result["main"] is not None:
            found += 1

    if both_strands:
        searched = "both strands"
    else:
        searched = "the forward strand"

    sections = ""
    for result in results:
        sections += record_html(result, min_length, both_strands) + "\n"

    legend = ""
    for letter, name in AMINO_ACID_NAMES.items():
        legend += "<div><code>" + letter + "</code> " + html.escape(name) + "</div>\n"

    safe_name = html.escape(input_name)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Proteins from {safe_name}</title>
<style>{PAGE_STYLE}</style>
</head>
<body>
<main>
<h1>Proteins from {safe_name}</h1>
<p class="facts">{plural(len(results), "sequence")} read · proteins found in {found} of them ·
searched {searched} for open reading frames of at least {plural(min_length, "amino acid")}</p>
{sections}
<details>
<summary>What do the letters mean?</summary>
<div class="legend">
{legend}
</div>
</details>
<footer>
<p>An <strong>open reading frame (ORF)</strong> runs from a start codon (AUG) to the next stop
codon (UAA, UAG or UGA) in the same reading frame. The main protein is the longest ORF that ends at
a stop codon; if none does, it's the longest ORF found, marked "incomplete". Forward-strand ORFs are
preferred, because mRNA records are written in the forward direction.</p>
<p>In genomic DNA, genes are interrupted by introns that this program can't cut out, so a protein
found there may be only part of the real one. For the real protein, use an mRNA record
(for example a RefSeq "NM_" sequence).</p>
<p>Made with reader.py, using the standard genetic code.</p>
</footer>
</main>
</body>
</html>
"""


def write_protein_fasta(results, path):
    """Save each record's main protein in FASTA format (60 letters per line)."""
    with open(path, "w", encoding="utf-8") as f:
        for result in results:
            main = result["main"]
            if main is None:
                continue
            note = ""
            if not main["complete"]:
                note = ", partial (no stop codon)"
            f.write(">" + result["header"] + " | protein, " + str(len(main["protein"])) + " aa, "
                    + main["strand"] + " strand bases " + str(main["start"]) + "-" + str(main["end"])
                    + note + "\n")
            for i in range(0, len(main["protein"]), 60):
                f.write(main["protein"][i:i + 60] + "\n")


# ---------------------------------------------------------------------------
# 5. The command-line program
# ---------------------------------------------------------------------------
def check_output_path(path, input_path):
    """Stop with a clear message if we can't (or shouldn't) write to `path`.
    (sys.exit stops the program and prints the message.)"""
    if path.is_dir():
        sys.exit(f"Error: '{path}' is a folder. Give a file name instead.")
    if not path.parent.is_dir():
        sys.exit(f"Error: can't save to '{path}': the folder '{path.parent}' doesn't exist.")
    if path.resolve() == input_path.resolve():
        sys.exit(f"Error: '{path}' is your input file. Pick a different output name so it isn't overwritten.")


def main():
    # Print special characters safely, even in a terminal that can't show them.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")

    parser = argparse.ArgumentParser(
        description="Translate the sequences in a FASTA file into proteins and save them as a web page."
    )
    parser.add_argument("-f", "--file", required=True, help="input FASTA file")
    parser.add_argument("-o", "--output",
                        help="HTML page to write (default: the input's name without its last extension, "
                             "plus _proteins.html, in the input's folder)")
    parser.add_argument("--min-length", type=int, default=50,
                        help="shortest protein to report, in amino acids (default: 50)")
    parser.add_argument("--both-strands", action="store_true",
                        help="also search the opposite strand (only useful for genomic DNA; "
                             "ORFs found there may be noise, so check the table)")
    parser.add_argument("--fasta", help="also save the main proteins to this FASTA file")
    args = parser.parse_args()

    # Check everything BEFORE doing any work, so a mistake never leaves half-written files.
    input_path = Path(args.file)
    if not input_path.is_file():
        sys.exit(f"Error: can't find the file '{input_path}'.")
    if args.min_length < 1:
        sys.exit("Error: --min-length must be at least 1.")

    if args.output:
        output_path = Path(args.output)
    else:
        # .stem is the file name without its last extension: fasta.txt -> fasta
        output_path = input_path.with_name(input_path.stem + "_proteins.html")
    check_output_path(output_path, input_path)
    if args.fasta:
        fasta_path = Path(args.fasta)
        check_output_path(fasta_path, input_path)
        if fasta_path.resolve() == output_path.resolve():
            sys.exit("Error: --fasta and the HTML page can't be the same file.")

    records = read_fasta(input_path)
    if len(records) == 0:
        sys.exit(f"Error: no sequences found in '{input_path}'. Is it a FASTA file?")

    results = []
    for header, dna in records:
        results.append(analyze(header, dna, args.min_length, args.both_strands))

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(build_page(results, input_path.name, args.min_length, args.both_strands))
        if args.fasta:
            write_protein_fasta(results, args.fasta)
    except OSError as error:
        sys.exit(f"Error: couldn't save the results: {error}")

    # A short summary in the terminal, too.
    print(f"Read {plural(len(results), 'sequence')} from {input_path.name}")
    for result in results:
        name = short(result["header"], 40)
        main_orf = result["main"]
        if result["length"] > 0 and result["known_bases"] < result["length"] / 2:
            print(f"  {name}: warning, this doesn't look like DNA or RNA")
        elif main_orf is None:
            print(f"  {name}: no protein of at least {plural(args.min_length, 'amino acid')}")
        else:
            protein = main_orf["protein"]
            print(f"  {name}: {plural(len(protein), 'amino acid')}, starting {short(protein, 16)}")
    print(f"Saved the page: {output_path}  (open it in your web browser)")
    if args.fasta:
        print(f"Saved the proteins as FASTA: {args.fasta}")


# Run main() only when this file is run directly (not when another program imports it).
if __name__ == "__main__":
    main()
