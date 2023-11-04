import shutil
from audio_transcribe.detect_language import detect_language
from pathlib import Path
from audio_transcribe.utils import get_sub_stem_name
import pytest


# @pytest.fixture(scope="module")
# def one_audio_dir(audio_dir, tmp_path_factory):
#     dir = tmp_path_factory.mktemp("one_audio_dir")
#     yield shutil.copytree(Path(audio_dir) / "one_file", dir, dirs_exist_ok=True)
#     shutil.rmtree(dir)


def test_detect_language(audio_dir: Path):
    audio_path = audio_dir / "one_file" / "test_1.wav"
    language = detect_language(audio_path=audio_path)
    assert language == "en"
