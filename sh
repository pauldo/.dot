if command -v navi > /dev/null; then
  if [ -n "$ZSH_VERSION" ]; then
    eval "$(navi widget zsh)"
    bindkey -r '^g'
    # Alt+s
    bindkey '\es' _navi_widget
    export ZSH_COMPDUMP="$HOME/.cache/zcompdump"
    autoload -Uz compinit
    compinit -d "$ZSH_COMPDUMP"
  elif [ -n "$BASH_VERSION" ]; then
    eval "$(navi widget bash)"
    # chsh -s $(which zsh)
  fi
fi
