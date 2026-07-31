import argparse 

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', type=str, required=True, help='input FASTA file')

args = parser.parse_args()

input_file = open(args.file, 'r')
output_file = open('codon.txt', 'w')

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
        for n in range(0, len(output), 3):
            codon = output[n:n + 3]
        #     output_file.write('(' + codon + ')') 
        # output_file.write('\n')
        

        for codon in output:
            amino_acid = ''
            if codon == 'AUG':
                amino_acid += 'START'
            elif codon in ('UUU', 'UUC'):   #this means if codon=='UUU' or codon=='UUC'
                amino_acid += 'Phe'
            elif codon in ('UUA', 'UUG', 'CUU', 'CUC', 'CUA', 'CUG'):
                amino_acid  += 'Leu'
            elif codon in ('AUU', 'AUC', 'AUA'):
                amino_acid  += 'Ile'
            elif codon == ('GUU', 'GUC', 'GUA', 'GUG'):
                amino_acid  += 'Val'
            elif codon == ('UCU', 'UCC', 'UCA', 'UCG', 'AGU', 'AGC'):
                amino_acid  += 'Ser'
        output_file.write(amino_acid)





            


        #     if codon == 'AUG':
        #         output += 'START'
        #     elif codon == 'UUU' or 'UUC':
        #         output += 'Phe'
        #     elif codon == 'UUA' or 'UUG' or 'CUU' or 'CUC' or 'CUA' or 'CUG':
        #         output += 'Leu'
        #     elif codon == 'AUU' or 'AUC' or 'AUA':
        #         output += 'Ile'
        #     elif codon == 'GUU' or 'GUC' or 'GUA' or 'GUG':
        #         output += 'Val'
        #     elif codon == 'UCU' or 'UCC' or 'UCA' or 'UCG' or 'AGU' or 'AGC':
        #         output += 'Ser'
        # output_file.write(output)

    