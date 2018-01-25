# Family workflow

### ID Files

ID files are for mapping names to database ids.
We use two files, `ids.rmsk.txt` and `ids.dfam.txt`, for the
Repbase and Dfam databases.

### Models

Download the record for each model in EMBL format. (A slight formatting 
correction is made to this file to make it readable with BioPython):

```bash
url="http://www.girinst.org/protected/repbase_extract.php"
cat ids.rmsk.txt | while read id; do
    curl -u $(cat ../repbase_pw.txt) "$url?access=$id&format=EMBL" |\
    perl -lpe 's/^DR\s+\[\d+\] \(Consensus\)/DR   REPBASE; CON/' > models/$id.rmsk.embl
done
```

Convert each record into GenBank and FASTA formats:

```
for f in models/*.rmsk.embl; do
    ../scripts/embl2gbk.py < $f | tee ${f%.*}.gbk | ../scripts/gbk2fasta.py > ${f%.*}.fna
done
```
Download the HMM and seed alignment for each Dfam model.

```
cat ids.dfam.txt | while read l; do
    n=$(cut -f1 <<<"$l")
    i=$(cut -f2 <<<"$l")
    echo "Name: $n, ID: $i"
    curl -X POST -F "file=hmm" http://dfam.org/download/model/$i > models/${n}.hmm.gz
    curl -X POST -F "file=seed" http://dfam.org/download/model/$i > models/${n}.seed.gz
done
```

Create model-derived consensus for each record.

```
for f in models/*.hmm.gz; do
    hmmemit -C $f > ${f%%.*}-consensus.fna
done
```


###

```bash
python ../scripts/extract_genes.py dfam/HERV9_consensus.fasta dfam/HERV9_consensus.bed > HERV9.genes.fasta
cat dfam/LTR12_consensus.fasta dfam/LTR12B_consensus.fasta dfam/LTR12C_consensus.fasta dfam/LTR12D_consensus.fasta dfam/LTR12E_consensus.fasta dfam/LTR12F_consensus.fasta dfam/LTR12_v_consensus.fasta > HERV9.ltr.fasta



```
