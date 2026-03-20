% install

# claude
command -v claude >/dev/null 2>&1 || curl -fsSL https://claude.ai/install.sh | bash

# opencode
command -v opencode >/dev/null 2>&1 || curl -fsSL https://opencode.ai/install | bash

# kiro
command -v kiro >/dev/null 2>&1 || curl -fsSL https://cli.kiro.dev/install | bash

# zb
command -v zb >/dev/null 2>&1 || curl -fsSL https://zerobrew.rs/install | bash

# singbox
command -v singbox >/dev/null 2>&1 || curl -fsSL https://sing-box.app/install.sh | sh

# ohmyzsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# s-ui
command -v s-ui >/dev/null 2>&1 || bash <(curl -Ls https://raw.githubusercontent.com/alireza0/s-ui/master/install.sh)

# chsrc
command -v chsrc >/dev/null 2>&1 || curl https://chsrc.run/posix | bash

# x-cmd
command -v x-cmd >/dev/null 2>&1 || curl -L https://get.x-cmd.com | bash

% run

# githubhost
curl https://raw.hellogithub.com/hosts

# checkip
curl https://ipinfo.io/json

# checkweather
curl https://wttr.in

# checkspeed
curl -s https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py | python -

# checkregionrestriction
bash <(curl -L -s https://raw.githubusercontent.com/lmc999/RegionRestrictionCheck/main/check.sh)

