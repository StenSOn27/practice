from fibonacci_lib import infinite_fibonacci, ConsumeWithTimeout


def main() -> None:
    consumer = ConsumeWithTimeout(infinite_fibonacci(), timeout_seconds=3)
    for _ in consumer:
        pass


if __name__ == '__main__':
    main()
