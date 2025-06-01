from tkinter import *

root = Tk()

products = ["Alovera", "Asparagus", "Cordyceps"]
entries = {}

# Create input fields
for i, product in enumerate(products):
    Label(root, text=product).grid(row=i, column=0)
    entry = Entry(root)
    entry.grid(row=i, column=1)
    entries[product] = entry  # store entry widget in a dictionary

# Function to collect data
def collect_quantities():
    quantities = {}
    for product, entry in entries.items():
        value = entry.get()
        if value:  # skip empty inputs
            quantities[product] = int(value)
    print(quantities)

Button(root, text="Submit", command=collect_quantities).grid(row=len(products), column=1)




