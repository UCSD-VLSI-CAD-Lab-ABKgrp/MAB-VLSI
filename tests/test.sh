export NUM=$(cat tests/params.tmp | wc -l)
echo a,b > tests/samples.tmp
for ((i=0; i<10; i++)); do echo $i,$i; done >> tests/samples.tmp