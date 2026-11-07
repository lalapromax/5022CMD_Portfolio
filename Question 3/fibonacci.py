def fibonacci(n: int):
    if n <= 1:          # 1 comparison
        return n        # 1 return
    return fibonacci(n - 1) + fibonacci(n - 2)   # 2 recursive calls + 1 addition + 1 return


if __name__ == "__main__":
    for i in range(10):
        print(f"fibonacci({i}) = {fibonacci(i)}")

