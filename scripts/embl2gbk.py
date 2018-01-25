#! /usr/bin/env python
from __future__ import print_function
import sys
from Bio import SeqIO

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='convert embl to genbank.')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('rU'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    args = parser.parse_args()
    
    for s in SeqIO.parse(args.infile, 'embl'):
        _ = SeqIO.write(s, args.outfile, 'genbank')
