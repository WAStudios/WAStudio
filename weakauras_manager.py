import os
import subprocess
import shutil

GITHUB_URL = "https://github.com/WeakAuras/WeakAuras2.git"
TARGET_DIR = "WeakAuras2"

def is_git_repo(path):
    return os.path.isdir(os.path.join(path, ".git"))

def clone_or_update_weakauras():
    if not os.path.exists(TARGET_DIR):
        print("WeakAuras2 not found. Cloning from GitHub...")
        subprocess.run(["git", "clone", GITHUB_URL, TARGET_DIR])
    elif is_git_repo(TARGET_DIR):
        print("WeakAuras2 found. Pulling latest changes...")
        subprocess.run(["git", "-C", TARGET_DIR, "pull", "origin", "main"])
    else:
        print("Error: WeakAuras2 folder exists but is not a git repo.")
        print("Deleting and re-cloning...")
        shutil.rmtree(TARGET_DIR)
        subprocess.run(["git", "clone", GITHUB_URL, TARGET_DIR])

if __name__ == "__main__":
    clone_or_update_weakauras()