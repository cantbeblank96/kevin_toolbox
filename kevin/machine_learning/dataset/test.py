from kevin.machine_learning.dataset.face import dummy, verification
from kevin.data_flow.reader import UReader

if __name__ == '__main__':
    import numpy as np

    print("构造测试数据")

    # all
    dummy_factory = dummy.Factory(human_nums=50, dims_of_feature=256, gallery_nums=30)
    data = dummy_factory.generate(nums=100)
    # print(data)

    print("构造数据集")

    factory = verification.Factory(features=UReader(var=data["features"]),
                                   clusters=UReader(var=data["clusters"]))
    dataset = factory.generate_by_block([1, 2, 3], None, [3, 4, 5], None)
    print(dataset.keys())
    print(dataset)

    dataset = factory.generate_by_samples(np.array(list(zip([1, 2, 3], [4, 5, 6]))))
    print(dataset.keys())
    print(dataset)

    print("构造迭代器")

    generator = verification.get_generator_by_block(mode="triangle", factory=factory, chunk_step=30,
                                                    need_to_generate={"scores", "labels", "samples"})
    lens = []
    for db in generator:
        lens.append(len(db["scores"]))
        print(lens[-1])
    print(f"sum {sum(lens)}")

    #
    samples = UReader(var=np.array(list(zip([1, 2, 3], [4, 5, 6]))))
    generator = verification.get_generator_by_samples(samples=samples, factory=factory, chunk_step=2,
                                                      need_to_generate={"scores", "labels", "samples"})
    lens = []
    for db in generator:
        lens.append(len(db["scores"]))
        print(lens[-1])
    print(f"sum {sum(lens)}")
