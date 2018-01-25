#! /usr/bin/env python
from __future__ import print_function
import sys
from Bio import SeqIO

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='extract genes from fasta.')
    parser.add_argument('fasta', type=argparse.FileType('rU'))
    parser.add_argument('bed', type=argparse.FileType('rU'))        
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    args = parser.parse_args()
    
    seqs = {s.id:s for s in SeqIO.parse(args.fasta, 'fasta')}
    bed = (l.strip('\n').split('\t') for l in args.bed)
    for rec in bed:
        s = seqs[rec[0]][int(rec[1]):int(rec[2])]
        if rec[5] == '-':
            s = s.reverse_complement()
        s.id = '%s.%s' % (s.id, rec[3])
        s.description = '%s-%s(%s)' % (rec[1], rec[2], rec[5])
        SeqIO.write(s, args.outfile, 'fasta')
