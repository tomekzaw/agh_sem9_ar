from sequential import how_many_primes
from tqdm import tqdm


if __name__ == '__main__':
    # general tests
    for size in range(1, 10):
        assert how_many_primes(2, size) == 1
        assert how_many_primes(3, size) == 2
        assert how_many_primes(4, size) == 2
        assert how_many_primes(5, size) == 3
        assert how_many_primes(6, size) == 3
        assert how_many_primes(7, size) == 4
        assert how_many_primes(11, size) == 5
        assert how_many_primes(100, size) == 25
        assert how_many_primes(1000, size) == 168
        assert how_many_primes(10000, size) == 1229

    # load primes
    with open('primes.txt') as f:
        primes = map(int, f.read().strip().split(','))

    # detailed tests
    expected = 0
    next_prime = next(primes)

    for n in tqdm(range(0, 10_000)):
        if n == next_prime:
            expected += 1
            next_prime = next(primes)

        for size in range(1, 20):
            actual = how_many_primes(n, size)
            if actual != expected:
                raise Exception(f'Failed for n={n} and size={size}: actual={actual}, expected={expected}')
