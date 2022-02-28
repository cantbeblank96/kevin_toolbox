from kevin.data_flow.reader import Unified_Reader_Base


class UReader(Unified_Reader_Base):
    def __index__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_file_iterative_reader(self, file_path, chunk_size, **kwargs):
        return super().get_file_iterative_reader(file_path, chunk_size, **kwargs)

    def get_cache_manager(self, iterator, folder_path):
        return super().get_cache_manager(iterator, folder_path)

    def deal_data(self, data):
        return super().deal_data(data)


if __name__ == '__main__':
    import numpy as np

    reader = UReader(var=np.ones((10, 1)))

    print(reader.read(5, 10).shape)
    print(reader.read([3, 3]).shape)
    print(reader.find(1))

    reader = UReader(file_path="test_data.txt", chunk_size=2, folder_path="./temp/233")

    print(reader.read(2, 7))
    # del reader

    # reader = UReader(folder_path="./temp/233", chunk_size=2)
    print(len(reader))

    print(reader.read(7, 10))
    print(reader.read([3, 3]))
    print(reader.shape)
    print(len(reader))

    for i in reader:
        print(i)

    print(reader.find('data/6/horse_race_pan/2132020102319002000161_43_4.bmp'))
