#! /usr/bin/env python
from __future__ import print_function
import sys
from Bio import SeqIO
import re

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='extract genes from fasta.')
    parser.add_argument('fasta', type=argparse.FileType('rU'))
    parser.add_argument('gff', type=argparse.FileType('rU'))        
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    args = parser.parse_args()
    
    seqs = {s.id:s for s in SeqIO.parse(args.fasta, 'fasta')}
    gff = (l.strip('\n').split('\t') for l in args.gff if not l.startswith('#'))
    for rec in gff:
        if rec[2] != 'gene': continue
        s = seqs[rec[0]][(int(rec[3])-1):int(rec[4])]
        if rec[6] == '-':
            s = s.reverse_complement()
        attrs = dict(f.split('=') for f in rec[8].split(';'))
        s.id = '%s.%s' % (s.id, attrs['Name'])
        s.description = '%s-%s(%s)' % (rec[3], rec[4], rec[6])
        SeqIO.write(s, args.outfile, 'fasta')
