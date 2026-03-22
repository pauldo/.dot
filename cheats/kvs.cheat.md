% kvs

# search nvalue n2
echo "<getvalue>" | tr -d '\n' | navi --query "alias :: clip" --best-match

# searchlink
echo "<getlink>" | tr -d '\n' | navi --query "alias :: clip" --best-match

$ appendsearch: echo $NAVI_KV_SEARCH
$ query: echo "link|dsn|ip" | tr '|' '\n'
$ getvalue: navi --query ":kv: <query>" --print | column -t --- --column 2
$ getlink: navi --query ":kv: :link: <appendsearch>" --print | column -t --- --column 2
