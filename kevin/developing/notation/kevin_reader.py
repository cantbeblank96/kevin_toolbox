import os
from kevin.data_flow.reader import File_Iterative_Reader
from .converter import CONVERTER_FOR_READER


class Kevin_Notation_Reader:
    """
        遵守kevin_notation格式的数据文本读取器，支持分批次读取文件内容
    """

    def __init__(self, **kwargs):
        """
            设定关键参数
            必要参数：
                file_path:          文件路径
            读取相关参数：
                chunk_size:         每次读取多少行数据
                beg：                开始读取的位置
                                        默认为0
        """

        # 默认参数
        paras = {
            # 必要参数
            "file_path": None,
            # 读取相关参数
            "chunk_size": 100,
            "beg": 0,
        }

        # 获取参数
        paras.update(kwargs)

        # 校验参数
        #
        assert isinstance(paras["file_path"], (str,)) and os.path.isfile(paras["file_path"])

        self.paras = paras

        # 读取开头
        self.reader = File_Iterative_Reader(file_path=paras["file_path"], pre_jump_size=paras["beg"], drop=False)

        # kevin_notation
        offset = self.read_head(reader=self.reader, head="# --kevin_notation--")

        # metadata
        offset += self.read_head(reader=self.reader, head="# --metadata--")
        #
        self.metadata, count = self.read_metadata(reader=self.reader)
        offset += count

        del self.reader

        # 读取内容
        self.reader = File_Iterative_Reader(file_path=paras["file_path"],
                                            pre_jump_size=paras["beg"] + offset, drop=False)

        # contents
        self.read_head(reader=self.reader, head="# --contents--")

    # ------------------------------------ read head ------------------------------------ #

    @staticmethod
    def read_head(reader, head, try_times=10):
        reader.paras.update(dict(
            chunk_size=1,
            convert_func=lambda x: x[0],
            map_func=lambda x: x.strip()
        ))
        #
        for count in range(1, try_times + 1):
            line = next(reader)
            if line.startswith("#"):
                assert line.startswith(head), \
                    f"format of {head} is wrong!"
                return count
        raise Exception(f"can't find {head} after {try_times} attempts")

    # ------------------------------------ read metadata ------------------------------------ #

    @staticmethod
    def read_metadata(reader):
        reader.paras.update(dict(
            chunk_size=2,
            convert_func=None,
            map_func=None,  # 临时将 map_func 设为 None，避免将sep的值过滤掉
        ))
        key, sep = next(reader)
        assert key.startswith("# sep"), \
            f"format of metadata is wrong!"  # 开头第一个参数必须是 sep
        reader.paras.update(dict(
            map_func=lambda x: x.strip()
        ))  # 恢复 map_func
        res = dict(sep=sep.replace("\n", ""))
        #
        count = 2
        for (key, value) in reader:
            assert key.startswith("# ")
            if key.startswith("# --contents--"):
                break
            temp_ls = [i.strip() for i in key.split(' ', 2)]
            assert len(temp_ls) >= 2
            #
            count += 2
            #
            key = temp_ls[1]
            #
            paras_dict = dict()
            if len(temp_ls) > 2:
                paras = temp_ls[2]
                assert paras.startswith("(") and paras.endswith(")")
                paras = paras[1:-1]
                paras_ls = [i.split("=", 1) for i in paras.split(",", -1)]
                paras_dict.update({k: v for (k, v) in paras_ls})
            sep = paras_dict.get("sep", res["sep"])
            #
            if sep in value:
                value = value.split(sep, -1)
            #
            res[key] = value

        # 最后检验内容
        # 与 column 数量相关的字段是否相互一致
        num_ls = [len(res[key]) for key in ["column_name", "column_type", "column_num"] if key in res]
        assert len(set(num_ls)) <= 1
        #
        if len(num_ls) > 0:
            res["column_num"] = num_ls[0]
        #
        if "column_type" in res:
            unknown_types = set(res["column_type"]).difference(set(CONVERTER_FOR_READER.keys()))
            assert len(unknown_types) == 0, \
                f"There are unknown types {unknown_types} in column_type. " \
                f"Currently supported types are {set(CONVERTER_FOR_READER.keys())}"

        return res, count

    # ------------------------------------ read contents ------------------------------------ #

    @staticmethod
    def read_contents(reader, chunk_size, metadata):
        """
            读取 contents，并根据 metadata 对其进行解释
        """
        reader.paras.update(dict(
            chunk_size=chunk_size,
            convert_func=None,
            map_func=lambda x: x.strip(),
        ))
        #
        res = None
        chunk = next(reader)
        # 解释
        for line in chunk:
            value_ls = line.split(metadata["sep"])
            if "column_type" in metadata:
                assert len(value_ls) == len(metadata["column_type"])
                type_ls = metadata["column_type"]
            else:
                # use default converter
                type_ls = ["default"] * len(value_ls)
            value_ls = [CONVERTER_FOR_READER[type_](value) for type_, value in zip(type_ls, value_ls)]
            if res is None:
                res = [[] for _ in range(len(value_ls))]
            for i, value in enumerate(value_ls):
                res[i].append(value)
        # 整理
        if res is not None:
            column_name = metadata.get("column_name", list(range(len(res))))
            assert len(column_name) == len(res)
            res = {k: res[i] for i, k in enumerate(column_name)}
        return res, len(chunk)

    # ------------------------------------ magic func ------------------------------------ #

    def __next__(self):
        contents, len_ = self.read_contents(reader=self.reader, chunk_size=self.paras["chunk_size"],
                                            metadata=self.metadata)
        if len_ == 0:
            raise StopIteration
        else:
            return contents

    def __iter__(self):
        return self

    # with 上下文管理器
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self

    def __del__(self):
        try:
            del self.paras, self.metadata, self.reader
        except Exception as e:
            print(e)
