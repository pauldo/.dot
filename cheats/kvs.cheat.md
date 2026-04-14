% kvs

# searchvalue sv
echo "<getvalue>" | tr -d '\n'

# searchlink
echo "<getlink>" | tr -d '\n'

$ appendsearch: echo $NAVI_KV_SEARCH
$ query: echo "link|dsn|ip" | tr '|' '\n'
$ getvalue: navi --query ":kv: <query>" --print | column -t --- --column 2
$ getlink: navi --query ":kv: :link: <appendsearch>" --print | column -t --- --column 2
