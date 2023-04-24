import fcntl
import os
import time
from kevin_toolbox.computer_science.algorithm.locks import Mutex_Lock
import argparse

# 参数
# args = dict(
#     file_name="/home/SENSETIME/xukaiming/Desktop/my_repos/python_projects/kevin_toolbox/kevin_toolbox/computer_science/algorithm/locks/test/temp/233.txt",
#     rank=1,
#     batch_size=3,
#     iter_nums=10
# )
out_parser = argparse.ArgumentParser()
out_parser.add_argument('--file_name', type=str, required=True)
out_parser.add_argument('--rank', type=int, required=False, default=0)
out_parser.add_argument('--batch_size', type=int, required=False, default=3)
out_parser.add_argument('--iter_nums', type=int, required=False, default=100)
args = out_parser.parse_args().__dict__
print(args)

wait_interval = 1e-3
lock = Mutex_Lock(lock_name=args["file_name"] + ".lock", wait_interval=wait_interval)

for _ in range(args["iter_nums"]):
    # 获取锁
    lock.acquire(b_block_if_fail=True)
    print(f'rank {args["rank"]} is running')
    with  open(args["file_name"], 'a') as f:
        for _ in range(args["batch_size"]):
            f.write(f'{args["rank"]}: Hello, World!\n')
    lock.release()
