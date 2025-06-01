::虚拟环境存放路径，可修改
poetry config virtualenvs.path "C:\venvs"

winget install --id Gyan.FFmpeg -e

python -m pip install --upgrade poetry

poetry install --no-cache --sync --no-ansi --no-interaction