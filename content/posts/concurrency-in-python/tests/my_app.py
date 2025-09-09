# my_app.py

def greet(name: str) -> str:
    """Return a greeting message."""
    return f"Hello, {name}!"

def add(a: int, b: int) -> int:
    """Return the sum of two numbers."""
    return a + b

def main():
    """Main entry point of the program."""
    print("Running my_app...")
    msg = greet("Norbert")
    print(msg)

    result = add(3, 4)
    print(f"3 + 4 = {result}")

if __name__ == "__main__":
    main()
