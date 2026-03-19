% keys, vals

# copy value
echo "<getvalue>" | tr -d '\n' | navi --query "alias :: clip" --best-match

$ query: echo "link|dsn|ip" | tr '|' '\n'
$ getvalue: navi --query "<query>" --best-match --print | column -t --- --column 2
