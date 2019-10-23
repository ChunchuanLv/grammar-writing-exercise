for d in */ ; do
    python2 pcfg_parse_gen.py -i -g "$d*.gr" < "$d"other.txt
done

