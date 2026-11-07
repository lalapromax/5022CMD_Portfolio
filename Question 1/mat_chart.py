import matplotlib.pyplot as plt

from InventoryDriver import run_performance_test

sizes = [100, 500, 1000, 5000, 10000, 50000]
ht_times, arr_times = [], []

for n in sizes:
    trials = min(n, 2000)
    ht_t, arr_t = run_performance_test(n, trials)
    ht_times.append(ht_t * 1000)   # ms
    arr_times.append(arr_t * 1000)  # ms

plt.figure(figsize=(8, 5))
plt.plot(sizes, ht_times, marker="o", label="Hash Table (open addressing)")
plt.plot(sizes, arr_times, marker="s", label="1D Array (linear search)")
plt.xlabel("Number of records (N)")
plt.ylabel("Total search time (ms)")
plt.title("Search Performance: Hash Table vs. One-Dimensional Array")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("hash_vs_array_performance.png", dpi=150)
print("Saved chart to hash_vs_array_performance.png")