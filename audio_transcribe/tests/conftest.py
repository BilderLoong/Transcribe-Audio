from pathlib import Path
import pytest
import shutil

audio_fixtures_template_dir = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="function")
def audio_dir(tmp_path_factory):
    dir = tmp_path_factory.mktemp("audio_dir")
    yield shutil.copytree(audio_fixtures_template_dir, dir, dirs_exist_ok=True)

    shutil.rmtree(dir)