class Simple_Seq:
    def __init__(self, data, error_idx_ls):
        self.data = data
        self.error_idx_ls = error_idx_ls

    def __call__(self, idx):
        if idx in self.error_idx_ls:
            raise IndexError("Custom Errors")
        return self.data[idx]

    def __getitem__(self, idx):
        return self(idx)

    def __len__(self):
        return len(self.data)


if __name__ == '__main__':
    # 测试
    data = [1, 2, 3, 4, 5]
    seq = Simple_Seq(data=data, error_idx_ls=[2, 3])

    print(seq[1])
    print(seq(4))
    print(seq(3))
