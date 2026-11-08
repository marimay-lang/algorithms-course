# Integer mathematics without accidental overflow

Part of the MIT-licensed Marimay hobby learning project.

Run from the course root:

```sh
mmay run ./examples/07-number-theory
mmay test . --engine both
```

Read the [implementation and focused tests](../../algorithms/numeric/).

## Invariant

Euclidean reduction preserves the common divisors. In binary exponentiation the accumulated result times the remaining power equals the original power. Modular multiplication uses subtraction-based addition to avoid overflowing an intermediate sum.

## Trace

gcd(54,24) reduces through (24,6) to (6,0). power(-2,3) is -8. modularPower(2,10,1000) is 24. integerSquareRoot(15) is 3.

## Cost

GCD is O(log min(a,b)) for positive inputs; LCM adds one checked multiplication. Binary power is O(log exponent). Modular power is O(log exponent * log modulus). Trial primality/factorization are O(sqrt n); sieve is O(limit log log limit), O(limit) space. Binomial DP is O(n*min(k,n-k)) with linear row storage. Integer square root is O(log n), O(1) space.

## Contract

GCD/LCM accept nonnegative integers, with gcd(0,0)=0 and lcm(0,x)=0. power accepts a signed base and a nonnegative exponent; 0^0=1. Modular power requires a nonnegative base/exponent and positive modulus. Sieve returns primes strictly below its nonnegative limit; factorization requires value>=1. None distinguishes invalid input or overflow from a numeric answer.

## Exercise

Implement a segmented sieve reusing the prime list. State its interval contract before handling 0, 1 and an empty segment.
