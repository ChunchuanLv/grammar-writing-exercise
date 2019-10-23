for d in */ ; do
    python2 pcfg_parse_gen.py -o 10 -g "$d*.gr"  > "$d"sample.txt
done

