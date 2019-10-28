for d in */ ; do
    echo "$d"other.txt "start"
    python2 pcfg_parse_gen.py -i -g "$d*.gr" --unseen "unseen.tags" < "$d"other.txt &> "$d"parsed.txt
    echo "$d"other.txt "done"
done

