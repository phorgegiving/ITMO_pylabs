import timeit
cache = {}

def fabonachi(idx):
    if idx <=1:
        return idx
    return fabonachi(idx-1) + fabonachi(idx-2)

def fibonachi_alt(idx):
    if idx in cache:
        return cache(idx)
    
    if idx <= 1:
        return idx
    res = fibonachi_alt(idx-1)+fibonachi_alt(idx-2)
    cache[idx] = res
    return res

if __name__ == '__main__':
    res1 = timeit.timeit('fibonachi_alt(38)',
                         number=1,
                         globals=globals())
    print(res1)

    res2 = timeit.timeit('fabonachi(38)',
                         number=1,
                         globals=globals())
    print(res2)