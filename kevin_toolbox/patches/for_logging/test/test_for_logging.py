import os
import logging
import pytest
from kevin_toolbox.patches.for_os import remove
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.computer_science.algorithm.registration import Registry
from kevin_toolbox.patches.for_logging import build_logger

LOGGERS = Registry(uid="LOGGERS")
temp_dir = os.path.join(os.path.dirname(__file__), "temp")


def test_build_logger():
    print("test for_logging.build_logger()")

    remove(path=temp_dir, ignore_errors=True)

    # 多次调用build_logger()，不会重复创建logger
    logger_id_ls = []
    for _ in range(3):
        logger = build_logger(
            name=":global",
            handler_ls=[
                           dict(target=None, level="INFO", formatter="%(name)s - %(levelname)s - %(message)s"),
                       ] + [
                           dict(target=os.path.join(temp_dir, f'log_{n}.txt'), level=n if i % 2 == 0 else v) for
                           i, (n, v) in enumerate(logging._nameToLevel.items())
                       ],
            registry=LOGGERS
        )
        logger_id_ls.append(id(logger))
    check_consistency(*logger_id_ls)

    logger = LOGGERS.get(name=":global")

    # 写入
    for n, v in logging._nameToLevel.items():
        logger.log(level=v, msg=f'This is a {n} message')

    # 检查
    for n, v in logging._nameToLevel.items():
        with open(os.path.join(temp_dir, f'log_{n}.txt'), 'r') as f:
            levels = [i.strip().rsplit(" ", 2)[-2] for i in f.read().strip().split("\n", -1)]
        levels_expected = [i for i, j in logging._nameToLevel.items() if j >= v]
        if n == "NOTSET":
            levels_expected.remove("NOTSET")
        check_consistency(levels, levels_expected)
