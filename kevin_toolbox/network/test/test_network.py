import os
import pytest
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.network import get_response, fetch_content, fetch_metadata, download_file
from kevin_toolbox.network.test.test_data.data_0 import set_response

data_dir = os.path.join(os.path.dirname(__file__), "test_data")
temp_dir = os.path.join(os.path.dirname(__file__), "temp")


def test_get_response_success(monkeypatch):
    """
        测试 get_response 在请求成功时的返回结果。
    """
    set_response(monkeypatch, 200, b"OK")

    for stream in [True, False]:
        result = get_response(url="http://example.com", stream=stream, retries=2)
        assert result.data == b"OK"


def test_get_response_failure(monkeypatch):
    """
        测试 get_response 在响应状态码 >= 400 时应抛出异常。
    """
    set_response(monkeypatch, 404, b"Not Found")

    with pytest.raises(Exception) as excinfo:
        get_response(url="http://example.com", stream=False, retries=1)
    assert "HTTP 请求失败" in str(excinfo.value)


def test_fetch_content_0(monkeypatch):
    """
        测试整体读取，支持解码和不解码
    """
    set_response(monkeypatch, 200, b"233")

    for decoding, expected in zip([None, "utf-8"], [b"233", "233"]):
        response = get_response(url="http://example.com", retries=1)
        result = fetch_content(response=response, decoding=decoding)
        check_consistency(result, expected)
        #
        result = fetch_content(url="http://example.com", decoding=decoding)
        check_consistency(result, expected)


def test_fetch_content_1(monkeypatch):
    """
        测试分块读取的情况，即指定 chunk_size 后，返回一个生成器，能逐块读取数据。
    """
    set_response(monkeypatch, 200, b"233" * 15)

    response = get_response(url="http://example.com", retries=1)
    count = 0
    for i in fetch_content(response=response, chunk_size=3):
        check_consistency(i, b"233")
        count += 1
    check_consistency(count, 15)
    #
    count = 0
    for i in fetch_content(url="http://example.com", chunk_size=15):
        check_consistency(i, b"233" * 5)
        count += 1
    check_consistency(count, 3)


@pytest.mark.parametrize(
    "url, fake_headers, expected",
    [
        [
            "http://example.com/download/ignored.txt",
            {
                "Content-Disposition": 'attachment; filename="custom_name.pdf"',
                "Content-Type": "application/pdf",
                "Content-Length": "56789"
            },
            {
                'content_length': 56789, 'content_type': 'application/pdf',
                'content_disp': 'attachment; filename="custom_name.pdf"',
                'suffix': '.pdf', 'name': 'custom_name'
            }
        ],
        [
            "http://example.com/download/ignored.txt",
            {
                "Content-Length": "abc"
            },
            {
                'content_length': None, 'content_type': None, 'content_disp': None,
                'suffix': '.txt', 'name': 'ignored'
            }
        ],
        # 当 URL 中无法解析出文件名（例如 URL 路径为空）时，应该使用 default_name 和 default_suffix 作为返回值。
        [
            "http://example.com/download/",
            {
                "Content-Length": "abc"
            },
            {
                'content_length': None, 'content_type': None, 'content_disp': None,
                'suffix': ".bin", 'name': 'default'
            }
        ],
    ]
)
def test_fetch_metadata(monkeypatch, url, fake_headers, expected):
    set_response(monkeypatch, 200, b"233", fake_headers)

    metadata_s = fetch_metadata(url=url, default_suffix=".bin", default_name="default")
    check_consistency(metadata_s, expected)


def test_download_file(tmp_path, monkeypatch):
    fake_headers = {
        "Content-Disposition": 'attachment; filename="text.pdf"',
        "Content-Type": "application/pdf"
    }
    content = b"233" * 150
    set_response(monkeypatch, 200, content, fake_headers)

    file_path = download_file(
        output_dir=temp_dir,
        url="http://example.com/download/ignored.txt",
        file_name=None,  # 自动生成文件名
        b_allow_overwrite=True,
        b_display_progress=True,
        chunk_size=10
    )

    assert os.path.exists(file_path)
    with open(file_path, "rb") as f:
        res = f.read()
    check_consistency(res, content)
