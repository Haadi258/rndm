import tkinter as tk
from tkinter import messagebox
import pickle
from datetime import datetime

class Product:
    def __init__(self, name, price=0, weight=0):
        self.name = name
        self.price = price
        self.weight = weight
        self.purchase_history = []

    def add_purchase(self, date, price, weight):
        self.purchase_history.append((date, price, weight))

    def total_cost(self):
        total_price = sum([purchase[1] for purchase in self.purchase_history])
        total_weight = sum([purchase[2] for purchase in self.purchase_history])
        return total_price, total_weight

    def purchase_count(self):
        return len(self.purchase_history)

    def __str__(self):
        total_price, total_weight = self.total_cost()
        purchase_dates = ", ".join([purchase[0].split()[0] for purchase in self.purchase_history])  # Extracting only date without time
        return f"Name: {self.name}, Total Price: {total_price}, Total Weight: {total_weight}, Purchased {self.purchase_count()} times on: {purchase_dates}"

class ProductList:
    def __init__(self):
        self.products = {}

    def add_product(self, product):
        if product.name in self.products:
            existing_product = self.products[product.name]
            for purchase in product.purchase_history:
                existing_product.add_purchase(*purchase)
        else:
            self.products[product.name] = product

    def remove_product(self, product_name):
        if product_name in self.products:
            del self.products[product_name]

class ProductManager:
    def __init__(self):
        self.lists = {}
        self.load_data()

    def add_product_to_list(self, list_name, product):
        if list_name not in self.lists:
            self.lists[list_name] = ProductList()
        self.lists[list_name].add_product(product)

    def remove_product_from_list(self, list_name, product_name):
        if list_name in self.lists:
            self.lists[list_name].remove_product(product_name)

    def save_data(self):
        with open("products_data.pkl", "wb") as file:
            pickle.dump(self.lists, file)

    def load_data(self):
        try:
            with open("products_data.pkl", "rb") as file:
                self.lists = pickle.load(file)
        except FileNotFoundError:
            pass

class ProductApp:
    def __init__(self, root):
        self.root = root
        self.product_manager = ProductManager()
        self.create_widgets()

    def create_widgets(self):
        self.root.title("Product Manager")
        self.root.geometry("400x400")

        self.label_name = tk.Label(self.root, text="Product Name:")
        self.label_name.pack()

        self.entry_name = tk.Entry(self.root)
        self.entry_name.pack()

        self.label_price = tk.Label(self.root, text="Price:")
        self.label_price.pack()

        self.entry_price = tk.Entry(self.root)
        self.entry_price.pack()

        self.label_weight = tk.Label(self.root, text="Weight:")
        self.label_weight.pack()

        self.entry_weight = tk.Entry(self.root)
        self.entry_weight.pack()

        self.label_list = tk.Label(self.root, text="List Name:")
        self.label_list.pack()

        self.entry_list = tk.Entry(self.root)
        self.entry_list.pack()

        self.search_label = tk.Label(self.root, text="Search Product:")
        self.search_label.pack()

        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack()

        self.add_button = tk.Button(self.root, text="Add Product", command=self.add_product)
        self.add_button.pack()

        self.show_all_button = tk.Button(self.root, text="Show All Products", command=self.show_all_products)
        self.show_all_button.pack()

        self.save_button = tk.Button(self.root, text="Save Data", command=self.save_data)
        self.save_button.pack()

        self.search_button = tk.Button(self.root, text="Search Product", command=self.search_product)
        self.search_button.pack()

    def add_product(self):
        product_name = self.entry_name.get().strip()
        product_price = float(self.entry_price.get().strip())
        product_weight = float(self.entry_weight.get().strip())

        list_name = self.entry_list.get().strip()
        if not list_name:
            messagebox.showwarning("Warning", "Please enter a list name.")
            return

        if product_name:
            product = Product(product_name, product_price, product_weight)
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            product.add_purchase(current_date, product_price, product_weight)
            self.product_manager.add_product_to_list(list_name, product)
            messagebox.showinfo("Success", "Product added successfully!")
        else:
            messagebox.showwarning("Warning", "Please enter a product name.")

    def show_all_products(self):
        list_name = self.entry_list.get().strip()
        if not list_name:
            messagebox.showwarning("Warning", "Please enter a list name.")
            return

        if list_name in self.product_manager.lists:
            products = self.product_manager.lists[list_name].products
            if products:
                product_info = "\n".join([str(product) for product in products.values()])
                messagebox.showinfo("Products", product_info)
            else:
                messagebox.showinfo("Products", "No products in this list.")
        else:
            messagebox.showwarning("Warning", "List does not exist.")

    def save_data(self):
        self.product_manager.save_data()
        messagebox.showinfo("Success", "Data saved successfully!")

    def search_product(self):
        product_name = self.search_entry.get().strip()
        list_name = self.entry_list.get().strip()
        if not list_name:
            messagebox.showwarning("Warning", "Please enter a list name.")
            return

        if product_name and list_name in self.product_manager.lists:
            products = self.product_manager.lists[list_name].products
            if product_name in products:
                product_info = str(products[product_name])
                messagebox.showinfo("Product Info", product_info)
            else:
                messagebox.showinfo("Product Info", "Product not found in this list.")
        else:
            messagebox.showwarning("Warning", "Please enter a product name and a list name.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductApp(root)
    root.mainloop()
