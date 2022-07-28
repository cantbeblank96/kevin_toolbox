from kevin.data_flow.file import json_


def test_json():
    print("test file.json_")
    content = [{123: 123, -1: -1, 1.23: 1.23, -1.000: -1.0, "1.2.3": None}]
    file_path = "./test_data/temp/data_0.json"
    json_.write(content=content, file_path=file_path)
    content1 = json_.read(file_path=file_path, converters=[json_.converter.convert_dict_key_to_number])
    assert content == content1
