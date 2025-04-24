# WAStudio/get_wa.py

import os
import subprocess

def ensure_wa_repo(repo_path="./WeakAuras2"):
    if not os.path.exists(repo_path):
        print("Cloning WeakAuras2 repository...")
        subprocess.run(["git", "clone", "https://github.com/WeakAuras/WeakAuras2.git", repo_path], check=True)
    else:
        print("WeakAuras2 repository already exists. Pulling latest changes...")
        subprocess.run(["git", "-C", repo_path, "pull"], check=True)

    print("WeakAuras2 is up to date.")

# Example direct usage
if __name__ == "__main__":
    ensure_wa_repo()
