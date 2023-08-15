import pytest
from kevin_toolbox.patches.for_test import check_consistency
from kevin_toolbox.computer_science.algorithm import for_seq


def test_chunk_generator_0():
    print("test for_seq.chunk_generator()")

    # 测试输入是 具有 __len__ 属性的iterator、序列的情况
    for inputs in [range(10), list(range(10)), tuple(range(10))]:
        # 测试情况： len(inputs) > chunk_size
        #   b_drop_last=False
        info_s = dict()
        res = []
        for i in for_seq.chunk_generator(inputs=inputs, chunk_size=3, hook_for_progress_rate=info_s,
                                         b_display_progress=False, b_drop_last=False):
            res.append([info_s['progress_rate'], i])
        check_consistency([[0.25, [0, 1, 2]], [0.5, [3, 4, 5]], [0.75, [6, 7, 8]], [1.0, [9]]], res)
        #
        res = [i for i in
               for_seq.chunk_generator(inputs=inputs, chunk_size=3, b_display_progress=False, b_drop_last=False)]
        check_consistency([[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]], res)
        #   b_drop_last=True
        res = []
        for i in for_seq.chunk_generator(inputs=inputs, chunk_size=4, hook_for_progress_rate=info_s,
                                         b_display_progress=False, b_drop_last=True):
            res.append([info_s['progress_rate'], i])
        check_consistency([[0.5, [0, 1, 2, 3]], [1.0, [4, 5, 6, 7]]], res)

        # 测试情况： len(inputs) < chunk_size
        #   b_drop_last=False
        res = []
        for i in for_seq.chunk_generator(inputs=inputs, chunk_size=15, hook_for_progress_rate=info_s,
                                         b_display_progress=False, b_drop_last=False):
            res.append([info_s['progress_rate'], i])
        check_consistency([[1.0, list(range(10))]], res)
        #   b_drop_last=True
        res = []
        for i in for_seq.chunk_generator(inputs=inputs, chunk_size=15, hook_for_progress_rate=info_s,
                                         b_display_progress=False, b_drop_last=True):
            res.append([info_s['progress_rate'], i])
        check_consistency([], res)


def test_chunk_generator_1():
    print("test for_seq.chunk_generator()")

    # 测试输入是 不具有 __len__ 属性的 iterator、generator 的情况
    def my_generator(start, end):
        for i in range(start, end):
            yield i

    class My_Iterator:
        def __init__(self, start, end):
            self.start = start
            self.end = end

        def __iter__(self):
            return self

        def __next__(self):
            if self.start >= self.end:
                raise StopIteration
            else:
                self.start += 1
                return self.start - 1

    for func in [my_generator, My_Iterator]:
        # 测试情况： len(inputs) > chunk_size
        #   b_drop_last=False
        info_s = dict()
        res = []
        for i in for_seq.chunk_generator(inputs=func(0, 10), chunk_size=3, hook_for_progress_rate=info_s,
                                         b_display_progress=False, b_drop_last=False):
            res.append([info_s['progress_rate'], i])
        check_consistency([[1, [0, 1, 2]], [2, [3, 4, 5]], [3, [6, 7, 8]], [4, [9]]], res)
        #   b_drop_last=True
        res = []
        for i in for_seq.chunk_generator(inputs=func(0, 10), chunk_size=4, hook_for_progress_rate=info_s,
                                         b_display_progress=False, b_drop_last=True):
            res.append([info_s['progress_rate'], i])
        check_consistency([[1, [0, 1, 2, 3]], [2, [4, 5, 6, 7]]], res)

        # 测试情况： len(inputs) < chunk_size
        #   b_drop_last=False
        res = []
        for i in for_seq.chunk_generator(inputs=func(0, 10), chunk_size=15, hook_for_progress_rate=info_s,
                                         b_display_progress=False, b_drop_last=False):
            res.append([info_s['progress_rate'], i])
        check_consistency([[1, list(range(10))]], res)
        #   b_drop_last=True
        res = []
        for i in for_seq.chunk_generator(inputs=func(0, 10), chunk_size=15, hook_for_progress_rate=info_s,
                                         b_display_progress=False, b_drop_last=True):
            res.append([info_s['progress_rate'], i])
        check_consistency([], res)
