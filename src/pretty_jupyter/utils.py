import copy


def merge_dict(main_dict: dict, other_dict: dict):
    """
    Updates main dictionary with other dictionary recursively.

    Args:
        main_dict (dict): Main dictionary.
        other_dict (dict): Other dictionary.
    """
    main_dict = copy.deepcopy(main_dict)
    other_dict = copy.deepcopy(other_dict)

    other_dict = _update_dict(other_dict, main_dict)

    return other_dict

def _update_dict(dict_, override_dict):
    for key, val in override_dict.items():
        if isinstance(val, dict):
            dict_[key] = _update_dict(dict_.get(key, {}), val)
        else:
            dict_[key] = val
    return dict_
