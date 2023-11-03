from audio_transcribe import transcribe
from pathlib import Path
from audio_transcribe.utils import get_sub_stem_name


def test_transcribeByCli(audio_dir: Path):
    audio_path = audio_dir / "one_file" / "test_1.wav"
    model_type = "tiny"
    output_name = get_sub_stem_name(audio_path, model_type)

    transcribe.transcribeByCli(
        audio_path=audio_path,
        model_type=model_type,
        output_dir=audio_path.parent,
        output_name=output_name,
    )

    assert (audio_dir / "one_file" / f"{output_name}.srt").exists()
    assert (audio_dir / "one_file" / f"{output_name}.json").exists()
