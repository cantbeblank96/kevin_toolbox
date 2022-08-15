import os
import copy
import numpy as np
from kevin.data_flow.file.kevin_notation.converter import Converter, CONVERTER_FOR_WRITER
from kevin.data_flow.file import kevin_notation


class Kevin_Notation_Writer:
    """
        遵守 kevin_notation 格式的数据文本写入器（格式要求参见本模块下的 readme）
            支持分批次向文件写入内容
    """

    def __init__(self, **kwargs):
        """
            设定关键参数

            必要参数：
                file_path:          <string> 文件路径
            写入相关参数：
                mode:               <string> 写入模式
                                        支持以下模式：
                                            "w":    从头开始写入
                                            "a":    从末尾续写（要求文件已经具有 metadata）
                paras_for_open:     <paras dict> open() 函数的补充参数（除 mode 以外）
                converter:          <instance of kevin.Converter> converter is a dictionary-like data structure
                                            consisting of <string>:<func> pairs，
                                            用于根据指定数据类型选取适当的函数来处理输入数据。
                sep：                <string> 默认的分隔符
                                            默认使用 \t
        """

        # 默认参数
        paras = {
            # 必要参数
            "file_path": None,
            # 写入模式相关参数
            "mode": "w",
            "paras_for_open": dict(encoding='utf-8'),
            # 可选参数
            "converter": CONVERTER_FOR_WRITER,
            "sep": "\t",
        }

        # 获取参数
        paras.update(kwargs)

        # 校验参数
        #
        paras["file_path"] = os.path.abspath(paras["file_path"])
        os.makedirs(os.path.split(paras["file_path"])[0], exist_ok=True)
        #
        assert paras["mode"] in ["w", "a"]
        #
        assert isinstance(paras["paras_for_open"], (dict,))
        paras["paras_for_open"]["mode"] = paras["mode"]
        #
        assert isinstance(paras["converter"], (Converter, dict,))
        assert isinstance(paras["sep"], (str,))

        self.paras = paras

        # metadata
        self.metadata = dict()
        # 文件对象
        self.file = None

        if paras["mode"] == "a":
            # 采用追加写模式
            # 尝试打开已有文件
            assert os.path.isfile(self.paras["file_path"])
            try:
                # 要求 metadata 已被写入
                reader = kevin_notation.Reader(file_path=self.paras["file_path"])
            except Exception as e:
                raise Exception(f'file {self.paras["file_path"]} existed, but is not a standard kevin document!')
            self.metadata = copy.deepcopy(reader.metadata)
            del reader
            # 获取文件对象
            self.file = open(self.paras["file_path"], **self.paras["paras_for_open"])
            # 初始状态码
            beg_stage = 2
        else:
            # 采用覆盖写模式
            self.metadata["sep"] = self.paras["sep"]
            # 获取文件对象
            self.file = open(self.paras["file_path"], **self.paras["paras_for_open"])
            # 写入文件标记
            self.file.write(f"# --kevin_notation--\n\n")
            # 初始状态码
            beg_stage = 0

        # 变量
        # state 状态码
        #   0：关闭所有写操作
        #   1：正在写 metadata
        #   2：正在写 contents
        self.state = dict(stage=beg_stage)

    # ------------------------------------ metadata ------------------------------------ #

    def metadata_begin(self):
        assert self.state["stage"] == 0, \
            Exception(
                f"Error: need to close the last {['metadata', 'contents'][self.state['stage'] - 1]} writing first!")
        self.state["stage"] = 1

        self.file.write(f"# --metadata--\n")
        self.write_metadata("sep", self.paras["sep"])

    def write_metadata(self, key, value):
        """
            支持两种方式指定 value
                <list or tuple> 直接指定 value 的值，写入方式参考默认值
                <dict> 一个包含 value 以及额外指定写入方式参数的字典
                    {"value": <list or tuple>, "sep": ..., }
        """
        # 参数
        assert self.state["stage"] == 1, \
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

        # check
        if "column_num" in self.metadata:
            if key in ["column_name", "column_type"]:
                assert len(value) == self.metadata["column_num"]

        # write
        # key
        self.file.write(f"# {key}")
        if len(paras) > 0:
            self.file.write(f" ({','.join([f'{k}={v}' for k, v in paras.items()])})")
        self.file.write(f"\n")
        # value
        self.file.write(f"{sep.join([f'{v}' for v in value])}\n")

        # metadata
        value = list(value)
        self.metadata[key] = value[0] if len(value) == 1 else value
        #
        if key in ["column_name", "column_type"]:
            self.metadata["column_num"] = len(value)

    def metadata_end(self):
        self.state["stage"] = 0
        self.file.write(f"\n")
        self.file.flush()

    # ------------------------------------ contents ------------------------------------ #

    def contents_begin(self):
        assert self.state["stage"] == 0, \
            Exception(
                f"Error: need to close the last {['metadata', 'contents'][self.state['stage'] - 1]} writing first!")
        self.state["stage"] = 2

        self.file.write(f"# --contents--\n")

    def write_contents(self, value):
        assert self.state["stage"] == 2, \
            Exception(f"Error: please call contents_begin() before write_contents!")
        if len(value) == 0:
            return

        value = np.array(value)
        if value.ndim <= 1:
            value = value.reshape((1, -1))

        if "column_num" in self.metadata:
            assert value.shape[-1] == self.metadata["column_num"], \
                f"{value.shape}"

        # 转换并写入
        if "column_type" in self.metadata:
            type_ls = self.metadata["column_type"]
        else:
            type_ls = ["default"] * len(value.shape[-1])

        for row in value:
            row = [self.paras["converter"][type_](r) for type_, r in zip(type_ls, row)]
            line = f"{self.metadata['sep'].join(row)}\n"
            self.file.write(line)

    def contents_end(self):
        self.state["stage"] = 0
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
            assert self.state["stage"] > 0, \
                Exception(f"Error: please call metadata_begin() or contents_begin() before write!")
            if self.state["stage"] == 1:
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