% system

# set timezone
sudo timedatectl set-timezone Asia/Shanghai

; initialize .zshrc or .bashrc
# init zsh or bash

CURRENT_SHELL=$(basename "$SHELL")

if [[ "$CURRENT_SHELL" == "zsh" ]]; then
    RC_FILE="$HOME/.zshrc"
else
    RC_FILE="$HOME/.bashrc"
fi

CHECK_FILE="\$HOME/<file>"
LINE="[ -f $CHECK_FILE ] && source $CHECK_FILE"

if grep -Fq "$CHECK_FILE" "$RC_FILE"; then
    echo "Ignored: $RC_FILE (File exists)"
else
    echo -e "\n$LINE" >> "$RC_FILE"
    echo "Append success to $RC_FILE"
fi

$ file: echo ".append|.append_custom" | tr '|' '\n' | column -t
