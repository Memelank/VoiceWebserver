import os
import time
from io import StringIO
from typing import Union, Tuple

import torch
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess
from whisper.utils import ResultWriter, WriteJSON, WriteSRT, WriteTSV, WriteTXT, WriteVTT

from app.asr_models.asr_model import ASRModel
from app.config import CONFIG


class SenseVoiceEngine(ASRModel):
    """
    SenseVoice ASR engine implementation.
    """

    def __init__(self):
        super().__init__()
        self.model_name = CONFIG.SENSEVOICE_MODEL

    def load_model(self):
        """
        Loads the SenseVoice model.
        """
        with self.model_lock:
            if self.model is None:
                self.model = AutoModel(
                    model=self.model_name,
                    trust_remote_code=True,
                    remote_code="./model.py",
                    vad_model="fsmn-vad",
                    vad_kwargs={"max_single_segment_time": 30000},
                    device=CONFIG.DEVICE,
                )
                self.last_activity_time = time.time()

    def transcribe(
        self,
        audio,
        task: Union[str, None],
        language: Union[str, None],
        initial_prompt: Union[str, None],
        vad_filter: Union[bool, None],
        word_timestamps: Union[bool, None],
        options: Union[dict, None],
        output,
    ):
        """
        Perform transcription using SenseVoice.
        """
        self.load_model()
        self.last_activity_time = time.time()

        # 设置语言，如果未指定则自动检测
        if language is None:
            language = "auto"

        # 执行转录
        result = self.model.generate(
            input=audio,
            cache={},
            language=language,  # "zh", "en", "yue", "ja", "ko", "nospeech"
            use_itn=True,
            batch_size_s=60,
            merge_vad=True,
            merge_length_s=15,
        )

        # 处理输出
        if isinstance(result, list):
            text = rich_transcription_postprocess(result[0]["text"])
            detected_language = result[0].get("language", "unknown")
        else:
            text = rich_transcription_postprocess(result["text"])
            detected_language = result.get("language", "unknown")


        # 构建结果字典，确保格式与 ResultWriter 期望的一致
        result_dict = {
            "text": text,
            "segments": [{
                "text": text,
                "start": 0.0,
                "end": 0.0,
                "words": []
            }],
            "language": detected_language if language == "auto" else language
        }

        # 创建输出文件
        output_file = StringIO()
        self.write_result(result_dict, output_file, output)
        output_file.seek(0)

        return output_file

    def write_result(self, result: dict, file: StringIO, output: Union[str, None]):
        """
        Write the transcription result to the specified output format.
        """
        options = {
            "max_line_width": CONFIG.SUBTITLE_MAX_LINE_WIDTH,
            "max_line_count": CONFIG.SUBTITLE_MAX_LINE_COUNT,
            "highlight_words": CONFIG.SUBTITLE_HIGHLIGHT_WORDS
        }
        
        if output == "srt":
            WriteSRT(ResultWriter).write_result(result, file=file, options=options)
        elif output == "vtt":
            WriteVTT(ResultWriter).write_result(result, file=file, options=options)
        elif output == "tsv":
            WriteTSV(ResultWriter).write_result(result, file=file, options=options)
        elif output == "json":
            WriteJSON(ResultWriter).write_result(result, file=file, options=options)
        else:
            WriteTXT(ResultWriter).write_result(result, file=file, options=options)

    def language_detection(self, audio) -> Tuple[str, float]:
        """
        Perform language detection using SenseVoice.
        Returns a tuple of (language_code, confidence).
        """
        self.load_model()
        self.last_activity_time = time.time()

        # 使用 SenseVoice 进行语言检测
        result = self.model.generate(
            input=audio,
            cache={},
            language="auto",
            use_itn=False,
            batch_size_s=60,
            merge_vad=True,
            merge_length_s=15,
        )

        # 返回检测到的语言代码和置信度
        if isinstance(result, list):
            return result[0].get("language", "unknown"), 1.0
        return result.get("language", "unknown"), 1.0 