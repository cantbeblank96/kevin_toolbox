import hashlib
import json
import warnings


def get_hash(item, length=8, mode="md5"):
    """
        将输入 item 序列化，再计算出 hash 值
            本函数对于无序的字典能够提供唯一的 hash 值

        参数:
            item:
            length:         <int> 返回 hash 字符串的前多少位
            mode:           <str> 支持 hashlib 中提供的 hash 方法
    """
    worker = eval(f'hashlib.{mode}()')
    assert mode in hashlib.__all__
    try:
        item = json.dumps(item, sort_keys=True).encode()
    except:
        warnings.warn(
            f"the item {type(item)} unable to be serialized by json, reproducibility is no longer guaranteed!",
            UserWarning
        )
    worker.update(f"{item}".encode('utf-8'))
    hash_ = worker.hexdigest()[:length]
    return hash_


if __name__ == '__main__':
    print(get_hash(item={2,4}, length=8, mode="sha512"))
