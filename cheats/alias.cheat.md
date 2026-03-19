% alias

# :: setproxy
export HTTPS_PROXY=http://<ip>:<port> HTTP_PROXY=http://<ip>:<port> ALL_PROXY=http://<ip>:<port>

# :: unsetproxy
unset HTTPS_PROXY HTTP_PROXY ALL_PROXY

# :: tt
if ! command -v taskwarrior-tui > /dev/null; then
  brew install taskwarrior-tui
fi
taskwarrior-tui

# :: clip
if command -v pbcopy > /dev/null; then
  pbcopy
elif command -v wl-copy > /dev/null; then
  wl-copy
elif command -v xclip > /dev/null; then
  xclip -sel clip
fi

# :: pasteclip
if command -v pbpaste > /dev/null; then
  pbpaste
elif command -v wl-paste > /dev/null; then
  wl-paste
elif command -v xclip > /dev/null; then
  xclip -sel clip -o
fi

# :: np
navi --print

# :: ncp
navi --print | navi --query "alias :: clip" --best-match

$ ip: echo "127.0.0.1|" | tr '|' '\n'
$ port: echo "7890|" | tr '|' '\n'
