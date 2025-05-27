
![Licence](https://img.shields.io/github/license/ahmetoner/whisper-asr-webservice.svg)

# VoiceWebserver

VoiceWebserver 是一个通用的语音工具包。基于[Whisper ASR Box](https://github.com/ahmetoner/whisper-asr-webservice)开发。

## 特性

当前版本支持以下语音识别引擎：

- [openai/whisper](https://github.com/openai/whisper)@[v20240930](https://github.com/openai/whisper/releases/tag/v20240930)
- [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper)@[v1.1.0](https://github.com/SYSTRAN/faster-whisper/releases/tag/v1.1.0)
- [whisperX](https://github.com/m-bain/whisperX)@[v3.3.0](https://github.com/m-bain/whisperX/releases/tag/v3.3.0)
- [SenseVoice](https://github.com/iic/SenseVoice) - 支持中文语音识别

## 快速开始

### 使用 Poetry 安装
默认使用GPU
```shell
# 安装 poetry（如果尚未安装）
pip3 install poetry

# 安装依赖
poetry install

# 运行服务
#   whisper
ASR_DEVICE=cuda poetry run whisper-asr-webservice --host 0.0.0.0 --port 9000
#   sensevoice
ASR_ENGINE=sensevoice ASR_DEVICE=cuda poetry run whisper-asr-webservice --host 0.0.0.0 --port 9000
```

### 使用 Docker（未测试）

#### CPU 版本

```shell
docker run -d -p 9000:9000 \
  -e ASR_MODEL=base \
  -e ASR_ENGINE=openai_whisper \
  onerahmet/openai-whisper-asr-webservice:latest
```

#### GPU 版本

```shell
docker run -d --gpus all -p 9000:9000 \
  -e ASR_MODEL=base \
  -e ASR_ENGINE=openai_whisper \
  onerahmet/openai-whisper-asr-webservice:latest-gpu
```


## 主要特性

- 支持多种 ASR 引擎（OpenAI Whisper、Faster Whisper、WhisperX、SenseVoice）
- 支持多种输出格式（文本、JSON、VTT、SRT、TSV）
- 支持词级时间戳
- 支持语音活动检测（VAD）过滤
- 支持说话人分离（使用 WhisperX）
- 集成 FFmpeg 支持多种音频/视频格式
- 支持 GPU 加速
- 可配置的模型加载/卸载
- REST API 和 Swagger 文档

## 环境变量配置

主要配置选项：

- `ASR_ENGINE`: 引擎选择（openai_whisper, faster_whisper, whisperx, sensevoice）
- `ASR_MODEL`: 模型选择（tiny, base, small, medium, large-v3 等）
- `ASR_MODEL_PATH`: 自定义模型存储/加载路径
- `ASR_DEVICE`: 设备选择（cuda, cpu）
- `MODEL_IDLE_TIMEOUT`: 模型卸载超时时间
- `SENSEVOICE_MODEL`: SenseVoice 模型名称（默认为 "iic/SenseVoiceSmall"）
- `SENSEVOICE_MODEL_REVISION`: SenseVoice 模型版本（默认为 "v1.0.0"）

## 开发

启动服务后，访问 `http://localhost:9000` 或 `http://0.0.0.0:9000` 查看 Swagger UI 文档并测试 API 端点。

## 致谢

- 本项目使用了 [FFmpeg](http://ffmpeg.org) 项目的库，遵循 [LGPLv2.1](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html) 许可
