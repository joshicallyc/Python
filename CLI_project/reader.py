"""
reader.py: turn the DNA (or RNA) sequences in a FASTA file into proteins.

For every sequence in the file, this program:
  1. glues all of its lines into one long sequence,
  2. turns the DNA into mRNA (T becomes U),
  3. finds the open reading frames (ORFs): stretches that start with a start
     codon (AUG) and end with a stop codon, in all three reading frames,
  4. translates them into proteins,
and saves everything as an HTML page you can open in any web browser.

Examples (run these in a terminal, inside the CLI_project folder):
    python3 reader.py -f fasta.txt
    python3 reader.py -f fasta.txt -o my_proteins.html
    python3 reader.py -f humandna.fasta.html --both-strands --min-length 100
    python3 reader.py -f fasta.txt --fasta proteins.fasta
"""

import argparse
import html
import sys
from pathlib import Path


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
# every codon; building it once is the same result, much faster.)
CODON_TABLE = {}
for amino_acid, codons in CODONS_FOR.items():
    for codon in codons:
        CODON_TABLE[codon] = amino_acid

AMINO_ACID_NAMES = {
    "A": "Alanine", "R": "Arginine", "N": "Asparagine", "D": "Aspartic acid",
    "C": "Cysteine", "Q": "Glutamine", "E": "Glutamic acid", "G": "Glycine",
    "H": "Histidine", "I": "Isoleucine", "L": "Leucine", "K": "Lysine",
    "M": "Methionine", "F": "Phenylalanine", "P": "Proline", "S": "Serine",
    "T": "Threonine", "W": "Tryptophan", "Y": "Tyrosine", "V": "Valine",
    "X": "Unknown (the codon contains an unknown base, N)",
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
def keep_letters(text):
    """Return only the letters in `text`, uppercased (drops spaces and numbers)."""
    letters = ""
    for character in text.upper():
        if character.isalpha():
            letters += character
    return letters


def read_fasta(path):
    """Read a FASTA file and return a list of (header, sequence) pairs.

    Every line starting with ">" begins a new record. All the lines after a
    header are glued into ONE string, so a codon that crosses a line break
    stays whole. Blank lines are skipped.
    """
    records = []
    header = None      # the current record's name (None = no header seen yet)
    pieces = []        # the current record's sequence lines

    with open(path, encoding="utf-8", errors="replace") as f:   # "with" closes the file for us
        for line in f:
            line = line.strip()
            if line == "":
                continue
            if line.startswith(">"):
                # A new header: first save the record we were building, if any.
                if header is not None or pieces:
                    records.append((header or "(no name)", "".join(pieces)))
                header = line[1:].strip()
                pieces = []
            else:
                pieces.append(keep_letters(line))

    # Save the last record (there's no next ">" line to trigger it).
    if header is not None or pieces:
        records.append((header or "(no name)", "".join(pieces)))
    return records


# ---------------------------------------------------------------------------
# 3. From DNA to mRNA to protein
# ---------------------------------------------------------------------------
def to_rna(dna):
    """Turn the coding-strand DNA from a FASTA file into mRNA.

    GenBank FASTA files store the coding (sense) strand, written with T.
    The mRNA has the SAME sequence with U instead of T, so no base pairing
    is needed. Anything that isn't A, C, G or U (for example N, "unknown
    base") becomes N.
    """
    rna = ""
    for base in dna.replace("T", "U"):
        if base in "ACGU":
            rna += base
        else:
            rna += "N"
    return rna


def reverse_complement(rna):
    """The opposite strand, read in its own 5' -> 3' direction."""
    pairs = {"A": "U", "U": "A", "G": "C", "C": "G", "N": "N"}
    result = ""
    for base in reversed(rna):
        result += pairs[base]
    return result


def translate_from(rna, start):
    """Translate codon by codon, beginning at index `start`, until a stop codon.

    Returns (protein, found_stop). found_stop is False if the sequence ran
    out before a stop codon. Codons with an unknown base (N) become "X".
    """
    protein = ""
    for i in range(start, len(rna) - 2, 3):
        codon = rna[i:i + 3]
        amino_acid = CODON_TABLE.get(codon, "X")
        if amino_acid == "*":
            return protein, True
        protein += amino_acid
    return protein, False


def find_orfs(rna, strand, min_length):
    """Find the open reading frames (AUG ... stop) in all three reading frames.

    strand is "+" for the sequence as given, or "-" for its reverse complement.
    Returns a list of dictionaries, one per ORF that has at least
    `min_length` amino acids. Positions are 1-based, like in GenBank, and
    always refer to the original (+) sequence.
    """
    orfs = []
    for frame in range(3):                 # reading frames start at index 0, 1 or 2
        i = frame
        while i <= len(rna) - 3:
            if rna[i:i + 3] != "AUG":
                i += 3                     # not a start codon: move to the next codon
                continue

            protein, found_stop = translate_from(rna, i)
            codons_used = len(protein) + (1 if found_stop else 0)   # the stop codon counts too
            start, end = i + 1, i + 3 * codons_used                 # 1-based, inclusive
            if strand == "-":
                # Convert positions on the reverse strand back to the + strand.
                start, end = len(rna) - end + 1, len(rna) - start + 1

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


def orf_rank(orf):
    """Sort key: complete ORFs (with a stop codon) first, then the longest."""
    return (orf["complete"], len(orf["protein"]))


def molecular_weight(protein):
    """Approximate mass of a protein in daltons."""
    total = WATER_MASS
    for amino_acid in protein:
        total += RESIDUE_MASS[amino_acid]
    return total


def gc_content(rna):
    """Fraction of known bases that are G or C (0.0 to 1.0)."""
    known = rna.count("A") + rna.count("C") + rna.count("G") + rna.count("U")
    if known == 0:
        return 0.0
    return (rna.count("G") + rna.count("C")) / known


def analyze(header, dna, min_length, both_strands):
    """Everything we want to know about one FASTA record, in a dictionary."""
    rna = to_rna(dna)
    orfs = find_orfs(rna, "+", min_length)
    if both_strands:
        orfs += find_orfs(reverse_complement(rna), "-", min_length)
    orfs.sort(key=orf_rank, reverse=True)

    return {
        "header": header,
        "length": len(rna),
        "unknown_bases": rna.count("N"),
        "gc": gc_content(rna),
        "orfs": orfs,
        # The main protein: the longest complete ORF (or None if there isn't one).
        "main": orfs[0] if orfs else None,
    }


# ---------------------------------------------------------------------------
# 4. Writing the results
# ---------------------------------------------------------------------------
def format_protein(protein, per_line=60, block=10):
    """Lay out a protein like UniProt does: blocks of 10, 60 per line, numbered."""
    lines = []
    for i in range(0, len(protein), per_line):
        line = protein[i:i + per_line]
        blocks = []
        for j in range(0, len(line), block):
            blocks.append(line[j:j + block])
        lines.append(f"{i + 1:>5}  " + " ".join(blocks))
    return "\n".join(lines)


def describe_location(orf):
    """A short description like 'bases 11–547, + strand, frame 2'."""
    strand = "forward (+) strand" if orf["strand"] == "+" else "reverse (−) strand"
    return f"bases {orf['start']:,}–{orf['end']:,} · {strand}, frame {orf['frame']}"


def record_html(result, min_length):
    """The HTML section for one FASTA record."""
    parts = [f'<section class="record">\n<h2>{html.escape(result["header"])}</h2>']

    facts = f'{result["length"]:,} bases · GC content {result["gc"]:.1%}'
    if result["unknown_bases"]:
        facts += f' · {result["unknown_bases"]:,} unknown bases (N)'
    parts.append(f'<p class="facts">{facts}</p>')

    main = result["main"]
    if main is None:
        parts.append(
            f'<p class="empty">No protein of at least {min_length} amino acids was found. '
            "Try a smaller <code>--min-length</code>, or add <code>--both-strands</code> "
            "if this is genomic DNA.</p>"
        )
    else:
        protein = main["protein"]
        ending = "ends at a stop codon" if main["complete"] else "no stop codon before the sequence ends"
        parts.append(
            '<div class="protein">\n<h3>Main protein</h3>\n'
            f'<p class="facts">{len(protein):,} amino acids · {molecular_weight(protein) / 1000:.1f} kDa · '
            f'{describe_location(main)} · {ending}</p>\n'
            f'<pre>{format_protein(protein)}</pre>\n</div>'
        )

    if len(result["orfs"]) > 1:
        rows = []
        for number, orf in enumerate(result["orfs"], start=1):
            rows.append(
                f'<tr><td>{number}</td><td>{len(orf["protein"]):,}</td>'
                f'<td>{orf["strand"]}</td><td>{orf["frame"]}</td>'
                f'<td>{orf["start"]:,}–{orf["end"]:,}</td>'
                f'<td>{"yes" if orf["complete"] else "no"}</td>'
                f'<td class="seq">{orf["protein"][:30]}{"…" if len(orf["protein"]) > 30 else ""}</td></tr>'
            )
        parts.append(
            f'<details>\n<summary>All {len(result["orfs"])} open reading frames of at least '
            f"{min_length} amino acids</summary>\n<div class=\"table-wrap\"><table>\n"
            "<tr><th>#</th><th>Amino acids</th><th>Strand</th><th>Frame</th>"
            "<th>Bases</th><th>Stop codon?</th><th>Start of protein</th></tr>\n"
            + "\n".join(rows) + "\n</table></div>\n</details>"
        )

    parts.append("</section>")
    return "\n".join(parts)


PAGE_STYLE = """
:root {
  --bg: #fcfcfb; --card: #ffffff; --text: #1f1f1d; --muted: #5f5e5a;
  --border: #e3e2de; --accent: #2a78d6; --code-bg: #f4f3f0;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #1a1a19; --card: #222220; --text: #f0efec; --muted: #b3b2aa;
    --border: #3a3936; --accent: #3987e5; --code-bg: #2a2a28;
  }
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--text);
       font-family: system-ui, -apple-system, "Segoe UI", sans-serif; line-height: 1.5; }
main { max-width: 960px; margin: 0 auto; padding: 24px 16px 48px; }
h1 { margin: 0 0 4px; font-size: 1.6rem; }
h2 { margin: 0 0 4px; font-size: 1.2rem; overflow-wrap: anywhere; }
h3 { margin: 0 0 4px; font-size: 1rem; color: var(--accent); }
.facts { margin: 0 0 12px; color: var(--muted); font-size: 0.92rem; }
.record { background: var(--card); border: 1px solid var(--border); border-radius: 10px;
          padding: 16px; margin: 16px 0; }
.protein { border-left: 3px solid var(--accent); padding-left: 12px; margin: 12px 0; }
pre { background: var(--code-bg); border-radius: 6px; padding: 12px; margin: 0;
      overflow-x: auto; font-size: 0.9rem; line-height: 1.6; }
code, pre, .seq { font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace; }
details { margin-top: 12px; }
summary { cursor: pointer; color: var(--accent); }
.table-wrap { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; margin-top: 8px; font-size: 0.88rem; }
th, td { border-bottom: 1px solid var(--border); padding: 6px 8px; text-align: left; white-space: nowrap; }
th { color: var(--muted); font-weight: 600; }
.empty { color: var(--muted); }
.legend { display: grid; grid-template-columns: repeat(auto-fill, minmax(190px, 1fr)); gap: 2px 16px;
          margin-top: 8px; font-size: 0.9rem; }
footer { color: var(--muted); font-size: 0.85rem; margin-top: 24px; }
"""


def build_page(results, input_name, min_length, both_strands):
    """Put the whole HTML page together."""
    found = sum(1 for result in results if result["main"] is not None)
    strands = "both strands" if both_strands else "the forward strand"
    legend = "\n".join(
        f"<div><code>{letter}</code> {html.escape(name)}</div>"
        for letter, name in AMINO_ACID_NAMES.items()
    )
    sections = "\n".join(record_html(result, min_length) for result in results)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Proteins from {html.escape(input_name)}</title>
<style>{PAGE_STYLE}</style>
</head>
<body>
<main>
<h1>Proteins from {html.escape(input_name)}</h1>
<p class="facts">{len(results)} sequence{"s" if len(results) != 1 else ""} read ·
a protein found in {found} · searched {strands} for open reading frames
of at least {min_length} amino acids</p>
{sections}
<details>
<summary>What do the letters mean?</summary>
<div class="legend">
{legend}
</div>
</details>
<footer>
An <strong>open reading frame (ORF)</strong> runs from a start codon (AUG) to the next stop codon
(UAA, UAG or UGA) in the same reading frame. The main protein is the longest ORF that ends at a stop codon.
Made with reader.py, using the standard genetic code.
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
            f.write(f'>{result["header"]} | protein, {len(main["protein"])} aa, '
                    f'{main["strand"]} strand bases {main["start"]}-{main["end"]}\n')
            for i in range(0, len(main["protein"]), 60):
                f.write(main["protein"][i:i + 60] + "\n")


# ---------------------------------------------------------------------------
# 5. The command-line program
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Translate the sequences in a FASTA file into proteins and save them as a web page."
    )
    parser.add_argument("-f", "--file", required=True, help="input FASTA file")
    parser.add_argument("-o", "--output",
                        help="HTML page to write (default: <input name>_proteins.html, next to the input)")
    parser.add_argument("--min-length", type=int, default=50,
                        help="shortest protein to report, in amino acids (default: 50)")
    parser.add_argument("--both-strands", action="store_true",
                        help="also search the opposite strand (useful for genomic DNA)")
    parser.add_argument("--fasta", help="also save the main proteins to this FASTA file")
    args = parser.parse_args()

    input_path = Path(args.file)
    if not input_path.is_file():
        sys.exit(f"Error: can't find the file '{input_path}'.")
    if args.min_length < 1:
        sys.exit("Error: --min-length must be at least 1.")

    records = read_fasta(input_path)
    if not records:
        sys.exit(f"Error: no sequences found in '{input_path}'. Is it a FASTA file?")

    results = []
    for header, dna in records:
        results.append(analyze(header, dna, args.min_length, args.both_strands))

    output_path = Path(args.output) if args.output else input_path.with_name(input_path.stem + "_proteins.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(build_page(results, input_path.name, args.min_length, args.both_strands))

    # A short summary in the terminal, too.
    print(f"Read {len(results)} sequence(s) from {input_path.name}")
    for result in results:
        main_orf = result["main"]
        if main_orf is None:
            print(f"  {result['header'][:40]}: no protein of at least {args.min_length} amino acids")
        else:
            protein = main_orf["protein"]
            print(f"  {result['header'][:40]}: {len(protein)} amino acids, starting {protein[:15]}...")
    print(f"Saved the page: {output_path}  (open it in your web browser)")

    if args.fasta:
        write_protein_fasta(results, args.fasta)
        print(f"Saved the proteins as FASTA: {args.fasta}")


if __name__ == "__main__":
    main()
