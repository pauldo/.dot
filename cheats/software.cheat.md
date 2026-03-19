% software

# install brew
if ! command -v brew >/dev/null 2>&1; then
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# install singbox
if ! command -v singbox >/dev/null 2>&1; then
  curl -fsSL https://sing-box.app/install.sh | sh
fi

# install ohmyzsh
if ! command -v zsh >/dev/null 2>&1; then
  sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
fi

# install chsrc
if ! command -v chsrc >/dev/null 2>&1; then
  curl https://chsrc.run/posix | sudo bash
fi

# install x-cmd
if ! command -v x-cmd >/dev/null 2>&1; then
  eval "$(curl https://get.x-cmd.com)"
fi


