import threading
import time

from fibonacci import fibonacci

NUMBERS = (35, 38, 40)
ROUNDS = 10


def store_fib_results(n, results, index):
    #Compute fibonacci(n) and store it in results[index].
    results[index] = fibonacci(n)


def run_one_round(numbers):
    """Runs one round: spins up one thread per number, waits for all of
    them, and returns the elapsed time in nanoseconds plus the results."""
    results = [None] * len(numbers)
    threads = []

    t1 = time.perf_counter_ns()          # t1 - start time (first thread about to start)

    for i in range(len(numbers)):
        n = numbers[i]
        thread = threading.Thread(
            target=store_fib_results,
            args=(n, results, i),
            name=f"FibThread-{n}"
        )
        threads.append(thread)
        thread.start()                   # each number gets its own thread

    for thread in threads:
        thread.join()                    # wait for every thread to finish

    t2 = time.perf_counter_ns()          # t2 - time after the slowest thread finished

    elapsed_ns = t2 - t1
    return elapsed_ns, results


def main():
    print("=== Fibonacci Computation With MultiThreading ===")
    print(f" Values: Fibonacci{NUMBERS}  |  Threads per round: {len(NUMBERS)}  |  Rounds: {ROUNDS}")
    print("=" * 78)
    print(f"{'Round':<8}{'T (nanoseconds)':<22}{'T (seconds)':<15}{'Results (F35, F38, F40)'}")
    print("-" * 78)

    all_times_ns = []
    for round_num in range(1, ROUNDS + 1):
        elapsed_ns, results = run_one_round(NUMBERS)
        all_times_ns.append(elapsed_ns)
        print(f"{round_num:<8}{elapsed_ns:<22,}{elapsed_ns / 1e9:<15.6f}{results}")

    avg_ns = sum(all_times_ns) / len(all_times_ns)

    print("-" * 78)
    print(f"Average T over {ROUNDS} rounds : {avg_ns:,.0f} ns  ({avg_ns / 1e9:.6f} s)")
    print(f"Fastest round              : {min(all_times_ns):,} ns")
    print(f"Slowest round              : {max(all_times_ns):,} ns")
    print("=" * 78)


if __name__ == "__main__":
    main()
