import threading
import time

from fibonacci import fibonacci

NUMBERS = (35, 38, 40)
ROUNDS = 10


def store_fib_results(n, results, index):
    results[index] = fibonacci(n)


def run_multithreaded_round(numbers):
    results = [None] * len(numbers)
    threads = []

    t1 = time.perf_counter_ns()

    for i, n in enumerate(numbers):
        thread = threading.Thread(
            target=store_fib_results,
            args=(n, results, i)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    t2 = time.perf_counter_ns()
    return t2 - t1, results


def run_non_threaded_round(numbers):
    t1 = time.perf_counter_ns()
    results = [fibonacci(n) for n in numbers]

    return time.perf_counter_ns() - t1, results


# Reusable benchmarking function
def benchmark(title, run_function):

    print(f"=== {title} ===")
    print(f"Values: Fibonacci{NUMBERS} | Rounds: {ROUNDS}")
    print("=" * 78)
    print(f"{'Round':<8}{'T (nanoseconds)':<22}{'T (seconds)':<15}{'Results'}")
    print("-" * 78)

    times = []

    for round_num in range(1, ROUNDS + 1):
        elapsed_ns, results = run_function(NUMBERS)
        times.append(elapsed_ns)

        print(f"{round_num:<8}{elapsed_ns:<22,}{elapsed_ns / 1e9:<15.6f}{results}")

    avg_ns = sum(times) / len(times)

    print("-" * 78)
    print(f"Average T: {avg_ns:,.0f} ns ({avg_ns / 1e9:.6f} s)")
    print(f"Fastest round: {min(times):,} ns")
    print(f"Slowest round: {max(times):,} ns")
    print("=" * 78)

    return avg_ns


def main():

    # 1. Multithreaded benchmark
    mt_avg_ns = benchmark(
        "Fibonacci Computation With Multithreading",
        run_multithreaded_round)

    print()

    # 2. Sequential benchmark
    st_avg_ns = benchmark(
        "Fibonacci Computation Without Multithreading",
        run_non_threaded_round)

    # 3. Observation
    diff_percent = ((st_avg_ns - mt_avg_ns) / st_avg_ns) * 100

    print("\n=== BENCHMARK OBSERVATION ===")

    if diff_percent > 0:
        print(f"Multithreading reduced average completion time by {diff_percent:.1f}%.")
    elif diff_percent < 0:
        print(f"Multithreading increased average completion time by {abs(diff_percent):.1f}%.")
    else:
        print("Multithreading made no measurable difference.")


if __name__ == "__main__":
    main()