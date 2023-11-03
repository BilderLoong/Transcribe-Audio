from pathlib import Path


def get_sub_stem_name(file: Path, model_type: str):
    """
    @param file audio file path.
    """
    return f"{file.stem}_{model_type}"


def recursive_merge(*dicts):
    merged_dict = {}
    for dictionary in dicts:
        for key, value in dictionary.items():
            if (
                key in merged_dict
                and isinstance(merged_dict[key], dict)
                and isinstance(value, dict)
            ):
                merged_dict[key] = recursive_merge(merged_dict[key], value)
            else:
                merged_dict[key] = value
    return merged_dict
