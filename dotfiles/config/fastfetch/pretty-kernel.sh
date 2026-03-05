#!/usr/bin/env bash

cache_file="/tmp/kernel_flavor.cache"

# Check cache
if [[ -f "$cache_file" ]]; then
  cat "$cache_file"
  exit 0
fi

kernel=$(uname -r)

# Pattern matching for flavor
case "$kernel" in
*-zen*) flavor="Zen" ;;
*-hardened*) flavor="Hardened" ;;
*-lts*) flavor="LTS" ;;
*-generic*) flavor="Generic" ;;
*-cachyos*) flavor="CachyOS" ;;
*) flavor="" ;;
esac

result="Linux${flavor:+ $flavor}"

# Cache result
echo "$result" >"$cache_file"

echo "$result"
