% program

# check ip
curl https://ipinfo.io/json

# check weather
curl https://wttr.in

# check speed
curl -s https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py | python -

# check region restriction
bash <(curl -L -s https://raw.githubusercontent.com/lmc999/RegionRestrictionCheck/main/check.sh)

