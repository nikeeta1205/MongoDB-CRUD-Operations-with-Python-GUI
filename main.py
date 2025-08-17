import tkinter as tk
from tkinter import messagebox, ttk
from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")
db = client["RestaurantData"]
collection = db["menu"]


root = tk.Tk()
root.title("Restaurant Menu Management")
root.geometry("650x500")
root.config(bg="#f4f4f4")


title_label = tk.Label(root, text="503 - Nikeeta Sawant\nRestaurant CRUD Application",
                       font=("Helvetica", 18, "bold"), bg="#f4f4f4", fg="#2c3e50", justify="center")
title_label.pack(pady=15)


form_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove", padx=20, pady=20)
form_frame.pack(pady=10, fill="x", padx=20)


tk.Label(form_frame, text="Dish ID:", font=("Arial", 12), bg="#ffffff").grid(row=0, column=0, sticky="w", pady=5)
id_entry = ttk.Entry(form_frame, width=30)
id_entry.grid(row=0, column=1, pady=5)


tk.Label(form_frame, text="Dish Name:", font=("Arial", 12), bg="#ffffff").grid(row=1, column=0, sticky="w", pady=5)
name_entry = ttk.Entry(form_frame, width=30)
name_entry.grid(row=1, column=1, pady=5)


tk.Label(form_frame, text="Price (₹):", font=("Arial", 12), bg="#ffffff").grid(row=2, column=0, sticky="w", pady=5)
price_entry = ttk.Entry(form_frame, width=30)
price_entry.grid(row=2, column=1, pady=5)


tk.Label(form_frame, text="Category:", font=("Arial", 12), bg="#ffffff").grid(row=3, column=0, sticky="w", pady=5)
category_combo = ttk.Combobox(form_frame, width=28, values=["Starter", "Main Course", "Dessert", "Drink"])
category_combo.grid(row=3, column=1, pady=5)



def insert():
    dish_id = id_entry.get().strip()
    name = name_entry.get().strip()
    price = price_entry.get().strip()
    category = category_combo.get().strip()

    if not (dish_id and name and price and category):
        messagebox.showwarning("Missing Data", "Please fill all fields.")
        return

    try:
        collection.insert_one({
            "dish_id": dish_id,
            "name": name,
            "price": price,
            "category": category
        })
        messagebox.showinfo("Success", f"Dish '{name}' added to menu!")
        id_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        category_combo.set("")
    except:
        messagebox.showerror("Error", "Failed to insert data.")



def read():
    try:
        documents = collection.find()
        result = ""
        for doc in documents:
            result += f"🍽️ {doc['name']}  (ID: {doc['dish_id']})\n   Price: ₹{doc['price']} | Category: {doc['category']}\n\n"
        result_label.config(text=result)
    except:
        messagebox.showerror("Error", "Failed to display data.")



def update():
    update_win = tk.Toplevel(root)
    update_win.title("Update Dish")
    update_win.geometry("400x300")
    update_win.config(bg="#ecf0f1")

    tk.Label(update_win, text="Enter Dish Name to Update:", font=("Arial", 12), bg="#ecf0f1").pack(pady=10)
    name_input = ttk.Entry(update_win, width=30)
    name_input.pack()

    tk.Label(update_win, text="New Price (₹):", font=("Arial", 12), bg="#ecf0f1").pack(pady=10)
    price_input = ttk.Entry(update_win, width=30)
    price_input.pack()

    tk.Label(update_win, text="New Category:", font=("Arial", 12), bg="#ecf0f1").pack(pady=10)
    category_input = ttk.Combobox(update_win, width=28, values=["Starter", "Main Course", "Dessert", "Drink"])
    category_input.pack()

    def updateinfo():
        old_name = name_input.get()
        new_price = price_input.get()
        new_category = category_input.get()

        if not (old_name and new_price and new_category):
            messagebox.showwarning("Missing Data", "All fields are required!")
            return

        result = collection.update_one({"name": old_name}, {"$set": {"price": new_price, "category": new_category}})
        if result.modified_count > 0:
            messagebox.showinfo("Success", "Dish updated successfully!")
            update_win.destroy()
        else:
            messagebox.showinfo("No Match", "No matching dish found.")

    ttk.Button(update_win, text="Confirm Update", command=updateinfo).pack(pady=20)



def delete():
    delete_win = tk.Toplevel(root)
    delete_win.title("Delete Dish")
    delete_win.geometry("350x200")
    delete_win.config(bg="#fdebd0")

    tk.Label(delete_win, text="Enter Dish ID to Delete:", font=("Arial", 12), bg="#fdebd0").pack(pady=10)
    id_input = ttk.Entry(delete_win, width=30)
    id_input.pack()

    def deleteInfo():
        old_id = id_input.get()
        result = collection.delete_many({"dish_id": old_id})

        if result.deleted_count > 0:
            messagebox.showinfo("Success", "Dish deleted successfully!")
            delete_win.destroy()
        else:
            messagebox.showinfo("No Match", "No matching dish found.")

    ttk.Button(delete_win, text="Confirm Delete", command=deleteInfo).pack(pady=20)



btn_frame = tk.Frame(root, bg="#f4f4f4")
btn_frame.pack(pady=15)

ttk.Button(btn_frame, text="Add Dish", command=insert).grid(row=0, column=0, padx=10)
ttk.Button(btn_frame, text="Show Menu", command=read).grid(row=0, column=1, padx=10)
ttk.Button(btn_frame, text="Update Dish", command=update).grid(row=0, column=2, padx=10)
ttk.Button(btn_frame, text="Delete Dish", command=delete).grid(row=0, column=3, padx=10)


result_label = tk.Label(root, text="", justify="left", anchor="w", bg="#f4f4f4", fg="#34495e", font=("Courier", 11))
result_label.pack(pady=10, fill="both", expand=True)

root.mainloop()
