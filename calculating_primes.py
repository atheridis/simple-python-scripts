import numpy as np
from math import sqrt, ceil, floor
import concurrent.futures
import os


def sieve(limit):
    """
    Calculates prime numbers using the Sieve of Eratosthenes.

    :param int limit: Choose the limit which primes are calculated. Exclusive.
    :return np.array:
    """
    is_prime = np.ones(limit, dtype=bool)
    for n in range(2, ceil(sqrt(limit))):
        if is_prime[n]:
            is_prime[n * n :: n] = 0
    is_prime[0] = 0
    is_prime[1] = 0

    os.makedirs(f"primes{limit}", exist_ok=True)

    np.save(f"primes{limit}/Prime_{limit}_0", np.packbits(is_prime))

    return np.nonzero(is_prime)[0], is_prime


def wrapper(limit, segment, primes, worker):
    segment_range = [segment * worker, (1 + worker) * segment]
    if segment_range[1] >= limit:
        segment_range[1] = limit

    is_prime_range = np.ones(segment, dtype=bool)

    for i in range(len(primes)):
        loLim = floor(segment_range[0] / primes[i]) * primes[i]

        if loLim < segment_range[0]:
            loLim += primes[i]

        for j in range(loLim, segment_range[1], primes[i]):
            is_prime_range[j - segment_range[0]] = 0

    np.save(f"primes{segment}/Prime_{segment}_{worker}", np.packbits(is_prime_range))

    # return is_prime_range, worker


def segmented_sieve(limit):
    """
    Calculates prime numbers using the Sieve of Eratosthenes.
    Uses less memory compared to sieve, but is a bit slower.

    :param int limit: Choose the limit which primes are calculated. Exclusive.
    :return:
    """
    segment = int(ceil(sqrt(limit)))
    primes, is_prime = sieve(segment)

    prime_list = []
    prime_list.append((is_prime, 0))

    with concurrent.futures.ProcessPoolExecutor(12) as executor:
        results = []
        worker = 0
        while segment < limit:
            worker += 1
            results.append(
                executor.submit(wrapper, limit, int(ceil(sqrt(limit))), primes, worker)
            )
            segment += int(ceil(sqrt(limit)))

    return prime_list, int(ceil(sqrt(limit)))


def get_primes(seg, code):
    p = np.load(f"primes{seg}/Prime_{seg}_{code}.npy")
    p = np.unpackbits(p, count=seg)
    return np.nonzero(p)[0] + seg * code


def is_prime(seg, n):
    code = floor(n / seg)
    pos = n % seg
    primes = np.load(f"primes{seg}/Prime_{seg}_{code}.npy")
    primes = np.unpackbits(primes, count=seg)
    return primes[pos]


if __name__ == "__main__":
    l, seg = segmented_sieve(1_000_000)
    print(get_primes(1000, 1))
    # isprime = 0
    # print(is_prime(31623 ,isprime))

    # sums = 0
    # lists = []
    # count = 0
    # for i in range(100000):
    #     # if i % 1000 == 0:
    #     #     print(f"i: {i}")
    #     primes = get_primes(100000, i)
    #     for prime in primes:
    #         count += 1
    #         if count % 10000000 == 0:
    #             print(f"i: {int(count / 100000)}")
    #         sums = sums + int(prime)*int(prime)
    #         if sums % count == 0:
    #             lists.append(count)
    #             print(count)
