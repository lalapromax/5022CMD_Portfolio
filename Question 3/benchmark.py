import threading
import time

from fibonacci import fibonacci

NUMBERS = (35, 38, 40)
ROUNDS = 10


def store_fib_results(n, results, index):
    # Compute fibonacci(n) and store it in results[index].
    results[index] = fibonacci(n)


def run_multithreaded_round(numbers):
    #Runs one multithreaded round: uses one thread per number, waits for all,
    #returns the elapsed time in nanoseconds and the results

    results = [None] * len(numbers)
    threads = []

    t1 = time.perf_counter_ns()

    for i in range(len(numbers)):
        n = numbers[i]
        thread = threading.Thread(
            target=store_fib_results,
            args=(n, results, i),
            name=f"FibThread-{n}"
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    t2 = time.perf_counter_ns()
    return t2 - t1, results


def run_singlethread_round(numbers):
    #Runs one single-threaded round sequentially
    t1 = time.perf_counter_ns()
    results = [fibonacci(n) for n in numbers]
    t2 = time.perf_counter_ns()
    return t2 - t1, results


def main():

#1. Multithreaded Benchmark
    print("=== Fibonacci Computation With MultiThreading ===")
    print(f"Values: Fibonacci{NUMBERS}  |  Threads per round: {len(NUMBERS)}  |  Rounds: {ROUNDS}")
    print("=" * 78)
    print(f"{'Round':<8}{'T (nanoseconds)':<22}{'T (seconds)':<15}{'Results (F35, F38, F40)'}")
    print("-" * 78)

    mt_times_ns = []
    for round_num in range(1, ROUNDS + 1):
        elapsed_ns, results = run_multithreaded_round(NUMBERS)
        mt_times_ns.append(elapsed_ns)
        print(f"{round_num:<8}{elapsed_ns:<22,}{elapsed_ns / 1e9:<15.6f}{results}")

    mt_avg_ns = sum(mt_times_ns) / len(mt_times_ns)

    print("-" * 78)
    print(f"Average T over {ROUNDS} rounds : {mt_avg_ns:,.0f} ns  ({mt_avg_ns / 1e9:.6f} s)")
    print(f"Fastest round              : {min(mt_times_ns):,} ns")
    print(f"Slowest round              : {max(mt_times_ns):,} ns")
    print("=" * 78)
    print("\n")


#2. Non-Multithreaded Benchmark

    print("=== Fibonacci Computation Without MultiThreading ===")
    print(f" Values: Fibonacci{NUMBERS}  |  Rounds: {ROUNDS}")
    print("=" * 78)
    print(f"{'Round':<8}{'T (nanoseconds)':<22}{'T (seconds)':<15}{'Results (F35, F38, F40)'}")
    print("-" * 78)

    st_times_ns = []
    for round_num in range(1, ROUNDS + 1):
        elapsed_ns, results = run_singlethread_round(NUMBERS)
        st_times_ns.append(elapsed_ns)
        print(f"{round_num:<8}{elapsed_ns:<22,}{elapsed_ns / 1e9:<15.6f}{results}")

    st_avg_ns = sum(st_times_ns) / len(st_times_ns)

    print("-" * 78)
    print(f"Average T over {ROUNDS} rounds : {st_avg_ns:,.0f} ns  ({st_avg_ns / 1e9:.6f} s)")
    print(f"Fastest round              : {min(st_times_ns):,} ns")
    print(f"Slowest round              : {max(st_times_ns):,} ns")
    print("=" * 78)
    print("\n")

#3. Observation

    diff_percent = ((st_avg_ns - mt_avg_ns) / st_avg_ns) * 100

    print("=" * 78)
    print("=== BENCHMARK OBSERVATION ===")
    print("=" * 78)
    print(f"Observation: Multithreading reduced the average completion time by approximately {diff_percent:.1f}%.")
    print("=" * 78)


if __name__ == "__main__":
    main()