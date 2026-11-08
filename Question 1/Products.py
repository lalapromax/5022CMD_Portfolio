
#Product Class
class Product:

    def __init__(self, product_id:str, name:str, category:str, price:float, quantity:int, expiry_date:str, manufacturer:str):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity
        self.expiry_date = expiry_date
        self.manufacturer= manufacturer

    def __str__(self):
        return(
            f"ID: {self.product_id:<5} | Name: {self.name:<20} | Category: {self.category:<15} |"
            f"RM {self.price:>7.2f} | Qty: {self.quantity:>4} | "
            f"Exp: {self.expiry_date} | Mfr: {self.manufacturer}"

        )

