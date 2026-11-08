
#Product Class
class Product:

    def __init__(self, product_id, name, category, price, quantity, expiry_date, manufacturer):
        self.product_id = product_id.upper()
        self.name = name
        self.category = category
        self.price = float(price)
        self.quantity = int(quantity)
        self.expiry_date = expiry_date
        self.manufacturer= manufacturer

    def __str__(self):
        return(
            f"ID: {self.product_id:<5} | Name: {self.name:<20} | Category: {self.category:<15} |"
            f"RM {self.price:>7.2f} | Qty: {self.quantity:>4} | "
            f"Exp: {self.expiry_date} | Mfr: {self.manufacturer}"

        )

