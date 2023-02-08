from kevin.data_flow.file import kevin_notation


def read(file_path):
    """
        读取整个文件的快捷接口
    """
    with kevin_notation.Reader(file_path=file_path, chunk_size=-1) as reader:
        # metadata
        metadata = reader.metadata
        # content
        try:
            content = next(reader)
        except:
            content = None
    return metadata, content
