import os
import subprocess
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
ENV_DIR = os.path.join(PROJECT_ROOT, "99_virtual_environments", "rag-env")
PYTHON_EXEC = sys.executable


def run_command(cmd):
    print(f"Running: {cmd}")
    subprocess.check_call(cmd, shell=True)


def create_venv():
    if os.path.exists(ENV_DIR):
        print("Virtual environment already exists")
    else:
        print("Creating virtual environment at:")
        print(f" {ENV_DIR}")
        run_command(f"{PYTHON_EXEC} -m venv \"{ENV_DIR}\"")


def install_dependencies():
    print("Installing dependencies...")

    python_path = os.path.join(ENV_DIR, "Scripts", "python.exe")

    run_command(f"\"{python_path}\" -m pip install --upgrade pip")

    run_command(
        f"\"{python_path}\" -m pip install "
        "langchain "
        "langchain-community "
        "chromadb "
        "sentence-transformers "
        "pypdf "
        "openai"
    )


def main():
    print("===================================")
    print("🚀 RAG ENV SETUP STARTED")
    print("===================================")

    create_venv()
    install_dependencies()

    print("\nSetup complete!")
    print(f"Env location: {ENV_DIR}")

    activate_path = os.path.join(ENV_DIR, "Scripts", "activate")
    print("\nTo activate:")
    print(f"{activate_path}")


if __name__ == "__main__":
    main()