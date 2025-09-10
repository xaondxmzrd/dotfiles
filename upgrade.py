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


def download_file(url: str, target: Path, overwrite: bool = True):
    if target.exists() and not overwrite:
        return

    target.parent.mkdir(parents=True, exist_ok=True)

    resp = requests.get(url)
    resp.raise_for_status()
    target.write_bytes(resp.content)


def duplicate_file(original: Path, count: int):
    base, ext = original.stem, original.suffix
    for i in range(1, count):
        copy = original.with_name(f"{base}{i}{ext}")
        shutil.copy2(original, copy)


def apply_patch(target: Path, patch_file: Path):
    if not target.exists() or not patch_file.exists():
        return

    if shutil.which("patch") is None:
        return

    subprocess.run(["patch", "-p0", target, "-i", patch_file], check=True)


def main():
    github_hostname = "https://raw.githubusercontent.com"

    mpv_repo = github_hostname + "/mpv-player/mpv/master"
    mpv_gallery_repo = github_hostname + "/occivink/mpv-gallery-view/master"

    root_dir = read_root_dir()
    mpv_config_dir = root_dir / "dot_config/mpv"

    files_for_download: dict[str, Path] = {
        mpv_repo + "/TOOLS/lua/autoload.lua": mpv_config_dir / "scripts/autoload.lua",
        mpv_gallery_repo + "/script-modules/gallery.lua": mpv_config_dir / "script-modules/gallery.lua",
        mpv_gallery_repo + "/scripts/playlist-view.lua": mpv_config_dir / "scripts/playlist-view.lua",
        mpv_gallery_repo + "/scripts/gallery-thumbgen.lua": mpv_config_dir / "scripts/gallery-thumbgen.lua",
    }

    with ThreadPoolExecutor() as executor:
        executor.map(download_file, files_for_download.keys(), files_for_download.values())

    original = mpv_config_dir / "scripts/gallery-thumbgen.lua"
    if original.exists():
        num_procs = multiprocessing.cpu_count()
        duplicate_file(original, num_procs)

    apply_patch(mpv_config_dir / "scripts/playlist-view.lua", Path("playlist-view.lua.patch"))


if __name__ == "__main__":
    main()
