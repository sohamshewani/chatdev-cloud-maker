import os
import random
import subprocess
import time
from pathlib import Path

GH_USER = os.environ.get("GITHUB_ACTOR", "sohamshewani")

IDEAS = [
    ("snake-game", "A retro 2D arcade snake game with score tracking and speed scaling in Python"),
    ("calc-engine", "A graphical calculator utility with expression parsing and history storage"),
    ("pomodoro-cli", "A productivity timer with desktop notifications, sound alerts, and task logging"),
    ("markdown-viewer", "A lightweight local markdown previewer with real-time file watching and HTML rendering"),
    ("pass-manager", "A secure local password vault with AES encryption and clipboard copy support")
]

def run(cmd, cwd=None):
    return subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)

def main():
    tag, prompt = random.choice(IDEAS)
    repo_name = f"{tag}-{int(time.time())}"
    print(f"🚀 Initializing ChatDev Multi-Agent Org for: {repo_name}...")

    # Run ChatDev CLI with the selected idea
    cmd = f'python3 run.py --task "{prompt}" --name "{repo_name}"'
    res = run(cmd, cwd=Path("ChatDev"))
    print(res.stdout)

    # Find the generated output directory inside WareHouse
    warehouse = Path("ChatDev/WareHouse")
    matches = list(warehouse.glob(f"*{repo_name}*"))
    if not matches:
        print("⚠️ No output found in ChatDev/WareHouse")
        return

    work_dir = matches[0]
    print(f"📦 Packaging generated agent workspace: {work_dir}")

    (work_dir / ".gitignore").write_text("venv/\n__pycache__/\n*.pyc\n.DS_Store\n", encoding="utf-8")

    # Git sequence
    run("git init", cwd=work_dir)
    run(f"git config user.name '{GH_USER}'", cwd=work_dir)
    run(f"git config user.email '{GH_USER}@users.noreply.github.com'", cwd=work_dir)
    run("git add .", cwd=work_dir)
    run('git commit -m "feat: multi-agent production build engineered by ChatDev"', cwd=work_dir)
    run("git branch -M main", cwd=work_dir)

    # Publish to your GitHub account
    pub = run(
        f'gh repo create "{repo_name}" --public --source=. --remote=origin --description "{prompt}" --push',
        cwd=work_dir
    )

    if pub.returncode == 0:
        print(f"🌟 Successfully shipped multi-agent project: https://github.com/{GH_USER}/{repo_name}")
    else:
        print(f"⚠️ Push failed: {pub.stderr}")

if __name__ == "__main__":
    main()
