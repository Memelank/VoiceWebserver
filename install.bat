@echo off
SET "PYTHON_FOUND="

:: 检查是否已安装 python3 并添加到 PATH
where /Q python3
IF %ERRORLEVEL% EQU 0 (
    echo 检测到已安装 Python。
    SET "PYTHON_FOUND=true"
) ELSE (
    echo 未检测到 Python。尝试使用 winget 安装...
    :: 尝试使用 winget 安装 Python 3
    winget install Python.Python.3 -e --accept-package-agreements --accept-source-agreements
    IF %ERRORLEVEL% EQU 0 (
        echo 使用 winget 安装 Python 成功。
        SET "PYTHON_FOUND=true"
        :: 可能需要刷新环境变量或重启命令行，这里假设安装程序会处理PATH
    ) ELSE (
        echo 使用 winget 安装 Python 失败或 winget 未找到。
        echo 请手动安装 Python 3 (推荐从 Microsoft Store 或 python.org 下载安装器)，或确保系统已安装 winget 并重试。
        SET "PYTHON_FOUND="
    )
)

:: 检查是否找到了 Python 环境，如果没找到则退出
IF NOT DEFINED PYTHON_FOUND (
    echo 未找到可用的 Python 环境，无法继续。
    pause
    exit /b 1
)

:: 确保安装的 Python 环境中的 pip3 可用
where /Q pip3
IF %ERRORLEVEL% NEQ 0 (
    echo 未找到 pip3。请检查 Python 安装。
    pause
    exit /b %ERRORLEVEL%)

:: 安装 poetry
pip3 install poetry
IF %ERRORLEVEL% NEQ 0 (
    echo poetry 安装失败。
    pause
    exit /b %ERRORLEVEL%)

:: 安装项目依赖
poetry install
IF %ERRORLEVEL% NEQ 0 (
    echo 项目依赖安装失败。
    pause
    exit /b %ERRORLEVEL%)

echo 部署完成。
pause 