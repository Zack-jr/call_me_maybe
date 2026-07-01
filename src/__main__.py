from src.call_me_maybe import run


def main() -> None:
    """runs the program"""
    try:
        run()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
