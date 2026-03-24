

01. Install uv on Windows
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

02. Install Python 3.12
    uv python install 3.12

03. Create virtual environment
    uv venv reachy_mini_env --python 3.12

04. Activate the Env.
    reachy_mini_env\Scripts\activate

05. Install Dependenices
    uv pip install "reachy-mini"
    uv pip install "reachy-mini[mujoco]"
    git lfs install