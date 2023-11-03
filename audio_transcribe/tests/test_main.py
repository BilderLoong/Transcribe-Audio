from pathlib import Path
import shutil
from audio_transcribe.utils import get_sub_stem_name
from audio_transcribe.main import main
import pytest


@pytest.fixture(scope="module")
def one_audio_dir(audio_dir, tmp_path_factory):
    dir = tmp_path_factory.mktemp("one_audio_dir")
    yield shutil.copytree(Path(audio_dir) / "one_file", dir, dirs_exist_ok=True)
    shutil.rmtree(dir)


def test_main_for_one_audio_file(audio_dir: Path, tmp_path: Path):
    model_type = "tiny"
    threads = 16
    target_dir = audio_dir / "one_file"

    main(threads=threads, model_type=model_type, target_dir=target_dir)

    assert (
        target_dir / f"{get_sub_stem_name(target_dir / 'test_1.wav', model_type)}.srt"
    ).exists
    assert (
        target_dir / f"{get_sub_stem_name(target_dir / 'test_1.wav', model_type)}.json"
    ).exists


def test_main_skip_already_translate_file(audio_dir: Path, tmp_path: Path):
    pass


# test_main()


# def run_main():
#     # model_type = "tiny"
#     threads = 16
#     model_type = "large-v2"
#     # target_dir = Path.cwd()
#     target_dir = Path(r"D:\Sync\Boox Max Lumi\Audio book")

#     main(threads=threads, model_type=model_type, target_dir=target_dir)


# run_main()
