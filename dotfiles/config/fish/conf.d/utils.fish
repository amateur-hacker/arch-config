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

## Search for text in files (optional: pass directory)
function ftext --description "Search text in files (smart pager)"
    if test (count $argv) -lt 1
        echo "Usage: ftext <pattern> [dir]"
        return 1
    end

    set -l pattern "$argv[1]"
    set -l dir (test (count $argv) -ge 2; and echo $argv[2]; or echo .)

    if not test -d "$dir"
        echo (set_color red)"Error: '$dir' is not a valid directory."(set_color normal)
        return 1
    end

    set -l output (grep -iIHrn --color=always "$pattern" "$dir" | string collect)

    if test -z "$output"
        echo "No matches found."
        return 1
    end

    set -l lines (count (string split \n -- "$output"))
    set -l screen_lines (tput lines)

    if test "$lines" -gt "$screen_lines"
        echo "$output" | less -R
    else
        echo "$output"
    end
end

# Send a notification after long running command
function alert --description "Notify after last command"
    set -l last_command (history | tail -n1 | string replace -r '^[ \t]*[0-9]+[ \t]*' '' | string replace -r '[;&|][ \t]*alert$' '')
    if test $status -eq 0
        set -l icon terminal
    else
        set -l icon error
    end
    notify-send --urgency=low -i "$icon" "$last_command"
end

# Display internal and external IP
function whatismyip --description "Show internal & external IP"
    echo -n "Internal IP: "
    ip addr show wlan0 2>/dev/null | grep "inet " | awk '{print $2}' | cut -d/ -f1
    echo -n "External IP: "
    curl -s -4 ifconfig.me
end

# Count files, links, and directories (optional: pass directory)
function countfiles --description "Count files, links, dirs"
    set -l target_dir (test (count $argv) -gt 0; and echo $argv[1]; or echo .)

    if not test -d "$target_dir"
        echo (set_color red)"Error: '$target_dir' is not a directory."(set_color normal)
        return 1
    end

    for t in files links directories
        switch $t
            case files
                set type_char f
            case links
                set type_char l
            case directories
                set type_char d
        end
        set -l count (find $target_dir -type "$type_char" 2>/dev/null | wc -l)
        echo "$count $t"
    end
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
