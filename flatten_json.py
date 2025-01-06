from typing import List, Dict
import json


def json_flatten(json_file_path: str, keys: List[str], output_file_path: str) -> bool:
    """
    Function to extract the values from a nested JSON, and write a flattened JSON file with
    only the required keys paths and their values

    :param json_file_path: File path to read nested JSON from (e.g. product_example.json)
    :param keys: A list of json key paths to be flattened
    :param output_file_path: File path to write flattened JSON to (e.g. example_output.json)
    :return: True if successful, otherwise False
    """
    try:
        with open(json_file_path, 'r') as infile:
            data = json.load(infile)

        # check as a file can be a valid JSON, but not contain key-value pair
        # confirm on what structures we expect - only a nested JSON obj or can it also be an JSON array of objects
        if isinstance(data, dict):
            flat_data = {}
            for key_path in keys:
                key_list = key_path.split(".")
                key_path_value = get_nested_value(key_list, data)
                if key_path_value:
                    flat_data[key_path] = key_path_value
                else:
                    print(f"The key path was not found.")
                    return False

            with open(output_file_path, "w") as outfile:
                json.dump(flat_data, outfile)

            print("Run is successful!")
            return True

        else:
            print(f"Error 1: Expected the JSON to contain key-value pairs, but got {type(data).__name__}.")
            return False

    except Exception as e:
        print(f"Error: {e}")
        return False


def get_nested_value(key_list: List, data: Dict):
    """
    Function to extract the value at the end of the key path

    :param key_list: File path to read nested JSON from
    :param data: initial product data to search for key path in
    :return: the value at the end of the key path
    """
    value = data
    for key in key_list:

        # if the value is a dict - find the key and take its value
        if isinstance(value, dict):
            value = value.get(key, None)
            # if the key is not present, return None
            if value is None:
                return None

        # if the value is a list - find the first dictionary that contains the key and take its value
        elif isinstance(value, list):
            value = next((item.get(key, None) for item in value if isinstance(item, dict)), None)
            if value is None:
                return None

        # the value is not a list or a dict, but we have more keys to search for -> key doesn't exist
        else:
            return None
    return value


with open("JSON/example_argument.json", 'r') as f:
    keys = json.load(f)
    # print(type(keys))

json_flatten("JSON/product_example.json", keys, "JSON/flattened_product_output.json")
