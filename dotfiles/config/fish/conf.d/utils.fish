# Custom touch override for verbose output
function touch --description "Change file timestamps"
    for file in $argv
        if test -e "$file"
            echo "touch: updated timestamp '$file'"
        else
            echo "touch: created file '$file'"
        end
        command touch "$file"
    end
end

# cd to folder when quitting yazi
function yazi_cd --description "Open yazi and cd to last dir"
    set -l tmp (mktemp -t "yazi-cwd.XXXXXX")
    set -l cwd

    yazi $argv --cwd-file="$tmp"
    set cwd (cat "$tmp")
    if test -n "$cwd" -a "$cwd" != "$PWD"
        cd "$cwd"
    end
    command rm -f -- "$tmp"
end

# Display internal and external IP
function whatismyip --description "Show internal & external IP"
    set interface (ip route | grep default | awk '{print $5}')

    echo -n "Internal IP: "
    ip -4 addr show $interface | grep "inet " | awk '{print $2}' | cut -d/ -f1

    echo -n "External IP: "
    curl -s -4 ifconfig.me
end

# Source fish configs
function sfc --description "Reload all fish configs"
    for f in ~/.config/fish/**/*.fish
        if test -f $f
            source $f
        else
            echo (set_color red)"Warning: $f not found!"(set_color normal)
        end
    end
    clear
    echo (set_color green)"Fish config reloaded ✅"(set_color normal)
end
