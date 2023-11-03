from pathlib import Path
import timeit

import ffmpeg
print(ffmpeg.probe('../test_fixture/tests_data_stereo_diarization.wav')['format']['duration'])


print(__file__)
print(str((Path(__file__) / "..").resolve()))





def recursive_merge(*dicts):
    merged_dict = {}
    for dictionary in dicts:
        for key, value in dictionary.items():
            if key in merged_dict and isinstance(merged_dict[key], dict) and isinstance(value, dict):
                merged_dict[key] = recursive_merge(merged_dict[key], value)
            else:
                merged_dict[key] = value
    return merged_dict

# Example dictionaries
dict1 = {'key1': 'value1', 'key2': {'nested_key1': 'nested_value1'}}
dict2 = {'key2': {'nested_key2': 'nested_value2'}, 'key3': 'value3'}
dict3 = {'key2': {'nested_key3': 'nested_value3'}, 'key4': 'value4'}

merged = recursive_merge(dict1, dict2, dict3)
print(eval("{'tests_data_stereo_diarization_tiny': {'model_type': 'tiny', 'executed_time': 2.5287423133850098, 'audio_duration': 5.0, 'relative_speed': 1.9772675031118256, 'thread': 0}}"))

print(merged)
