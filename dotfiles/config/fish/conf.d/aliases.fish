# Common command settings
alias cp="cp -iv"
alias mv="mv -iv"
alias rm="trash-put -iv"
alias rrm="command rm"
alias bc="bc -ql"
alias qalc="qalc -t"
alias mkdir="mkdir -pv"
alias locate="plocate"
alias "trash-empty"="trash-empty -v"
alias grep='grep --color=auto'
alias rg='rg --smart-case --color=auto'
alias ln='ln -iv'
alias chmod='chmod -v'
alias chown='chown -v'
alias ls='lsd -a'
alias ll='lsd -al'
alias lt='lsd -a --tree'

# Application shortcuts
alias v="nvim"
alias z="zathura"

# Clean home directory
alias wget="wget --hsts-file=\"$XDG_DATA_HOME/wget-hsts\""

# Disk info
alias duf="duf --hide special"

# Package manager helpers
alias packsi="pacman -Slq | fzf --multi --preview 'pacman -Sii {1}' --preview-window=down:75% | xargs -ro sudo pacman -S" # package search and install
alias packsrm="pacman -Qqe | fzf --multi --preview 'pacman -Qi {1}' --preview-window=down:75% | xargs -ro sudo pacman -Rns" # package search and remove
