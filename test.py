def test():
    for i in range(10):
        yield i


d = test()
print(type(d))