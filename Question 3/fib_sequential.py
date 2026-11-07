
import time

from fibonacci import fibonacci

NUMBERS = (35, 38, 40)
ROUNDS = 10


def run_one_round(numbers):
    t1 = time.perf_counter_ns()                 # t1 - start time
    results = [fibonacci(n) for n in numbers]   # calculated one at a time
    t2 = time.perf_counter_ns()                 # t2 - end time

    elapsed_ns = t2 - t1
    return elapsed_ns, results


def main():
    print("=" * 78)
    print("=== Fibonacci Computation Without MultiThreading ===")
    print(f" Values: Fibonacci{NUMBERS}  |  Rounds: {ROUNDS}")
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
