import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog

# Initial inventory levels
inventory = {
    'Beef': 20,
    'Premium Chicken': 20,
    'Hot Buffalo Sauce': 20,
    'Jalapeno Peppers': 20,
    'Onions': 20,
    'Banana Peppers': 20,
    'Diced Tomatoes': 20,
    'Black Olives': 20,
    'Green Olives': 20,
    'Mushrooms': 20,
    'Pineapple': 20,
    'Cheddar Cheese Blend': 20,
    'Green Peppers': 20,
    'Spinach': 20,
    'Feta Cheese': 20,
    'Shredded Parmesan Asiago': 20,
}

pizza_orders = []

# Pizza data (size, toppings, price)
pizza_data = {
    'small': {'price': 5, 'toppings':  list(inventory.keys())},
    'medium': {'price': 7, 'toppings': list(inventory.keys())},
    'large': {'price': 10, 'toppings': list(inventory.keys())}
}

# Additional pizza customizations
crusts = ['Hand Tossed', 'Crunchy Thin Crust', 'Brooklyn Style']
sauces = ['Parmesan', 'Robust Inspired Tomato Sauce', 'Hearty Marinara Sauce', 'Honey BBQ Sauce', 'Garlic Parmesan Sauce', 'Alfredo Sauce', 'Ranch', 'No Sauce']
cheeses = ['Light', 'Normal', 'Extra']

# Calculate total inventory cost
total_inventory_cost = sum(inventory[item] * 1 for item in inventory)  # Assuming each item costs $1

# Calculate total profit from pizzas
total_pizza_profit = sum(pizza_data[size]['price'] for size in pizza_data)  # Total profit from all pizzas

# Calculate break-even point
break_even_point = total_inventory_cost / (total_pizza_profit - total_inventory_cost)

root = tk.Tk()
root.title("Pizza Place Ordering System")

# Set window size and font size
root.geometry("1200x600")
root.option_add("*Font", "Arial 12")
root.option_add("*Foreground", "black")  # Change font color to black

# Create frames
menu_frame = tk.Frame(root, bg="lightblue")
order_frame = tk.Frame(root, bg="lightgreen")
vendor_frame = tk.Frame(root, bg="lightcoral")
stats_frame = tk.Frame(root, bg="lightyellow")

# Pack frames
menu_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
order_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
vendor_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
stats_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

def order_pizza(size, crust, sauce, cheese, toppings):
    global inventory, total_inventory_cost, total_pizza_profit, break_even_point, pizza_orders
    if size in pizza_data and all(topping in inventory for topping in toppings):
        cost = pizza_data[size]['price'] + len(toppings) * 1  # Each topping costs 1
        if all(inventory[topping] > 0 for topping in toppings):
            # Create pizza order data
            pizza_order = {'size': size, 'crust': crust, 'sauce': sauce, 'cheese': cheese, 'toppings': toppings, 'cost': cost}
            pizza_orders.append(pizza_order)

            messagebox.showinfo("Order Confirmation", f"Ordered {size} pizza with {crust} crust, {sauce} sauce, {cheese} cheese, and {', '.join(toppings)} toppings.")

            for topping in toppings:
                inventory[topping] -= 1
            update_inventory_display()
            update_order_display()

            # Deselect all toppings
            for var in toppings_vars:
                var.set(0)

            size_var.set("Select Size")
            crust_var.set("Select Crust")
            sauce_var.set("Select Sauce")
            cheese_var.set("Select Cheese")

            # Update statistics
            total_inventory_cost = sum(inventory[item] * 1 for item in inventory)
            total_pizza_profit = sum(pizza_data[size]['price'] for size in pizza_data)
            break_even_point = total_inventory_cost / (total_pizza_profit - total_inventory_cost)
            update_statistics()

            # Hide the re-order and select buttons
            reorder_button.pack_forget()
            select_button.pack_forget()
        else:
            messagebox.showerror("Error", "Out of stock for selected toppings")
    else:
        messagebox.showerror("Error", "Invalid pizza size or topping selection")

# User Agreement
user_agreement = """
<HARPS USER AGREEMENT>

By using this application, you agree to the following terms:

1. You will not sell or distribute any data from this application without the express consent of Forestview.\n
2. Forestview is not liable for any damages resulting from data breaches, zero-day attacks, or database worms, such as SQL injection.\n
3. You acknowledge that Forestview performs periodic vulnerability assessments against this system and demands the same preventive actions from all key vendors.\n
4. You understand that these requirements may change over time as technology and the overall security landscape changes.\n
"""
if not messagebox.askokcancel("User Agreement", user_agreement):
    exit()

def update_statistics():
    global total_inventory_cost, total_pizza_profit, break_even_point
    # Calculate total inventory cost
    total_inventory_cost = sum(inventory[item] * 1 for item in inventory)

    # Calculate total profit from pizzas
    total_pizza_profit = sum(order['cost'] for order in pizza_orders)

    # Calculate break-even point
    if total_pizza_profit - total_inventory_cost != 0:
        break_even_point = total_inventory_cost / (total_pizza_profit - total_inventory_cost)
    else:
        break_even_point = 0

    # Display statistics
    inventory_cost_label.config(text=f"Total Inventory Cost: ${total_inventory_cost}")
    profit_label.config(text=f"Total Profit from Pizzas: ${total_pizza_profit}")
    break_even_label.config(text=f"Break-even Point: {break_even_point:.2f} pizzas")

def update_inventory_display():
    for widget in vendor_frame.winfo_children():
        widget.destroy()

    vendor_label = tk.Label(vendor_frame, text="Vendor Information", bg="lightcoral", font=("Arial", 16, "bold"))
    vendor_label.pack()

    for item, quantity in inventory.items():
        label_text = f"{item.capitalize()}: {quantity}"
        item_label = tk.Label(vendor_frame, text=label_text,bg="lightcoral", font=("Arial", 12))
        item_label.pack()

def update_order_display():
    order_listbox.delete('1.0', 'end')  # Clear the ScrolledText
    total_cost = sum(order['cost'] for order in pizza_orders)
    for i, order in enumerate(pizza_orders, start=1):
        order_text = f"Order {i}: {order['size']} pizza with {order['crust']} crust, {order['sauce']} sauce, {order['cheese']} cheese, and {', '.join(order['toppings'])} toppings - ${order['cost']}"
        order_listbox.insert(tk.END, order_text + '\n')
    total_cost_label.config(text=f"Total Cost: ${total_cost}")

def cancel_order():
    """
    Cancel an order based on user input.
    """
    order_number = simpledialog.askinteger("Cancel Order", "Enter the order number to cancel:")
    if order_number is not None and 1 <= order_number <= len(pizza_orders):
        cancelled_order = pizza_orders.pop(order_number - 1)
        for topping in cancelled_order['toppings']:
            inventory[topping] += 1  # Add the toppings back to the inventory
        update_order_display()
        update_statistics()
    else:
        messagebox.showerror("Error", "Invalid order number")


def order_pizza(size, crust, sauce, cheese, toppings):
    global inventory, total_inventory_cost, total_pizza_profit, break_even_point, pizza_orders
    if size in pizza_data and all(topping in inventory for topping in toppings):
        cost = pizza_data[size]['price'] + len(toppings) * 1.5  # Each topping costs 1.5
        if all(inventory[topping] > 0 for topping in toppings):
            # Create pizza order data
            pizza_order = {'size': size, 'crust': crust, 'sauce': sauce, 'cheese': cheese, 'toppings': toppings, 'cost': cost}
            pizza_orders.append(pizza_order)

            messagebox.showinfo("Order Confirmation", f"Ordered {size} pizza with {crust} crust, {sauce} sauce, {cheese} cheese, and {', '.join(toppings)} toppings.")

            for topping in toppings:
                inventory[topping] -= 1
            update_inventory_display()
            update_order_display()

            # Deselect all toppings
            for var in toppings_vars:
                var.set(0)

            size_var.set("Select Size")
            crust_var.set("Select Crust")
            sauce_var.set("Select Sauce")
            cheese_var.set("Select Cheese")

            # Update statistics
            total_inventory_cost = sum(inventory[item] * 1 for item in inventory)
            total_pizza_profit = sum(pizza_data[size]['price'] for size in pizza_data)
            break_even_point = total_inventory_cost / (total_pizza_profit - total_inventory_cost)
            update_statistics()

            # Hide the re-order and select buttons
            reorder_button.pack_forget()
            select_button.pack_forget()
        else:
            messagebox.showerror("Error", "Out of stock for selected toppings")
    else:
        messagebox.showerror("Error", "Invalid pizza size or topping selection")


def re_order_ingredient(ingredient):
    global inventory
    if inventory.get(ingredient, 0) < 5:
        inventory[ingredient] = 20
        update_inventory_display()
        update_statistics()
        messagebox.showinfo("Re-Order", f"Re-ordered {ingredient}")
    else:
        messagebox.showinfo("Re-Order", f"{ingredient} inventory level is sufficient (>= 5)")

reorder_button = tk.Button(vendor_frame, text="Re-Order", command=lambda: re_order_ingredient(selected_ingredient), bg="white", fg="black", font=("Arial", 12, "bold"))

def select_ingredient(ingredient):
    global selected_ingredient
    selected_ingredient = ingredient

ingredient_listbox = tk.Listbox(vendor_frame, width=40, bg="lightcoral", font=("Arial", 12))

# Button for re-ordering ingredients
reorder_button.pack()
select_button = tk.Button(vendor_frame, text="Select Ingredient", command=lambda: select_ingredient(ingredient_listbox.get(tk.ACTIVE)), bg="white", fg="black", font=("Arial", 12, "bold"))

select_button.pack()

menu_label = tk.Label(menu_frame, text="Menu", bg="lightblue", font=("Arial", 16, "bold"))
menu_label.pack()

size_label = tk.Label(menu_frame, text="Size:", bg="lightblue", font=("Arial", 12))
size_label.pack()
size_var = tk.StringVar()
size_var.set("Select Size")

size_option = tk.OptionMenu(menu_frame, size_var, "small","medium","large")
size_option.config(font=("Arial", 12))
size_option.pack()

crust_label = tk.Label(menu_frame, text="Crust:", bg="lightblue", font=("Arial", 12))
crust_label.pack()
crust_var = tk.StringVar()
crust_var.set("Select Crust")

crust_option = tk.OptionMenu(menu_frame, crust_var, *crusts)
crust_option.config(font=("Arial", 12))
crust_option.pack()

sauce_label = tk.Label(menu_frame, text="Sauce:", bg="lightblue", font=("Arial", 12))
sauce_label.pack()
sauce_var = tk.StringVar()
sauce_var.set("Select Sauce")

sauce_option = tk.OptionMenu(menu_frame, sauce_var, *sauces)
sauce_option.config(font=("Arial", 12))
sauce_option.pack()

cheese_label = tk.Label(menu_frame, text="Cheese:", bg="lightblue", font=("Arial", 12))
cheese_label.pack()
cheese_var = tk.StringVar()
cheese_var.set("Select Cheese")

cheese_option = tk.OptionMenu(menu_frame, cheese_var, *cheeses)
cheese_label.pack()
cheese_var = tk.StringVar()
cheese_var.set("Select Cheese")

cheese_option = tk.OptionMenu(menu_frame, cheese_var, *cheeses)
cheese_option.config(font=("Arial", 12))
cheese_option.pack()

toppings_label = tk.Label(menu_frame, text="Toppings:", bg="lightblue", font=("Arial",12))
toppings_label.pack()
toppings_vars = []

for topping in list(inventory.keys()):
    var = tk.IntVar()
    toppings_vars.append(var)
    topping_check = tk.Checkbutton(menu_frame, text=topping, variable=var, bg="lightblue", font=("Arial", 12))
    topping_check.pack()

order_button = tk.Button(menu_frame, text="Order", command=lambda: order_pizza(size_var.get(), crust_var.get(), sauce_var.get(), cheese_var.get(), [topping for topping, var in zip(list(inventory.keys()), toppings_vars) if var.get() == 1]), bg="white", fg="black", font=("Arial", 12, "bold"))
order_button.pack()

order_label = tk.Label(order_frame, text="Order Details", bg="lightgreen", font=("Arial", 16, "bold"))
order_label.pack()

order_listbox = scrolledtext.ScrolledText(order_frame, width=40, height=10, bg="black", fg="white")
order_listbox.pack()

cancel_button = tk.Button(order_frame, text="Cancel Order", command=cancel_order, bg="white", fg="black", font=("Arial", 12, "bold"))
cancel_button.pack()

total_cost_label = tk.Label(order_frame, text="Total Cost: $0", bg="lightgreen", font=("Arial", 12))
total_cost_label.pack()

vendor_label = tk.Label(vendor_frame, text="Vendor Information", bg="lightcoral", font=("Arial", 16, "bold"))
vendor_label.pack()

selected_ingredient = ""

ingredient_listbox = tk.Listbox(vendor_frame, width=40, bg="lightcoral", font=("Arial", 12))

for ingredient in inventory:
    ingredient_listbox.insert(tk.END, ingredient)

ingredient_listbox.pack()

stats_label = tk.Label(stats_frame, text="Statistics", bg="lightyellow", font=("Arial", 16, "bold"))
stats_label.pack()

inventory_cost_label = tk.Label(stats_frame, text=f"Total Inventory Cost: ${total_inventory_cost}", bg="lightyellow", font=("Arial", 12))
inventory_cost_label.pack()

profit_label = tk.Label(stats_frame, text=f"Total Profit from Pizzas: ${total_pizza_profit}", bg="lightyellow", font=("Arial", 12))
profit_label.pack()

break_even_label = tk.Label(stats_frame, text=f"Break-even Point: {break_even_point:.2f} pizzas", bg="lightyellow", font=("Arial", 12))
break_even_label.pack()

update_inventory_display()
update_order_display()
update_statistics()

root.mainloop()