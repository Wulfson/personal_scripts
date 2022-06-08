export HISTSIZE=8000
export HISTFILESIZE=-1
export HISTIGNORE="&:ll:ls:[bf]g:exit"
export TERM='xterm-256color'
export EDITOR=vim

export PATH=$HOME'/bin:'$PATH
export PYTHONSTARTUP=~/python_interpreter_startup.py

alias sresume='screen -t bash -h 5000 -d -R -S bash'
alias srshort='screen -c /home/ubuntu/.screenrc_short -t bash -h 5000 -d -R -S bash'
alias gx='grep -nR --exclude-dir=".git" --exclude="*.pyc"'
alias sfix="export SSH_AUTH_SOCK=\$(find /tmp/ssh-* -user $USER -name agent\* -printf '%T@ %p\n' 2>/dev/null | sort -k 1nr | sed 's/^[^ ]* //' | head -n 1)"

for file in ./scripts/*;
 do
      source $file;
 done
