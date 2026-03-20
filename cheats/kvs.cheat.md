% kvs

# search nvalue
echo "<getvalue>" | tr -d '\n' | navi --query "alias :: clip" --best-match

$ query: echo "link|dsn|ip" | tr '|' '\n'
$ getvalue: navi --query ":kv: <query>" --print | column -t --- --column 2
