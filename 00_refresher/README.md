# Python refresher

A one-evening (about 60–75 minutes) Google Colab notebook that brings Python back after a break. It reviews
the core skills with DNA examples instead of toy problems, then runs the DNA translator in
[`CLI_project/`](../CLI_project/) to find its bug.

<a href="https://colab.research.google.com/github/joshicallyc/Python/blob/main/00_refresher/python_refresher.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

| Part | Topic | Practice |
|---|---|---|
| 0 | Setup | Download the project into Colab; a `check()` helper marks answers ✅ / ❌ / ⬜ |
| 1 | Strings | Uppercase, slicing codons, GC content, DNA → mRNA |
| 2 | Loops | Looping letter by letter vs. codon by codon with `range(0, len(seq), 3)` |
| 3 | `if` / `elif` / `else` | Labeling start and stop codons; why `==` and `in` differ |
| 4 | Dictionaries | A mini codon table: translating codons into a protein |
| 5 | Functions | `transcribe()` and `split_codons()` |
| 6 | Files | Reading a FASTA file: header vs. sequence lines |
| 7 | Debugging | Running the first version of `reader.py` and explaining why it outputs no amino acids |
| Bonus | Plotting | A bar chart of base counts with matplotlib |

**How to use it:** open it in Colab with the badge above, and run cells in order with **Shift + Enter**.
Each exercise has a collapsed hint and answer. Short on time? Parts 0–3 and 7 take about 40 minutes.
