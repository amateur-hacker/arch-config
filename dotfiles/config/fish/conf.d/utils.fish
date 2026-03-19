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

# Refresh arch linux mirrors
function refresh_mirrors --description "Refresh mirrors using local GeoIP + sync pacman"
    echo (set_color cyan)"[INFO] Detecting public IP..."(set_color normal)

    set -l ip (curl -fsSL ifconfig.me)

    if test -z "$ip"
        echo (set_color red)"[ERROR] Failed to get public IP"(set_color normal)
        return 1
    end

    echo (set_color cyan)"[INFO] Detecting country via GeoIP..."(set_color normal)

    set -l geo (geoiplookup $ip)

    if test $status -ne 0 -o -z "$geo"
        echo (set_color red)"[ERROR] geoiplookup failed"(set_color normal)
        return 1
    end

    set -l country (string split ":" $geo)[2]
    set country (string trim $country)
    set country (string split "," $country)[1]
    set country (string trim $country)

    if not string match -rq '^[A-Z]{2}$' -- $country
        echo (set_color red)"[ERROR] Invalid country code: $country"(set_color normal)
        return 1
    end

    echo (set_color cyan)"[INFO] Using country: $country"(set_color normal)

    set -l tmp (mktemp)
    set -l url "https://archlinux.org/mirrorlist/?country=$country&protocol=https&use_mirror_status=on"

    echo (set_color cyan)"[INFO] Fetching mirror list..."(set_color normal)

    if not curl -fsSL "$url" | sed -e 's/^#Server/Server/' -e '/^#/d' >"$tmp"
        echo (set_color red)"[ERROR] Failed to fetch mirror list"(set_color normal)
        command rm -f "$tmp"
        return 1
    end

    if test ! -s "$tmp"
        echo (set_color red)"[ERROR] Empty mirror list"(set_color normal)
        command rm -f "$tmp"
        return 1
    end

    echo (set_color cyan)"[INFO] Backing up current mirrorlist..."(set_color normal)
    sudo cp /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.bak

    echo (set_color cyan)"[INFO] Ranking mirrors..."(set_color normal)

    if not rankmirrors -n 5 "$tmp" | sudo tee /etc/pacman.d/mirrorlist >/dev/null
        echo (set_color red)"[ERROR] Mirror update failed"(set_color normal)
        command rm -f "$tmp"
        return 1
    end

    command rm -f "$tmp"

    echo (set_color cyan)"[INFO] Syncing package databases..."(set_color normal)

    if sudo pacman -Syy
        echo (set_color green)"[SUCCESS] Mirrors updated + DB synced ✔"(set_color normal)
    else
        echo (set_color red)"[ERROR] Pacman sync failed"(set_color normal)
        return 1
    end
end
