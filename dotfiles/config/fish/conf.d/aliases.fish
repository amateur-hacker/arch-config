# Default flags
alias cp='cp -iv'
alias mv='mv -iv'
alias ln='ln -iv'
alias mkdir='mkdir -pv'
alias chmod='chmod -v'
alias chown='chown -v'
alias grep='grep --color=auto'
alias rg='rg --smart-case --color=auto'
alias df='df -h'
alias free='free -hm'
alias bc='bc -ql'
alias ping='ping -c 3'
alias ps='ps auxf'
alias less='less -R'
alias zip='zip -v'
alias unzip='unzip -v'
alias qalc='qalc -t'
alias dysk='dysk --sort type-desc'
alias duf='duf --hide special'
alias trash-empty='trash-empty -v'

# Command replacements
alias rm='trash-put -iv'
alias rrm='command rm'
alias cat='bat'
alias vim='nvim'
alias locate='plocate'
alias ls='lsd -al'
alias tree='lsd -a --tree'

# Shortcuts
alias v='nvim'
alias sv='EDITOR=nvim sudoedit'
alias z='zathura'
alias jctl="journalctl -p 3 -xb"

# Clean home directory
alias wget='wget --hsts-file="$XDG_DATA_HOME/wget-hsts"'

# Pacman helpers
alias packsi="pacman -Slq | fzf --multi --preview 'pacman -Sii {1}' --preview-window=down:75% | xargs -ro sudo pacman -S"
alias packsrm="pacman -Qqe | fzf --multi --preview 'pacman -Qi {1}' --preview-window=down:75% | xargs -ro sudo pacman -Rns"
