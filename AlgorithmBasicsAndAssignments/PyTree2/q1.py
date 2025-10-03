import math
import sys

# 32868901 Yin Lam Lo

def get_factors(n):  # get list of factors in tuple O(sqrt(n))
    factors = []
    i = 1
    while i <= math.sqrt(n):
        if n % i == 0:
            factors.append((i, int(n / i)))
        i = i + 1
    return factors

def q(a, n):
    factors = get_factors(n)
    total = pow(a, n)
    repetition_sum = 0

    if len(factors) != 1:       # no need to calculate duplicate with prime
        factors = factors[1:]   # exclude 1 * N
        reversed_factors = list(reversed(factors))

        if reversed_factors[0][0] == reversed_factors[0][1]:    # not count the factor thats is the same e.g. 3*3
            reversed_factors = reversed_factors[1:]
        for i in range(len(reversed_factors)):      # O(sqrt(n)*2)
            reversed_factors[i] = (reversed_factors[i][1], reversed_factors[i][0])
        factors = factors + reversed_factors        # full factor tuple that leads to n

        repeated = []
        factors_factor = []

        for i in range(len(factors)):       # get all string using a^n-a for each factor
            repeated_in_factor = a**factors[i][0]-a
            repeated.append(repeated_in_factor)

        repetition_sum = sum(repeated)

        for i in range(len(factors)):       # subtract the overcounted
            _factors = get_factors(factors[i][0])[1:]
            _factor_set = set()
            for j in _factors:  # unpack tuple
                for k in j:
                    _factor_set.add(k)
                factors_factor += list(_factor_set)     # factors to be calculated and be subtract to

        # factors_factor: list of over counted by the factors


        for i in factors_factor:    # subtract the over counted created by the factors using a^n-1
            for f in factors:
                if i == f[0]:
                    repetition_sum -= a**f[0]-a

    print(f'{total - a} {total - a - repetition_sum} {a} {(total - a) % n == 0}')


if __name__ == "__main__":
    _, a, n = sys.argv
    q(int(a), int(n))

