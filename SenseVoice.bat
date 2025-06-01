@SET ASR_ENGINE=sensevoice
@SET ASR_DEVICE=cuda

poetry run whisper-asr-webservice --host 0.0.0.0 --port 9000

pause