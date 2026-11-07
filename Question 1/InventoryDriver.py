import timeit
import matplotlib.pyplot as plt
import random

from hash_table import HashTable
from InventorySystem import Product

TABLE_SIZE = 101


class InventorySystem:

    def __init__(self, capacity=TABLE_SIZE):
        self.table = HashTable(capacity)

    def insert_product(self, product):
        self.table.insert(product.product_id, product)

    def search_product(self, product_id):
        return self.table.search(product_id)

    def edit_product(self, product_id, **fields):
        product = self.table.search(product_id)

        if product is None:
            return False

        for key, value in fields.items():
            if value is not None and hasattr(product, key):
                setattr(product, key, value)

        self.table.insert(product_id, product)
        return True

    def delete_product(self, product_id):
        return self.table.delete(product_id)

    def list_items(self):
        return [v for _, v in self.table.print_items()]


# Sample data
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

    for i in products:
        system.insert_product(i)


def arr_search(arr, key):
    for p in arr:
        if p.product_id == key:
            return p
    return None


def menu():
    print("=" * 20, end="")
    print("PHARMACY INVENTORY SYSTEM", end="")
    print("=" * 20)

    options = """
1. Insert a product
2. Search for a product (via Product ID)
3. Edit an existing product
4. Delete a product
5. List all products
6. Run Performance Benchmark (Hash Table vs Array)
7. Exit
    """
    print(options)
    print("=" * 65)


def new_product():
    product_id = input("Product ID: ").strip()
    name = input("Name: ").strip()
    category = input("Category: ").strip()
    price = float(input("Price (RM): ").strip())
    quantity = int(input("Quantity: ").strip())
    expiry_date = input("Expiry (YYYY-MM-DD): ").strip()
    manufacturer = input("Manufacturer: ").strip()

    return Product(product_id, name, category, price, quantity, expiry_date, manufacturer)


#Hash Table vs One-Dimensional Array Benchmark

def generate_products(n):
    names = ["Paracetamol", "Amoxicillin", "Cetirizine", "Vitamin C", "Ibuprofen", "Methylphenidate", "Omeprazole", "Loratadine", "Metformin"]
    categories = ['Analgesic', 'Antibiotic', 'Antihistamine', 'Supplement', 'Antacid', 'Analgesic', 'Antidiabetic','Stimulant']
    manufacturers = ["Duopharma", "Pharmaniaga", "CCM", "Novartis", "Nature's Way", "Hovid"]

    result = []
    for i in range(n):
        quantity = random.randint(30, 100)
        price = round(random.random(), 2) + random.randint(10, 20)
        result.append(
            Product(
                product_id=f"MED{i:06d}",
                name=f"{random.choice(names)}",
                category=f"{random.choice(categories)}",
                price=price,
                quantity=quantity,
                expiry_date="2026-10-21",
                manufacturer=f"{random.choice(manufacturers)}"
            )
        )
    return result


def run_performance_test(n, trials):
    products = generate_products(n)
    search_keys = [p.product_id for p in random.sample(products, min(trials, n))]

    # Ensure system capacity is sized correctly to accommodate n items
    b_system = InventorySystem(capacity=int(n * 2))

    for p in products:
        b_system.insert_product(p)

    def hash_time_search():
        for k in search_keys:
            b_system.search_product(k)

    def arr_time_search():
        for k in search_keys:
            arr_search(products, k)

    ht_time = min(timeit.repeat(hash_time_search, number=1, repeat=5))
    arr_time = min(timeit.repeat(arr_time_search, number=1, repeat=5))

    ratio = arr_time / ht_time if ht_time > 0 else 0

    print(f"N = {n:>6} records | {len(search_keys):>5} searches | "
          f"Hash Table: {ht_time * 1000:9.4f} ms | "
          f"Array: {arr_time * 1000:9.4f} ms | "
          f"Array is {ratio:6.1f}x SLOWER")

    return ht_time, arr_time


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
                product = new_product()
                system.insert_product(product)
                print(f"Inserted {product.product_id}, {product.name}")

            case 2:
                product_id = input("Enter Product ID: ").strip()
                result = system.search_product(product_id)
                print(f"Found: {result}" if result else f"{product_id} Not found.")

            case 3:
                product_id = input("Enter Product ID: ").strip()
                if system.search_product(product_id) is None:
                    print(f"{product_id} Not found.")
                    continue

                print("Leave a field blank to keep its current value.")
                name = input("New name         : ").strip() or None

                try:
                    new_price = float(input("New price    : ").strip())
                except ValueError:
                    new_price = None

                try:
                    new_quantity = float(input("New quantity : ").strip())
                except ValueError:
                    new_quantity = None

                new_manufacturer = input("New manufacturer: ").strip() or None

                updated = system.edit_product(product_id, name=name, price=new_price, quantity=new_quantity,
                                              manufacturer=new_manufacturer)
                print("Updated." if updated else "Not found.")

            case 4:
                product_id = input("Input Product ID: ").strip()
                deleted = system.delete_product(product_id)
                print("Deleted." if deleted else "Not found.")

            case 5:
                products = system.list_items()
                print(f"{len(products)} products available:")
                for p in products:
                    print(" " + str(p))

            case 6:
                print("\n" + "=" * 95)
                print("PERFORMANCE BENCHMARK: HASH TABLE vs. ONE-DIMENSIONAL ARRAY")
                print("=" * 95)
                for n in [100, 500, 1000, 5000, 10000, 50000]:
                    run_performance_test(n, trials=min(n, 2000))
                print("=" * 95)
                input("\nBenchmark complete. Press Enter to return to the main menu...")

            case 7:
                print("Exiting System...")
                break

            case _:
                print("Invalid option, please try again.")


if __name__ == "__main__":
    main()