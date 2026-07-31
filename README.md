# Python

Personal Python learning and practice projects.

## Structure

- **`hello_world/basics/`** — small scripts working through core Python concepts: variables, loops, conditionals, functions, string/type operations, and comparison and logical operators.
- **`hello_world/Python practice/`** — general practice scripts, including coding exercises and notes from learning sessions.
- **`hello_world/adder.py/`** — `adder.py`, a small CLI tool (built with `argparse`) that prints a greeting and optionally sums/multiplies a list of numbers, writes output to a file, and times execution.
- **`CLI_project/`** — `reader.py`, a work-in-progress CLI tool that reads a FASTA file, transcribes DNA to RNA, and translates codons into amino acids.

## Running the CLI tools

```bash
# adder.py
python3 "hello_world/adder.py/adder.py" "Hello!" -n 1 2 3 -v 2

# reader.py
python3 CLI_project/reader.py -f CLI_project/fasta.txt
```
