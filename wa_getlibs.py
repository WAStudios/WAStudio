# WAStudio/wa_getlibs.py

import os
import subprocess
import yaml

def getlibs():
    pkgmeta_path = "./WeakAuras2/.pkgmeta"
    libs_dir = "./libs"

    if not os.path.exists(pkgmeta_path):
        print(f".pkgmeta not found at {pkgmeta_path}")
        return

    with open(pkgmeta_path, "r") as f:
        pkgmeta_data = yaml.safe_load(f)

    externals = pkgmeta_data.get("externals", {})
    print(f"Starting library sync from .pkgmeta...")

    if not os.path.exists(libs_dir):
        os.makedirs(libs_dir, exist_ok=True)
        print(f"Created new libs directory: {libs_dir}")
    else:
        print(f"Using existing libs directory: {libs_dir}")

    print(f"Found {len(externals)} externals in .pkgmeta")

    for path, data in externals.items():
        target_path = os.path.join(libs_dir, os.path.basename(path))
        if isinstance(data, str):
            url = data
            branch = None
        elif isinstance(data, dict):
            url = data.get("url")
            branch = data.get("tag") or data.get("commit")
        else:
            print(f"Unknown format for {path}, skipping.")
            continue

        if os.path.exists(target_path):
            if os.path.exists(os.path.join(target_path, ".git")):
                print(f"Updating existing git repo {url} in {target_path}...")
                try:
                    subprocess.run(["git", "-C", target_path, "pull"], check=True)
                except subprocess.CalledProcessError:
                    print(f"Git pull failed for {target_path}, attempting to reset to origin/HEAD...")
                    subprocess.run(["git", "-C", target_path, "fetch"], check=True)
                    subprocess.run(["git", "-C", target_path, "reset", "--hard", "origin/HEAD"], check=True)
                if branch and branch.lower() not in ("head", "default"):
                    subprocess.run(["git", "-C", target_path, "checkout", branch], check=True)
                continue
            elif os.path.exists(os.path.join(target_path, ".svn")):
                print(f"Updating existing svn repo {url} in {target_path}...")
                subprocess.run(["svn", "update", target_path], check=True)
                continue

        if "townlong-yak.com" in url or url.endswith(".git") or "github.com" in url:
            print(f"Cloning git repo {url} into {target_path}...")
            git_clone_cmd = ["git", "clone", url, target_path]
            if branch and branch.lower() not in ("head", "default"):
                git_clone_cmd.insert(4, "--branch")
                git_clone_cmd.insert(5, branch)
            subprocess.run(git_clone_cmd, check=True)
        else:
            print(f"Checking out svn repo {url} into {target_path}...")
            subprocess.run(["svn", "checkout", url, target_path], check=True)

    print("All libraries fetched or updated successfully.")
