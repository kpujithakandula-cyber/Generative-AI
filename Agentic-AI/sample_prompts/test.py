def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def print_primes_up_to(limit):
    """Print all prime numbers up to the given limit."""
    primes = [num for num in range(2, limit + 1) if is_prime(num)]
    print(f"Prime numbers up to {limit}:")
    print(", ".join(map(str, primes)))
    print(f"Total count: {len(primes)}")


if __name__ == "__main__":
    print_primes_up_to(100)
