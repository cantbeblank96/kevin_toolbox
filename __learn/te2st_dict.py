class KAIMING:
    def __init__(self, x):
        assert isinstance(x, (int,))
        self.x = x

    def __hash__(self):
        return self.x % 10

    def __eq__(self, other):
        return self.x % 2 == other.x % 2

    def __get__(self, instance, owner):
        return 233


if __name__ == '__main__':
    k1 = KAIMING(11)
    k2 = KAIMING(111)

    print(f"{k2}")
    print(k1 == k2)
    print(hash(k1) == hash(k2))
    c = dict()
    c[k1] = "k1"
    print(c)
    c[k2] = "k2"
    print(c)

    c = list()
    c.append(k1)
    c.append(k1)
    # print(id(c[0]) == id(k1))
    print(id(c[0]))
    print(id(c[1]))
