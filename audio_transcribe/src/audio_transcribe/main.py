# import this will cause the below error:
# zsh: segmentation fault  /Users/birudo/.venv/subai/bin/python
# /usr/local/Cellar/python@3.11/3.11.5/Frameworks/Python.framework/Versions/3.11/lib/python3.11/multiprocessing/resource_tracker.py:224: UserWarning: resource_tracker: There appear to be 1 leaked semaphore objects to clean up at shutdown
#   warnings.warn('resource_tracker: There appear to be %d '

# from subsai import SubsAI, Tools

import json
from pathlib import Path
import logging
from typing import Literal
from .transcribe import transcribe_by_whisper_ctranslate2_cli
from .translate import translate_by_whisper_ctranslate2_cli
import time
import os
import ffmpeg
from .utils import get_sub_stem_name, recursive_merge
import pysubs2, json
from .detect_language import detect_language

proxy = "http://127.0.0.1:7890"
os.environ["http_proxy"] = proxy
os.environ["all_proxy"] = proxy
os.environ["https_proxy"] = proxy


def is_translated(file: Path, model_type: str) -> bool:
    if not file.is_file():
        return False

    srt_file_name = f"{get_translated_stem_name(file=file,model_type=model_type)}.json"
    srt_file_path = file.parent / srt_file_name

    return Path(srt_file_path).exists()


def get_translated_stem_name(file: Path, model_type: str) -> str:
    return f"{get_sub_stem_name(file, model_type)}_en"


def is_transcribed(file: Path, model_type: str):
    if not file.is_file():
        return False

    srt_file_name = f"{get_sub_stem_name(file, model_type)}.json"
    srt_file_path = file.parent / srt_file_name

    return Path(srt_file_path).exists()


def iterate_audio_files_recursively(dir_path: Path):
    audio_extensions = {".mp3", ".wav", ".mp4", ".ogg", ".flac", ".aac", ".mkv"}
    audio_files = dir_path.glob("**/*")
    audio_files = filter(lambda file: file.suffix in audio_extensions, audio_files)
    yield from audio_files


def log_execute_time(
    audio_file: Path,
    output_name: str,
    executed_time: float,
    log_file: Path,
    model_type: str,
    threads: int,
):
    audio_duration = float(
        ffmpeg.probe(str(audio_file.resolve()))["format"]["duration"]
    )

    # Read file.
    try:
        with open(log_file, "rt+") as file:
            if len(log_file.read_text()) == 0:
                dict = {}
            else:
                dict = json.load(file)
    except IOError:
        print("Could not read file, starting from scratch")
        dict = {}

    # Save file.
    with open(log_file, "wt") as f:
        merged_dict = recursive_merge(
            dict,
            {
                f"{ output_name }_threads_{threads}": {
                    "model_type": model_type,
                    "executed_time": executed_time,
                    "audio_duration": audio_duration,
                    "relative_speed": audio_duration / executed_time,
                    "thread": threads,
                },
            },
        )

        json.dump(merged_dict, f, indent=2)


def get_non_word_level_subtitle_name(stem: str):
    return f"{ stem }_non_word_level"


# def is_generate_line_level_subtitles():
#     get_non_word_level_subtitle_name(whisper_json_file.stem)


def generate_line_level_subtitles(whisper_json_file: Path, output_dir: Path):
    if not whisper_json_file.exists():
        return

    with open(whisper_json_file, encoding="utf-8") as file:
        sub_dict = json.load(file)
        subs = pysubs2.load_from_whisper(sub_dict)
        file = output_dir / Path(
            get_non_word_level_subtitle_name(whisper_json_file.stem)
        )
        print(str(file))
        subs.save(f"{str(file)}.srt")
        return file


def main(threads: int, model_type: Literal["large-v2", "tiny"], target_dir: Path):
    if not target_dir.is_dir():
        logging.error(f"{target_dir.resolve()} does not exist.")

    transcribed_count_in_current_session = 0
    all_transcribed_transcribed_count = 0

    for audio_file in iterate_audio_files_recursively(target_dir):
        audio_file = audio_file.resolve()
        language = detect_language(audio_path=audio_file)
        print(f"Detected language: {language}")

        translated_stem_name = get_sub_stem_name(audio_file, model_type)
        output_dir = audio_file.parent
        if not is_transcribed(file=audio_file, model_type=model_type):
            print(f"Transcribing: {audio_file}")
            print(
                f"Transcribed files in current session: {transcribed_count_in_current_session}"
            )
            print(f"All transcribed files: {all_transcribed_transcribed_count}")
            print(
                f"Remain files amount: {len(list(iterate_audio_files_recursively(target_dir)))-all_transcribed_transcribed_count}"
            )

            start = time.time()
            transcribe_by_whisper_ctranslate2_cli(
                audio_path=audio_file,
                output_dir=output_dir,
                model_type=model_type,
                output_name=translated_stem_name,
                threads=threads,
                language=language,
                initial_prompt="日本語では、文の末尾に「。」を使って文章を終わらせます。また、カンマ「、」を使って文中の要素を区切ります。疑問文の場合は「？」を使用し、驚きや強調を表す場合には「！」を使います。引用文では、「」を使用します。括弧は（）や『』を使い、読点の代わりに「…」を使用することもあります。それに加えて、コロン「：」やセミコロン「；」も使用されます。以上のように、日本語では様々な句読点を使って文章を表現します。"
                if language == "ja"
                else "",
            )

            end = time.time()
            executed_time = end - start
            log_file = target_dir / "transcribe_execute_time_log.json"

            if executed_time > 0:
                log_execute_time(
                    audio_file=audio_file,
                    output_name=translated_stem_name,
                    executed_time=executed_time,
                    log_file=log_file,
                    model_type=model_type,
                    threads=threads,
                )

            transcribed_count_in_current_session = (
                transcribed_count_in_current_session + 1
            )

        else:
            all_transcribed_transcribed_count = all_transcribed_transcribed_count + 1
            print(f"Skip already transcribed file: {audio_file}.")
        generate_line_level_subtitles(
            output_dir=output_dir,
            whisper_json_file=output_dir / f"{translated_stem_name}.json",
        )

        if not is_translated(file=audio_file, model_type=model_type):
            translated_stem_name = get_translated_stem_name(
                audio_file, model_type=model_type
            )

            print(f"Translating: {audio_file}")
            translate_by_whisper_ctranslate2_cli(
                audio_path=audio_file,
                output_dir=output_dir,
                output_name=translated_stem_name,
                threads=threads,
                model_type=model_type,
            )

        generate_line_level_subtitles(
            output_dir=output_dir,
            whisper_json_file=output_dir / f"{translated_stem_name}.json",
        )
