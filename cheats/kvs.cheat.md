% kvs

# copyvalue
echo "<getvalue>" | tr -d '\n' | navi --query "alias :: clip" --best-match

$ query: echo "link|dsn|ip" | tr '|' '\n'
$ getvalue: navi --query ":kv: <query>" --best-match --print | column -t --- --column 2
