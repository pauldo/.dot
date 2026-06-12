if command -v navi > /dev/null; then
  if [ -n "$ZSH_VERSION" ]; then
    eval "$(navi widget zsh)"

    _navi_to_clipboard() {
      local result=$(navi --query ":copy: " --print 2>/dev/null)
      if [ -n "$result" ]; then
        echo -n "$result" | clip
        zle -M "Copied: $result"
      fi
      zle reset-prompt
    }
    # Alt+c
    zle -N _navi_to_clipboard
    bindkey '\ec' _navi_to_clipboard

    _navi_smart_execute() {
      local result=$(navi --query ":env: " --print 2>/dev/null)
      if [ -n "$result" ]; then
        if [[ "$result" =~ "^echo " ]]; then
          LBUFFER="$LBUFFER$result"
        else
          eval "$result"
          zle -M "Executed: $result"
        fi
      fi
      zle reset-prompt
    }

    # Alt+e
    zle -N _navi_smart_execute
    bindkey '\ee' _navi_smart_execute

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
