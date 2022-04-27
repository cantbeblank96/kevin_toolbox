import os
import numpy as np


class Kevin_Notation_Writer:
    """
        遵守kevin_notation格式的数据文本写入器，支持分批次向文件写入内容
    """

    def __init__(self, **kwargs):
        """
            设定关键参数
            必要参数：
                file_path:          文件路径
            写入模式相关参数：
                paras_for_open:     open() 函数的补充参数
            可选参数：
                sep：                默认的分隔符
        """

        # 默认参数
        paras = {
            # 必要参数
            "file_path": None,
            # 写入模式相关参数
            "paras_for_open": dict(mode="w", encoding='utf-8'),
            # 可选参数
            "sep": "\t",
        }

        # 获取参数
        paras.update(kwargs)

        # 校验参数
        #
        file_path = os.path.abspath(paras["file_path"])
        folder = os.path.split(file_path)[0]
        if not os.path.exists(folder):
            os.makedirs(folder)
        #
        paras_for_open = paras["paras_for_open"]
        assert isinstance(paras_for_open, (dict,))

        # 获取文件对象
        self.file = open(file_path, **paras_for_open)

        self.paras = paras

        # 状态码
        #   0：关闭所有写操作
        #   1：正在写 metadata
        #   2：正在写 contents
        self.state = dict(mode=0)

        self.file.write(f"# --kevin_notation--\n\n")

    # ------------------------------------ metadata ------------------------------------ #

    def metadata_begin(self):
        assert self.state["mode"] == 0, \
            Exception(
                f"Error: need to close the last {['metadata', 'contents'][self.state['mode'] - 1]} writing first!")
        self.state["mode"] = 1

        self.file.write(f"# --metadata--\n")
        self.write_metadata("sep", self.paras["sep"])

    def write_metadata(self, key, value):
        # 参数
        assert self.state["mode"] == 1, \
            Exception(f"Error: please call metadata_begin() before write_metadata!")
        assert isinstance(key, (str,))
        #
        paras = dict()
        if isinstance(value, (dict,)):
            assert "value" in value
            paras = value
            value = paras.pop("value")
        elif not isinstance(value, (list, tuple,)):
            value = [value]
        assert isinstance(value, (list, tuple,))
        #
        sep = paras.get("sep", self.paras['sep'])
        assert isinstance(sep, (str,))

        # key
        self.file.write(f"# {key}")
        if len(paras) > 0:
            self.file.write(f" ({','.join([f'{k}={v}' for k, v in paras.items()])})")
        self.file.write(f"\n")
        # value
        self.file.write(f"{sep.join([f'{v}' for v in value])}\n")

    def metadata_end(self):
        self.state["mode"] = 0
        self.file.write(f"\n")
        self.file.flush()

    # ------------------------------------ contents ------------------------------------ #

    def contents_begin(self):
        assert self.state["mode"] == 0, \
            Exception(
                f"Error: need to close the last {['metadata', 'contents'][self.state['mode'] - 1]} writing first!")
        self.state["mode"] = 2

        self.file.write(f"# --contents--\n")

    def write_contents(self, value):
        assert self.state["mode"] == 2, \
            Exception(f"Error: please call contents_begin() before write_contents!")

        value = np.array(value)
        if value.ndim <= 1:
            value = value.reshape((1, -1))
        for row in value:
            self.file.write(f"{self.paras['sep'].join([f'{r}' for r in row])}\n")

    def contents_end(self):
        self.state["mode"] = 0
        self.file.write(f"\n")
        self.file.flush()

    # ------------------------------------ magic func ------------------------------------ #

    # self.key = value
    def __setattr__(self, key, value):
        """
            支持直接通过 self.key = value 的方式来写入 metadata 和 contents
        """
        if "state" not in self.__dict__:
            # status 未被设置，未完成初始化
            super().__setattr__(key, value)
        else:
            assert self.state["mode"] > 0, \
                Exception(f"Error: please call metadata_begin() or contents_begin() before write!")
            if self.state["mode"] == 1:
                self.write_metadata(key, value)
            else:
                self.write_contents(value)

    # with 上下文管理器
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self

    def __del__(self):
        try:
            del self.paras, self.state
            self.file.close()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    import numpy as np

    values = [[0, 2.31, "m0.pkt"], [1, 2.22, "m1.pkt"]]

    writer = Kevin_Notation_Writer(file_path="./test.txt")

    writer.metadata_begin()
    writer.title = "this is the title"
    writer.column_name = ["epoch", "loss", "model_name"]
    writer.column_type = {"value": ["int", "float", "str"], "sep": " "}
    writer.metadata_end()

    writer.contents_begin()
    writer.contents = values
    writer.contents_end()

    with Kevin_Notation_Writer(file_path="./test2.txt") as writer:
        writer.metadata_begin()
        writer.title = "this is the title"
        writer.column_name = ["epoch", "loss", "model_name"]
        writer.column_type = {"value": ["int", "float", "str"], "sep": " "}
        writer.metadata_end()

        writer.contents_begin()
        writer.contents = values
        writer.contents_end()
