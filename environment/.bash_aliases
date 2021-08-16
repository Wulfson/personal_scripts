export HISTIGNORE="&:ll:ls:[bf]g:exit"
export TERM='xterm-256color'
export EDITOR=vim

alias gx='grep -nR --exclude-dir=".git" --exclude="*.pyc"'
alias sfix="export SSH_AUTH_SOCK=\$(find /tmp/ssh-* -user $USER -name agent\* -printf '%T@ %p\n' 2>/dev/null | sort -k 1nr | sed 's/^[^ ]* //' | head -n 1)"
alias sresume='screen -t bash -h 5000 -d -R -S bash'
alias srshort='screen -c /home/ubuntu/.screenrc_short -t bash -h 5000 -d -R -S bash'
