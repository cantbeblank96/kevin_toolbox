import os
import subprocess
import torch
import torch.distributed as dist


# os.environ['MASTER_ADDR'] = 'localhost'
# os.environ['MASTER_PORT'] = '5678'
#
#
# dist.init_process_group(backend='nccl', init_method='env://', world_size=1, rank=0)


def init_dist_slurm(backend, port=None):
    """
    """
    if "MASTER_ADDR" not in os.environ:
        addr = subprocess.getoutput(
            f'scontrol show hostname {os.environ["SLURM_NODELIST"]} | head -n1')
        os.environ['MASTER_ADDR'] = addr
    os.environ['MASTER_PORT'] = port

    rank = int(os.environ['SLURM_PROCID'])
    world_size = int(os.environ['SLURM_NTASKS'])
    num_gpus = torch.cuda.device_count()
    torch.cuda.set_device(rank % num_gpus)

    dist.init_process_group(backend=backend, init_method='env://', world_size=world_size, rank=rank)


init_dist_slurm(backend="nccl")

print(dist.get_world_size(), dist.get_rank())

import torch
import os
from mmcv.runner import init_dist, get_dist_info

if True:
    proc_id = int(os.environ['SLURM_PROCID'])
    ntasks = int(os.environ['SLURM_NTASKS'])
    node_list = os.environ['SLURM_NODELIST']
    print(proc_id, ntasks, node_list)

init_dist('slurm', backend="nccl", port=52222)
rank, world_size = get_dist_info()
print(rank, world_size)
