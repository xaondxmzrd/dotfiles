#!/usr/bin/env python3
import multiprocessing
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests


def read_root_dir() -> Path:
    chezmoiroot = Path(".chezmoiroot")
    if chezmoiroot.exists():
        return Path(chezmoiroot.read_text().strip())
    else:
        return Path(".")


ROOT_DIR = read_root_dir()
MPV_CONFIG_DIR = ROOT_DIR / "dot_config/mpv"
GITHUB_BASE = "https://raw.githubusercontent.com"
MPV_REPO = GITHUB_BASE + "/mpv-player/mpv/master"
MPV_GALLERY_REPO = GITHUB_BASE + "/occivink/mpv-gallery-view/master"
MPV_IMAGE_CONFIG_REPO = GITHUB_BASE + "/guidocella/mpv-image-config/main"


def download(url: str, target: Path, overwrite: bool = True):
    if target.exists() and not overwrite:
        return

    target.parent.mkdir(parents=True, exist_ok=True)

    resp = requests.get(url)
    resp.raise_for_status()
    target.write_bytes(resp.content)

    print(resp.reason, url)


def duplicate(original: Path, count: int):
    base, ext = original.stem, original.suffix
    for i in range(1, count):
        copy = original.with_name(f"{base}{i}{ext}")
        shutil.copy2(original, copy)


def patch(target: Path, patch_file: Path):
    if not target.exists() or not patch_file.exists():
        return

    if shutil.which("patch") is None:
        return

    subprocess.run(["patch", "-p0", target, "-i", patch_file], check=True)


def mpv_scripts_autoload_lua():
    download(MPV_REPO + "/TOOLS/lua/autoload.lua", MPV_CONFIG_DIR / "scripts/autoload.lua")


def mpv_script_modules_gallery_lua():
    path_from_mpv = "script-modules/gallery.lua"
    download(f"{MPV_GALLERY_REPO}/{path_from_mpv}", MPV_CONFIG_DIR / path_from_mpv)


def mpv_scripts_playlist_view_lua():
    path_from_mpv = "scripts/playlist-view.lua"
    path_from_woking = MPV_CONFIG_DIR / "scripts/playlist-view.lua"

    download(f"{MPV_GALLERY_REPO}/{path_from_mpv}", path_from_woking)
    patch(path_from_woking, Path("playlist-view.lua.patch"))


def mpv_scripts_gallery_thumbgen_lua():
    path_from_mpv = "scripts/gallery-thumbgen.lua"
    path_from_woking = MPV_CONFIG_DIR / path_from_mpv

    download(f"{MPV_GALLERY_REPO}/{path_from_mpv}", MPV_CONFIG_DIR / path_from_mpv)
    duplicate(path_from_woking, multiprocessing.cpu_count())


def mpv_mpv_conf():
    path_from_mpv = Path("mpv.conf")
    path_from_woking = MPV_CONFIG_DIR / path_from_mpv

    download(f"{MPV_IMAGE_CONFIG_REPO}/{path_from_mpv}", path_from_woking)
    patch(path_from_woking, Path("mpv.conf.patch"))


def main():
    with ThreadPoolExecutor() as executor:
        [
            executor.submit(func)
            for func in [
                mpv_scripts_autoload_lua,
                mpv_script_modules_gallery_lua,
                mpv_scripts_playlist_view_lua,
                mpv_scripts_gallery_thumbgen_lua,
                mpv_mpv_conf,
            ]
        ]


if __name__ == "__main__":
    main()
