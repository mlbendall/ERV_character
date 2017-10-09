# HERV9

## RepBase

| name | region |
| --- | --- |
| HERV9 | internal |
| LTR12 | LTR |
| LTR12B | LTR |
| LTR12C | LTR |
| LTR12D | LTR |
| LTR12E | LTR |
| LTR12F | LTR |


Download the record for each model in EMBL format. (A slight formatting 
correction is made to this file to make it readable with BioPython):

```bash
url="http://www.girinst.org/protected/repbase_extract.php"
cat repbase/ids.txt | while read id; do
    curl -u $(cat ../repbase_pw.txt) "$url?access=$id&format=EMBL" |\
    perl -lpe 's/^DR\s+\[\d+\] \(Consensus\)/DR   REPBASE; CON/' > repbase/$id.embl
done
```

Convert each record into GenBank and FASTA formats:

```
for f in repbase/*.embl; do
    python -  <<EOF
from Bio import SeqIO
seq = SeqIO.read("$f", "embl")
SeqIO.write(seq, "${f%.*}.gbk", 'genbank')
seq.id = "${f%%.*}"
SeqIO.write(seq, "${f%.*}.fasta", 'fasta')
EOF

done
```

## DFAM

| name | dfam ID | region |
| --- | --- | --- |
| HERV9 | DF0000173 | internal |
| HERV9N | DF0001303 | internal |
| HERV9NC | DF0001278 | internal |
| LTR12 | DF0000399 | LTR |
| LTR12B | DF0000401 | LTR |
| LTR12C | DF0000402 | LTR |
| LTR12D | DF0000403 | LTR |
| LTR12E | DF0000404 | LTR |
| LTR12F | DF0000405 | LTR |
| LTR12_v | DF0000400 | LTR |

Download the seed alignment and HMM for each model.

```
cat dfam/ids.txt | while read l; do
    n=$(cut -f1 <<<"$l")
    i=$(cut -f2 <<<"$l")
    echo "Name: $n, ID: $i"
    curl -X POST -F "file=hmm" http://dfam.org/download/model/$i > dfam/$n.hmm.gz
    curl -X POST -F "file=seed" http://dfam.org/download/model/$i > dfam/$n.seed.gz
done
```    

Create model-derived consensus for each record.

```
for f in dfam/*.hmm.gz; do
    hmmemit -C $f > ${f%%.*}_consensus.fasta
done
```