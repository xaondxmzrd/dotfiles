import os
import subprocess


def diff(require_dir, check_dir):
    for dirpath, _, filenames in os.walk(require_dir):
        for filename in filenames:
            rel_path = os.path.relpath(os.path.join(dirpath, filename), require_dir)
            require_file = os.path.join(require_dir, rel_path)
            check_file = os.path.join(check_dir, rel_path)

            if not os.path.isfile(check_file):
                print(f"[!] File not found in: {check_file}")
                continue

            subprocess.run(["diff", "-u", "--color=auto", require_file, check_file])


diff("home", os.getenv("HOME"))
diff("root", "/")
