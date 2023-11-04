from pathlib import Path
from audio_transcribe.main import main
from audio_transcribe.transcribe import transcribe_by_whisper_ctranslate2_cli

# main(32, "large-v2", Path(r"D:\OneDrive - hdu.edu.cn\Audio book"))
# main(32, "large-v2", Path(r"D:\Video\Hanzawa Naoki (2013) 1080p-MED"))
main(32, "large-v2", Path(r"D:\Video\Hanzawa Naoki (2013) 1080p-MED"))
# main(32, "large-v2", Path(r"D:\Sync\Boox Max Lumi\Audio book\scripts\audio_transcribe\tests\fixtures\one_file"))
