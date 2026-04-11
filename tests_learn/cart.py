class ShoppingCart:
    def __init__(self):
        # Stores items as {item_name: {"price": float, "quantity": int}}
        self.items = {}

    def add_item(self, name, price, quantity=1):           #### cola. 10$, 3
        if name in self.items:
            self.items[name]["quantity"] += quantity
        else:
            self.items[name] = {"price": price, "quantity": quantity}

    def remove_item(self, name, quantity=1):
        if name in self.items:
            self.items[name]["quantity"] -= quantity
            if self.items[name]["quantity"] <= 0:
                del self.items[name]

    def get_total(self):
        total = 0
        for item in self.items.values():
            total += item["price"] * item["quantity"]
        return total


my_cart = ShoppingCart()
