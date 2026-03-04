# Default applications
set -x EDITOR nvim
set -x VISUAL nvim
set -x TERMINAL kitty
set -x BROWSER google-chrome-stable

# XDG base directories
set -x XDG_CONFIG_HOME "$HOME/.config"
set -x XDG_DATA_HOME "$HOME/.local/share"
set -x XDG_STATE_HOME "$HOME/.local/state"
set -x XDG_CACHE_HOME "$HOME/.cache"

# Common user directories
set -x XDG_DOCUMENTS_DIR "$HOME/documents"
set -x XDG_DOWNLOADS_DIR "$HOME/downloads"
set -x XDG_MUSIC_DIR "$HOME/music"
set -x XDG_PICTURES_DIR "$HOME/pictures"
set -x XDG_VIDEOS_DIR "$HOME/videos"

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
fish_add_path $HOME/.local/bin

# Redirect tool-specific files to XDG paths
set -x LESSHISTFILE "$XDG_DATA_HOME/less_history"
set -x PYTHON_HISTORY "$XDG_DATA_HOME/python_history"
set -x GTK2_RC_FILES "$XDG_CONFIG_HOME/gtk-2.0/gtkrc-2.0"
set -x GNUPGHOME "$XDG_DATA_HOME/gnupg"
set -x CARGO_HOME "$XDG_DATA_HOME/cargo"
set -x GOPATH "$XDG_DATA_HOME/go"
set -x GOBIN "$GOPATH/bin"
set -x GOMODCACHE "$XDG_CACHE_HOME/go/mod"
set -x REDISCLI_HISTFILE "$XDG_DATA_HOME/redis/rediscli_history"
set -x GIT_CONFIG_GLOBAL "$XDG_CONFIG_HOME/git/config"
# set -x WGETRC "$XDG_CONFIG_HOME/wget/wgetrc"
# set -x REDISCLI_RCFILE "$XDG_CONFIG_HOME/redis/redisclirc"
# set -x PYTHONSTARTUP "$XDG_CONFIG_HOME/python/pythonrc"
# set -x FFMPEG_DATADIR "$XDG_CONFIG_HOME/ffmpeg"
# set -x ZDOTDIR "$XDG_CONFIG_HOME/zsh"
# set -x PARALLEL_HOME "$XDG_CONFIG_HOME/parallel"
# set -x NPM_CONFIG_USERCONFIG "$XDG_CONFIG_HOME/npm/npmrc"
# set -x _JAVA_OPTIONS "-Djava.util.prefs.userRoot=$XDG_CONFIG_HOME/java"
# set -x XINITRC "$XDG_CONFIG_HOME/x11/xinitrc"
# set -x XPROFILE "$XDG_CONFIG_HOME/x11/xprofile"
# set -x XRESOURCES "$XDG_CONFIG_HOME/x11/xresources"
# set -x GRADLE_USER_HOME "$XDG_DATA_HOME/gradle"
# set -x NUGET_PACKAGES "$XDG_CACHE_HOME/NuGetPackages"
# set -x WINEPREFIX "$XDG_DATA_HOME/wineprefixes/default"

# Files to ensure
for f in $LESSHISTFILE $PYTHON_HISTORY $REDISCLI_HISTFILE
    if test $f = $REDISCLI_HISTFILE
        if type -q redis-cli
            ensure_file $REDISCLI_HISTFILE
        end
    else
        ensure_file $f
    end
end

# Directories to ensure
for d in $GNUPGHOME $ATAC_MAIN_DIR
    ensure_dir $d
    if test $d = $GNUPGHOME
        set current_mode (stat -c "%a" $GNUPGHOME 2>/dev/null)

        if test "$current_mode" != 700
            chmod 700 $GNUPGHOME
        end
    end
end

# Personal environment tweaks
set -x NODE_OPTIONS "--no-warnings --max-old-space-size=4096"
set -x MANPAGER "nvim +Man!"
set -x FZF_DEFAULT_OPTS "\
--color=bg+:#313244,bg:#1E1E2E,spinner:#F5E0DC,hl:#F38BA8 \
--color=fg:#CDD6F4,header:#F38BA8,info:#B4BEFE,pointer:#B4BEFE \
--color=marker:#B4BEFE,fg+:#CDD6F4,prompt:#B4BEFE,hl+:#F38BA8 \
--color=selected-bg:#45475A \
--color=border:#6C7086,label:#CDD6F4"
set -x LS_COLORS (dircolors -b  ~/.config/dircolors | sed 's/^LS_COLORS='\''//;s/'\''$//')
set -x ATAC_THEME "$XDG_CONFIG_HOME/atac/mocha.toml"

# Colored less + termcap vars
set -x LESS_TERMCAP_mb (printf '\e[1;38;2;243;139;168m') # pink
set -x LESS_TERMCAP_md (printf '\e[1;38;2;180;190;254m') # lavender
set -x LESS_TERMCAP_me (printf '\e[0m')
set -x LESS_TERMCAP_so (printf '\e[38;2;30;30;46;48;2;180;190;254m') # inverted lavender highlight
set -x LESS_TERMCAP_se (printf '\e[0m')
set -x LESS_TERMCAP_us (printf '\e[1;38;2;166;227;161m') # green underline
set -x LESS_TERMCAP_ue (printf '\e[0m')
