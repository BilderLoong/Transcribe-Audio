import os
from pathlib import Path
import subprocess
from typing import Literal


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


def translate_by_whisper_ctranslate2_cli(
    audio_path: Path,
    output_dir: Path,
    output_name: str,
    model_type: Literal["large-v2", "tiny"],
    device: Literal["auto", "cpu"] = "auto",
    threads: int = 0,
    language="",
    initial_prompt="",
):
    args = [
        "whisper-ctranslate2",
        "--model",
        model_type,
        "--highlight_words",
        "True",
        "--pretty_json",
        "True",
        "--print_colors",
        "True",
        "--word_timestamp",
        "True",
        "--threads",
        str(threads),
        "--output_dir",
        output_dir,
        "--task",
        "translate",
        audio_path,
    ]
    if language:
        args.extend(["--language", language])

    if initial_prompt:
        args.extend(
            [
                "--initial_prompt",
                initial_prompt,
            ]
        )

    process = subprocess.run(args=args)
    # whisper-ctranslate2 --print_colors True  --language ja --threads 32 --word_timestamp True --model large-v2 --verbose True  --highlight_words True --max_line_width 13 --max_line_count 13  --initial_prompt "、 。 ！ ？ 「」 （） ［］ ｛｝ 【】 ・ … ゠" "test_1_min.mp3"
    # ffmpeg -i "銃・病原菌・鉄 上/003 - 銃・病原菌・鉄 上.mp3" -t 00:01:00 -acodec copy test_1_min.mp3

    rename_output_files(audio_path, output_name)

    return process.returncode
