# Disable default fish greeting
set fish_greeting

# Helpers
function ensure_file
    command mkdir -p (dirname $argv[1])
    test -f $argv[1]; or touch $argv[1]
end

function ensure_dir
    command mkdir -p $argv[1]
end

# Add to path
ensure_dir $HOME/.local/bin
fish_add_path $HOME/.local/bin $HOME/.local/share/bun/bin $HOME/.local/share/cargo/bin /var/lib/flatpak/exports/bin

# Setup vi mode keybindings and configure defaults
function fish_user_key_bindings
    fish_vi_key_bindings
    bind yy fish_clipboard_copy
    bind Y fish_clipboard_copy
    bind p fish_clipboard_paste
    bind -M visual -m default y 'fish_clipboard_copy; commandline -f end-selection repaint-mode'
    # bind -M insert -m default jk 'commandline -f repaint'
    bind --erase --preset -M visual \ev
    bind --erase --preset -M insert \ev
    bind -M insert ! __history_previous_command
    bind -M insert '$' __history_previous_command_arguments
end

# Support for !! and !$
function __history_previous_command
    switch (commandline -t)
        case "!"
            commandline -t $history[1]
            commandline -f repaint
        case "*"
            commandline -i !
    end
end

function __history_previous_command_arguments
    switch (commandline -t)
        case "!"
            commandline -t ""
            commandline -f history-token-search-backward
        case "*"
            commandline -i '$'
    end
end

# System info on launch if interactive
if status is-interactive
    fastfetch
    # nitch++
end

# Fish shell theme
fish_config theme choose "Catppuccin Mocha"

# Shell integrations
starship init fish | source
zoxide init --cmd cd fish | source
fzf --fish | FZF_ALT_C_COMMAND= FZF_CTRL_T_COMMAND= source
