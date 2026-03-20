if command -v navi > /dev/null; then
	eval "$(navi widget zsh)"
  bindkey -r '^g'
  # Alt+s
  bindkey '\es' _navi_widget
fi
