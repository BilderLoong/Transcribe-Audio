from pathlib import Path
from audio_transcribe.dir_meta import (
    get_json_dict,
    write_dict_to_json,
    save_file_meta,
    get_file_meta,
    DIR_META_FILE_NAME,
)


def test_dir_meat(tmp_path: Path):
    dict = {"a": "av"}
    file_path = tmp_path / "foo.mp3"
    save_file_meta(file=file_path, data=dict)

    assert (tmp_path / DIR_META_FILE_NAME).exists()

    assert get_file_meta(file_path) == dict
    assert get_json_dict(tmp_path / DIR_META_FILE_NAME) == {"foo.mp3": dict}


def test_write_and_get_dict_to_json(tmp_path: Path):
    dict = {"a": "av"}
    file_path = tmp_path / "dir_meta.json"
    write_dict_to_json(dict=dict, filename=file_path)

    assert file_path.exists()

    dict_res = get_json_dict(file_path)
    assert dict == dict_res
