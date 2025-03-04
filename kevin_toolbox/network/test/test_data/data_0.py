from kevin_toolbox.network.get_response import http


class FakeResponse:
    """模拟 urllib3.response.HTTPResponse"""

    def __init__(self, status, data, headers=None):
        self.status = status
        self.data = data
        self._offset = 0
        self.headers = headers

    def read(self, chunk_size=None):
        if chunk_size is not None:
            if self._offset >= len(self.data):
                return b""
            chunk = self.data[self._offset:self._offset + chunk_size]
            self._offset += chunk_size
        else:
            chunk = self.data[self._offset:]
        return chunk


def set_response(monkeypatch, status, data, headers=None):
    def fake_request(*args, **kwargs):
        """模拟成功的请求：返回状态码 200 和固定内容"""
        return FakeResponse(status, data, headers)

    # 使用 monkeypatch 替换 http.request 为模拟的函数
    monkeypatch.setattr(http, "request", fake_request)
