import os
import pytest
import subprocess
import numpy as np
from kevin_toolbox.patches import for_os
from kevin_toolbox.patches.for_test import check_consistency


def test_Mutex_Lock():
    print("test locks.Mutex_Lock")

    test_dir = os.path.dirname(__file__)
    temp_dir = os.path.join(test_dir, "temp")

    for _ in range(5):
        batch_size, iter_nums = np.random.randint(3, 10), np.random.randint(10, 100)
        rank_nums = np.random.randint(3, 10)

        for_os.remove(path=temp_dir, ignore_errors=True)
        os.makedirs(temp_dir, exist_ok=True)

        # 同时运行多个 _write_to_file 脚本写入同一个文件
        #   该脚本中使用了 Mutex_Lock 互斥锁来避免不同进程之间的冲突
        process_ls = []
        for i in range(rank_nums):
            cmd = f'python {os.path.join(test_dir, "_write_to_file.py")} ' \
                  f'--file_name {os.path.join(temp_dir, "233.txt")} ' \
                  f'--rank {i} ' \
                  f'--batch_size {batch_size} ' \
                  f'--iter_nums {iter_nums} '
            process = subprocess.Popen(cmd.strip().split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process_ls.append(process)
        for p in process_ls:
            p.wait()

        # 验证各个进程写入的部分是完整的，无不干扰的，证明互斥锁发挥了作用
        with open(os.path.join(temp_dir, "233.txt"), "r") as f:
            res = f.read().strip().split("\n")
        count_s = {i: 0 for i in range(rank_nums)}
        for i in range(iter_nums * rank_nums):
            batch = res[i * batch_size:(i + 1) * batch_size]
            count_s[int(batch[0].split(":", 1)[0])] += 1
        check_consistency(iter_nums, *list(count_s.values()))

    # 清理现场
    for_os.remove(path=temp_dir, ignore_errors=True)
