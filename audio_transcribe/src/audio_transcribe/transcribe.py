import subprocess
from typing import Literal
from src.whisper_ctranslate2 import writers
from src.whisper_ctranslate2.transcribe import Transcribe, TranscriptionOptions
from pathlib import Path
import os
from .utils import get_sub_stem_name

proxy = "http://127.0.0.1:7890"
os.environ["http_proxy"] = proxy
os.environ["all_proxy"] = proxy
os.environ["https_proxy"] = proxy


default_asr_options = TranscriptionOptions(
    beam_size=5,
    best_of=5,
    patience=1.0,
    length_penalty=1.0,
    repetition_penalty=1.0,
    no_repeat_ngram_size=0,
    log_prob_threshold=-1.0,
    no_speech_threshold=0.6,
    compression_ratio_threshold=2.4,
    condition_on_previous_text=True,
    prompt_reset_on_temperature=0,
    temperature=(0.0, 0.2, 0.4, 0.6000000000000001, 0.8, 1.0),
    initial_prompt=None,
    suppress_blank=True,
    suppress_tokens=[-1],
    word_timestamps=False,
    print_colors=False,
    prepend_punctuations="\"'“¿([{-",
    append_punctuations="\"'.。,，!！?？:：”)]}、",
    vad_filter=False,
    vad_threshold=None,
    vad_min_speech_duration_ms=None,
    vad_max_speech_duration_s=None,
    vad_min_silence_duration_ms=None,
)


def transcribe(
    audio_path: Path,
    output_dir: Path,
    output_name: str,
    model_type: Literal["large-v2", "tiny"],
    device: Literal["auto", "cpu"] = "auto",
    threads=0,
):
    result = Transcribe(
        device=device,
        model_path=model_type,
        device_index=0,
        compute_type="auto",
        threads=threads,
        cache_directory=None,
        local_files_only=False,
    ).inference(
        audio=str(audio_path),
        task="transcribe",
        language=None,
        verbose=True,
        live=False,
        options=default_asr_options,
    )

    print("output_dir", str(output_dir))
    writer = writers.get_writer("all", str(output_dir))
    print("output_name", str(output_name))

    writer(
        result,
        # use a faked extension name.
        f"{output_name}.mp3",
        {
            "highlight_words": True,
            "max_line_count": None,
            "max_line_width": None,
            "pretty_json": True,
        },
    )


def transcribe_by_whisper_ctranslate2_cli(
    audio_path: Path,
    output_dir: Path,
    output_name: str,
    model_type: Literal["large-v2", "tiny"],
    language: str = "",
    initial_prompt="",
    device: Literal["auto", "cpu"] = "auto",
    threads: int = 0,
    word_timestamp: bool = True,
):
    args = [
        "whisper-ctranslate2",
        "--model",
        model_type,
        # "--max_line_width",
        # "15",
        # "--max_line_count",
        # "15",
        "--highlight_words",
        "True",
        "--pretty_json",
        "True",
        "--print_colors",
        "True",
        "--threads",
        str(threads),
        "--output_dir",
        output_dir,
        audio_path,
    ]

    if word_timestamp:
        print(f"Using word_timestamp when transcribing.")
        args.extend(
            [
                "--word_timestamp",
                "True",
            ]
        )

    if initial_prompt:
        print(f"Using initial_prompt:{initial_prompt} when transcribing.")
        args.extend(
            [
                "--initial_prompt",
                initial_prompt,
            ]
        )

    if language:
        args.extend(["--language", language])

    print(f"Transcribe command args: {args}")
    process = subprocess.run(args)
    # whisper-ctranslate2 --print_colors True  --language ja --threads 32 --word_timestamp True --model large-v2 --verbose True  --highlight_words True --max_line_width 13 --max_line_count 13  --initial_prompt "、 。 ！ ？ 「」 （） ［］ ｛｝ 【】 ・ … ゠" "test_1_min.mp3"
    # ffmpeg -i "銃・病原菌・鉄 上/003 - 銃・病原菌・鉄 上.mp3" -t 00:01:00 -acodec copy test_1_min.mp3

    rename_output_files(audio_path, output_name)

    return process.returncode


def rename_output_files(audio_path: Path, target_name: str):
    for i in ["json", "srt", "tsv", "vtt", "txt"]:
        stem = audio_path.stem
        dir = audio_path.parent
        source = dir / f"{stem}.{i}"
        target = dir / f"{target_name}.{i}"
        if source.is_file():
            # async may cause race condition.
            # source.rename(target)

            os.rename(source, target)


# """
#  Simple test
# """
# audio_path = (
#     Path(__file__).parent.parent / "test_fixture" / "tests_data_stereo_diarization.wav"
# )
# output_dir = audio_path.parent
# model_type = "tiny"

# import time


# for i in range(1, 3):
#     start = time.time()
#     transcribe(
#         audio_path,
#         output_dir,
#         get_sub_stem_name(file=audio_path, model_type=model_type),
#         model_type=model_type,
#     )
#     end = time.time()
#     print(end - start)
