#!/usr/bin/bash

root=$(cat .chezmoiroot)
github_hostname="raw.githubusercontent.com"

# mpv

mpv_config_dir="$root/dot_config/mpv"

## autoload

autoload_lua="https://$github_hostname/mpv-player/mpv/master/TOOLS/lua/autoload.lua"
wget "$autoload_lua" -O "$mpv_config_dir/scripts/autoload.lua"

## mpv_gallery_view

mpv_gallery_view_repository="https://$github_hostname/occivink/mpv-gallery-view/master"

files_of_mpv_gallery_view=(
    "script-modules/gallery.lua"
    "scripts/playlist-view.lua"
    "scripts/gallery-thumbgen.lua"
)

for file in "${files_of_mpv_gallery_view[@]}"; do
    wget "$mpv_gallery_view_repository/$file" -O "$mpv_config_dir/$file"
done

### playlist-view.lua

patch "$mpv_config_dir/scripts/playlist-view.lua" <"playlist-view.lua.patch"

### gallery-thumbgen.lua

original_file="$mpv_config_dir/scripts/gallery-thumbgen.lua"
for i in $(seq 2 $(nproc)); do
    cp "$original_file" "${original_file%.*}$i.${original_file##*.}"
done
