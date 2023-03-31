import pytest

from kevin_toolbox.machine_learning.dataset.face import dummy, verification, analysis
from kevin_toolbox.data_flow.core.reader import UReader
import numpy as np
import torch

seed = 233
np.random.seed(seed)
torch.manual_seed(seed)
torch.cuda.manual_seed_all(seed)


def test_face():
    print("构造测试数据")

    # all
    dummy_factory = dummy.Factory(human_nums=50, dims_of_feature=25, gallery_nums=30)
    data = dummy_factory.generate(nums=20)
    # print(data)

    print("测试 Factory")

    factory = verification.Factory(features=UReader(var=data["features"]),
                                   clusters=UReader(var=data["clusters"]))
    dataset = factory.generate_by_block([1, 2, 3], None, [3, 4, 5], None)
    print(dataset.keys())
    print(dataset)

    dataset = factory.generate_by_samples(np.array(list(zip([11, 16, 17], [11, 16, 17]))))
    print(dataset.keys())
    print(dataset)

    print("测试 executor、generator")

    # executor_ls
    executor_ls, size_ls = verification.get_executor_ls.by_block(mode="triangle", factory=factory, chunk_step=2,
                                                                 need_to_generate={"scores", "labels", "samples"})
    # generator
    generator = verification.build_generator(executor_ls, size_ls)
    lens = []
    for i, db in enumerate(generator):
        lens.append(size_ls[i])
        # print(lens[-1])
    print(f"sum {sum(lens)}")

    print("测试 executor、iterator")

    # executor_ls
    samples = UReader(var=np.array(list(zip([1, 2, 3], [4, 5, 6]))))
    executor_ls, size_ls = verification.get_executor_ls.by_samples(samples=samples, factory=factory, chunk_step=2,
                                                                   need_to_generate={"scores", "labels", "samples"})

    # iterator
    iterator = verification.build_iterator(executor_ls, size_ls)
    lens = []
    for i, db in enumerate(iterator):
        lens.append(size_ls[i])
        print(lens[-1])
        print(db)
    print(f"sum {sum(lens)}")


def test_analysis():
    print("构造测试数据")
    dummy_factory = dummy.Factory(human_nums=50, dims_of_feature=25, gallery_nums=30)
    data = dummy_factory.generate(nums=1000)

    factory = verification.Factory(features=UReader(var=data["features"]),
                                   clusters=UReader(var=data["clusters"]))

    executor_ls, size_ls = verification.get_executor_ls.by_block(mode="triangle", factory=factory, chunk_step=10,
                                                                 need_to_generate={"scores", "labels", "samples"})
    # iterator
    iterator = verification.build_iterator(executor_ls, size_ls)

    print("测试 get_fail_case_from_iterator")

    fp_db, fn_db = analysis.get_fail_case_from_iterator(iterator=iterator, threshold=0.3, upper_bound=3, verbose=False)
    print(fp_db, fn_db)
