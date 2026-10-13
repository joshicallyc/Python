import argparse 

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', type=str, required=True, help='input FASTA file')

args = parser.parse_args()

input_file = open(args.file, 'r', encoding='utf-8')
output_file = open('amino_acid_sequence.txt', 'w', encoding='utf-8')

for line in input_file:
    line = line.upper()
    line = line.strip()
    if line.startswith('>'):
        output_file.write(line + '\n')
    else:
        output = ''
        for letter in line:
            if letter == 'A':
                output += 'U'
            elif letter == 'T':
                output += 'A'
            elif letter == 'C':
                output += 'G'
            elif letter == 'G':
                output += 'C'

        amino_acid_line = ''
        for n in range(0, len(output), 3):
            codon = output[n:n + 3]
            amino_acid_groups = {
                'Alanine': ('GCU', 'GCC', 'GCA', 'GCG'),
                'Arginine': ('CGU', 'CGC', 'CGA', 'CGG', 'AGA', 'AGG'),
                'Asparagine': ('AAU', 'AAC'),
                'Aspartic_Acid': ('GAU', 'GAC'),
                'Cysteine': ('UGU', 'UGC'),
                'Glutamic_Acid': ('GAA', 'GAG'),
                'Glutamine': ('CAA', 'CAG'),
                'Glycine': ('GGU', 'GGC', 'GGA', 'GGG'),
                'Histidine': ('CAU', 'CAC'),
                'Isoleucine': ('AUU', 'AUC', 'AUA'),
                'Leucine': ('UUA', 'UUG', 'CUU', 'CUC', 'CUA', 'CUG'),
                'Lysine': ('AAA', 'AAG'),
                'START': ('AUG',),
                'Phenylalanine': ('UUU', 'UUC'),
                'Proline': ('CCU', 'CCC', 'CCA', 'CCG'),
                'Serine': ('UCU', 'UCC', 'UCA', 'UCG', 'AGU', 'AGC'),
                'Threonine': ('ACU', 'ACC', 'ACA', 'ACG'),
                'Tryptophan': ('UGG',),
                'Tyrosine': ('UAU', 'UAC'),
                'Valine': ('GUU', 'GUC', 'GUA', 'GUG'),
                'STOP': ('UAA', 'UAG', 'UGA')
            }
            codon_table = {}
            for amino_acid_name, codons in amino_acid_groups.items():
                for codon_key in codons:
                    codon_table[codon_key] = amino_acid_name
            amino_acid = codon_table.get(codon, 'UNKNOWN')
            amino_acid_line += '(' + amino_acid + ')' + ' '
        output_file.write(amino_acid_line + '\n')  