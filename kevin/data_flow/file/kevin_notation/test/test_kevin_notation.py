import pytest
from kevin.patches.for_test import check_consistency

import os
import numpy as np

from kevin.data_flow.file import kevin_notation
from kevin.data_flow.file.kevin_notation.test.test_data.data_all import metadata_ls, content_ls, file_path_ls


@pytest.mark.parametrize("expected_metadata, expected_content, file_path",
                         zip(metadata_ls, content_ls, file_path_ls))
def test_reader(expected_metadata, expected_content, file_path):
    print("test Reader")

    # 读取
    chunk_size = np.random.randint(1, 10)
    with kevin_notation.Reader(file_path=file_path, chunk_size=chunk_size) as reader:
        # metadata
        print(reader.metadata)
        check_consistency(expected_metadata, reader.metadata)
        # content
        content = next(reader)
        for chunk in reader:
            for key in content.keys():
                content[key].extend(chunk[key])
        print(content)
        check_consistency(expected_content, content)


@pytest.mark.parametrize("expected_metadata, expected_content, file_path",
                         zip(metadata_ls, content_ls, file_path_ls))
def test_writer(expected_metadata, expected_content, file_path):
    print("test Writer")

    # 新建
    file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "test_data/temp",
                             os.path.basename(file_path))
    part = np.random.randint(1, 5)
    values = list(zip(*[expected_content[key][:-part] for key in expected_metadata["column_name"]]))
    with kevin_notation.Writer(file_path=file_path, mode="w", sep=expected_metadata["sep"]) as writer:
        writer.metadata_begin()
        for key, value in expected_metadata.items():
            if key == "sep":
                pass
            elif key == "column_name":
                writer.column_name = value
            elif key == "column_type":
                # 尝试使用局部指定的 sep
                writer.column_type = {"value": value, "sep": " "}
            else:
                writer.write_metadata(key, value)
        writer.metadata_end()

        writer.contents_begin()
        writer.contents = values
        writer.contents_end()

    # 续写
    values = list(zip(*[expected_content[key][-part:] for key in expected_metadata["column_name"]]))
    with kevin_notation.Writer(file_path=file_path, mode="a") as writer:
        writer.contents = values
        writer.contents_end()

    # 检验
    with kevin_notation.Reader(file_path=file_path, chunk_size=1000) as reader:
        # metadata
        check_consistency(expected_metadata, reader.metadata)
        # content
        content = next(reader)
        check_consistency(expected_content, content)