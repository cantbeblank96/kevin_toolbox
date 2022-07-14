import numpy as np
from kevin.developing.notation import Kevin_Notation_Reader, Kevin_Notation_Writer

if __name__ == "__main__":
    print("test Writer")

    # 新建
    file_path = "./test.txt"
    values = [[0, 2.31, "m0.pkt"], [1, 2.22, "m1.pkt"]]
    with Kevin_Notation_Writer(file_path=file_path, mode="w") as writer:
        writer.metadata_begin()
        writer.title = "this is the title"
        writer.column_name = ["epoch", "loss", "model_name"]
        writer.column_type = {"value": ["int", "float", "str"], "sep": " "}
        writer.metadata_end()

        writer.contents_begin()
        writer.contents = values
        writer.contents_end()
    # 续写
    values = [[10, 12.31, "m01.pkt"], [11, 12.22, "m11.pkt"]]
    with Kevin_Notation_Writer(file_path=file_path, mode="a") as writer:
        writer.contents = values
        writer.contents_end()

    print("test Reader")

    # 读取
    with Kevin_Notation_Reader(file_path=file_path, chunk_size=3) as reader:
        print(reader.metadata)
        for content in reader:
            print(content)
