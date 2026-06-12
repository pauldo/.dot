if command -v navi > /dev/null; then
  if [ -n "$ZSH_VERSION" ]; then
    eval "$(navi widget zsh)"

    _navi_to_clipboard() {
      local result=$(navi --print 2>/dev/null)
      if [ -n "$result" ]; then
        echo -n "$result" | clip
        zle -M "Copied: $result"
      fi
      zle reset-prompt
    }
    # Alt+c
    zle -N _navi_to_clipboard
    bindkey '\ec' _navi_to_clipboard

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
