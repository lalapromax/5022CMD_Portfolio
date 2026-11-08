
import timeit
import random
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from hash_table import HashTable
from Products import Product


TABLE_SIZE = 101
BENCHMARK_SIZES = [100, 500, 1000, 5000, 10000, 50000]


# ==========================================
# INVENTORY SYSTEM
# ==========================================

class InventorySystem:

    def __init__(self, capacity=TABLE_SIZE):
        self.table = HashTable(capacity)

    def insert_product(self, product):
        if self.search_product(product.product_id) is not None:
            return False

        self.table.insert(product.product_id, product)
        return True

    def search_product(self, product_id):
        return self.table.search(product_id)

    def edit_product(self, product_id, **fields):
        product = self.search_product(product_id)

        if product is None:
            return False

        for key, value in fields.items():
            if value is not None and hasattr(product, key):
                setattr(product, key, value)

        return True

    def delete_product(self, product_id):
        return self.table.delete(product_id)

    def list_items(self):
        return [product for _, product in self.table.print_items()]


# ==========================================
# SAMPLE INVENTORY DATA
# ==========================================

def seed_data(system):

    products = [
        Product("MED1001", "Paracetamol 500mg", "Analgesic", 5.90, 200, "2027-05-01", "Duopharma"),
        Product("MED1002", "Amoxicillin 250mg", "Antibiotic", 12.50, 150, "2026-12-15", "Pharmaniaga"),
        Product("MED1003", "Cetirizine 10mg", "Antihistamine", 8.20, 100, "2027-02-20", "CCM"),
        Product("MED1004", "Vitamin C 1000mg", "Supplement", 15.00, 300, "2028-01-10", "Nature's Way"),
        Product("MED1005", "Omeprazole 20mg", "Antacid", 18.90, 80, "2026-11-05", "Hovid"),
        Product("MED1006", "Ibuprofen 400mg", "Analgesic", 7.50, 120, "2027-07-18", "Duopharma"),
        Product("MED1007", "Loratadine 10mg", "Antihistamine", 9.80, 90, "2027-03-30", "CCM"),
        Product("MED1008", "Metformin 500mg", "Antidiabetic", 10.20, 200, "2026-10-22", "Pharmaniaga"),
    ]

    for product in products:
        system.insert_product(product)


# ==========================================
# INVENTORY MENU
# ==========================================

def menu():

    print()
    print("=" * 20 + " PHARMACY INVENTORY SYSTEM " + "=" * 20)

    print("""
1. Insert a product
2. Search for a product
3. Edit an existing product
4. Delete a product
5. List all products
6. Run Performance Benchmark
7. Exit
""")

    print("=" * 65)


def new_product():

    product_id = input("Product ID: ").strip()
    name = input("Name: ").strip()
    category = input("Category: ").strip()
    price = float(input("Price (RM): "))
    quantity = int(input("Quantity: "))
    expiry_date = input("Expiry (YYYY-MM-DD): ").strip()
    manufacturer = input("Manufacturer: ").strip()

    return Product(
        product_id, name, category, price,
        quantity, expiry_date, manufacturer
    )


# ==========================================
# PERFORMANCE BENCHMARK
# ==========================================

def generate_products(n):

    names = [
        "Paracetamol", "Amoxicillin", "Cetirizine",
        "Vitamin C", "Ibuprofen", "Methylphenidate",
        "Omeprazole", "Loratadine", "Metformin"
    ]

    categories = [
        "Analgesic", "Antibiotic", "Antihistamine",
        "Supplement", "Antacid", "Antidiabetic",
        "Stimulant"
    ]

    manufacturers = [
        "Duopharma", "Pharmaniaga", "CCM",
        "Novartis", "Nature's Way", "Hovid"
    ]

    products = []

    for i in range(n):

        product = Product(
            product_id=f"MED{i:06d}",
            name=random.choice(names),
            category=random.choice(categories),
            price=round(random.uniform(10, 20), 2),
            quantity=random.randint(30, 100),
            expiry_date="2026-10-21",
            manufacturer=random.choice(manufacturers)
        )

        products.append(product)

    return products


def arr_search(arr, key):

    for product in arr:
        if product.product_id == key:
            return product

    return None


def run_performance_test(n, trials):
    #Runs the benchmark test
    products = generate_products(n)

    search_keys = [
        product.product_id
        for product in random.sample(products, min(trials, n))
    ]

    # Build hash table
    hash_system = InventorySystem(capacity=n * 2)

    for product in products:
        hash_system.insert_product(product)

    # Benchmark search operations
    def hash_search():
        for key in search_keys:
            hash_system.search_product(key)

    def array_search():
        for key in search_keys:
            arr_search(products, key)

    hash_time = min(timeit.repeat(hash_search, number=1, repeat=5))

    array_time = min(timeit.repeat(array_search, number=1, repeat=5))

    ratio = array_time / hash_time if hash_time > 0 else 0

    print(
        f"N = {n:>6} | "
        f"Searches = {len(search_keys):>5} | "
        f"Hash Table = {hash_time * 1000:9.4f} ms | "
        f"Array = {array_time * 1000:9.4f} ms | "
        f"Array is {ratio:6.1f}x slower"
    )

    return hash_time, array_time


def plot_performance(sizes, hash_times, array_times):

    plt.figure(figsize=(8, 5))

    plt.plot(
        sizes, hash_times,
        marker="o",
        label="Hash Table (open addressing)"
    )

    plt.plot(
        sizes, array_times,
        marker="s",
        label="1D Array (linear search)"
    )

    plt.xlabel("Number of records (N)")
    plt.ylabel("Total search time (ms)")
    plt.title("Search Performance: Hash Table vs. One-Dimensional Array")

    plt.xscale("log")
    plt.yscale("log")

    # Display normal numbers instead of 10^x
    ax = plt.gca()
    ax.xaxis.set_major_formatter(
        FuncFormatter(lambda x, _: f"{x:,.0f}")
    )
    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda y, _: f"{y:,.0f}")
    )

    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig("hash_vs_array_performance.png", dpi=150)
    plt.show()

    print("\nChart saved as hash_vs_array_performance.png")


def run_benchmark():

    hash_times = []
    array_times = []

    print("\n" + "=" * 95)
    print("PERFORMANCE BENCHMARK: HASH TABLE vs. ONE-DIMENSIONAL ARRAY")
    print("=" * 95)

    for n in BENCHMARK_SIZES:

        trials = min(n, 2000)

        hash_time, array_time = run_performance_test(n, trials)

        hash_times.append(hash_time * 1000)
        array_times.append(array_time * 1000)

    print("=" * 95)

    plot_performance(
        BENCHMARK_SIZES,
        hash_times,
        array_times
    )


# ==========================================
# MAIN PROGRAM
# ==========================================

def main():

    system = InventorySystem()
    seed_data(system)

    while True:

        menu()

        try:
            choice = int(input("Select an option: ").strip())

        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue

        match choice:

            case 1:
                try:
                    product = new_product()

                    inserted = system.insert_product(product)

                    if inserted:
                        print(f"Inserted {product.product_id}, {product.name}")
                    else:
                        print(f"Product ID {product.product_id} already exists!")

                except ValueError:
                    print("Invalid price or quantity.")


            case 2:
                product_id = input("Enter Product ID: ").strip()
                result = system.search_product(product_id)

                print(f"Found: {result}" if result else "Product not found.")

            case 3:
                product_id = input("Enter Product ID: ").strip()

                if system.search_product(product_id) is None:
                    print("Product not found.")
                    continue

                print("Leave a field blank to keep its current value.")

                name = input("New name: ").strip() or None
                manufacturer = input("New manufacturer: ").strip() or None

                try:
                    price_input = input("New price: ").strip()
                    new_price = float(price_input) if price_input else None

                    quantity_input = input("New quantity: ").strip()
                    new_quantity = int(quantity_input) if quantity_input else None

                except ValueError:
                    print("Invalid price or quantity.")
                    continue

                system.edit_product(
                    product_id,
                    name=name,
                    price=new_price,
                    quantity=new_quantity,
                    manufacturer=manufacturer
                )

                print("Product updated.")

            case 4:
                product_id = input("Enter Product ID: ").strip()

                deleted = system.delete_product(product_id)

                print("Deleted." if deleted else "Product not found.")

            case 5:
                products = system.list_items()

                print(f"\n{len(products)} products available:")

                for product in products:
                    print(product)

            case 6:
                run_benchmark()

            case 7:
                print("Exiting system...")
                break

            case _:
                print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
