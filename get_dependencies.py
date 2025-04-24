# WAStudio/get_dependencies.py

import os
import subprocess

def ensure_repo(repo_url, clone_path):
    if not os.path.exists(clone_path):
        print(f"Cloning {repo_url} into {clone_path}...")
        subprocess.run(["git", "clone", repo_url, clone_path], check=True)
    else:
        print(f"{clone_path} already exists. Pulling latest changes...")
        subprocess.run(["git", "-C", clone_path, "pull"], check=True)

def ensure_wa_repo():
    ensure_repo("https://github.com/WeakAuras/WeakAuras2.git", "./WeakAuras2")

def ensure_wase_repo():
    ensure_repo("https://github.com/WAStudios/WASEngine.git", "./WASEngine")
