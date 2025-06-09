import pytest
import tempfile
import shutil
import os
import time
from file_feature_extractor import File_Feature_Extractor  # 替换为你的实际模块路径


@pytest.fixture
def setup_test_dir():
    # 创建临时目录和两个测试文件
    test_dir = tempfile.mkdtemp()
    file1 = os.path.join(test_dir, "file1.txt")
    file2 = os.path.join(test_dir, "file2.bin")

    with open(file1, 'w') as f:
        f.write("Hello, world!")

    with open(file2, 'wb') as f:
        f.write(os.urandom(2048))

    yield test_dir, file1, file2

    # 清理临时目录
    shutil.rmtree(test_dir)


def test_scan_and_get_result(setup_test_dir):
    test_dir, file1, file2 = setup_test_dir

    extractor = File_Feature_Extractor(
        root_dir=test_dir,
        shallow_size=16,
        include_metadata=True,
        include_shallow_hash=True,
        include_full_hash=True,
        hash_algorithms=('md5', 'sha1')
    )

    extractor.scan()
    result = extractor.get_result()

    assert file1 in result
    assert "metadata" in result[file1]
    assert "shallow_hash" in result[file1]
    assert "hash" in result[file1]


def test_save_and_load_cache(setup_test_dir):
    test_dir, file1, file2 = setup_test_dir

    extractor = File_Feature_Extractor(root_dir=test_dir)
    extractor.scan()

    cache_file = os.path.join(test_dir, "cache.json")
    extractor.save_cache(cache_file)

    new_extractor = File_Feature_Extractor(root_dir=test_dir)
    new_extractor.load_cache(cache_file)
    result = new_extractor.get_result()

    assert file2 in result
    assert "hash" in result[file2]


def test_update_modified_file(setup_test_dir):
    test_dir, file1, _ = setup_test_dir

    extractor = File_Feature_Extractor(root_dir=test_dir)
    extractor.scan()

    old_md5 = extractor.get_result()[file1]["hash"]["md5"]

    time.sleep(1)  # 确保修改时间有变化
    with open(file1, 'w') as f:
        f.write("Modified content!")

    extractor.update()
    new_md5 = extractor.get_result()[file1]["hash"]["md5"]

    assert old_md5 != new_md5


def test_ignore_unchanged_files_on_update(setup_test_dir):
    test_dir, file1, _ = setup_test_dir

    extractor = File_Feature_Extractor(root_dir=test_dir)
    extractor.scan()
    result_before = extractor.get_result()[file1]

    extractor.update()
    result_after = extractor.get_result()[file1]

    assert result_before == result_after
