import csv
import random
from faker import Faker
from faker_commerce import EcommerceProvider # Correctly import the provider
from datetime import datetime, timedelta

# --- Configuration ---
NUM_CUSTOMERS = 1000
NUM_PRODUCTS = 500
NUM_ORDERS = 5000
MAX_ITEMS_PER_ORDER = 5
DB_START_DATE = datetime(2022, 1, 1)
DB_END_DATE = datetime(2023, 12, 31)

# Initialize Faker and add the ecommerce provider
fake = Faker()
fake.add_provider(EcommerceProvider)

# --- Data Storage ---
categories_data = []
products_data = []
customers_data = []
orders_data = []
order_items_data = []
payments_data = []

# --- Helper Functions ---
def create_csv(filename, headers, data):
    """Creates a CSV file from a list of dictionaries."""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
        print(f"Successfully created {filename}")
    except IOError as e:
        print(f"Error writing to {filename}: {e}")

# --- 1. Generate Categories ---
print("Generating Categories...")
category_list = ['Electronics', 'Books', 'Home & Kitchen', 'Apparel', 'Sports & Outdoors', 'Toys & Games', 'Health & Beauty', 'Automotive']
for i, cat_name in enumerate(category_list, 1):
    categories_data.append({
        'category_id': i,
        'category_name': cat_name
    })

# --- 2. Generate Customers ---
print("Generating Customers...")
for i in range(1, NUM_CUSTOMERS + 1):
    customers_data.append({
        'customer_id': i,
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.unique.email(),
        'registration_date': fake.date_time_between(start_date='-3y', end_date='now')
    })

# --- 3. Generate Products ---
print("Generating Products...")
for i in range(1, NUM_PRODUCTS + 1):
    products_data.append({
        'product_id': i,
        'product_name': fake.ecommerce_name(), # This will now work correctly
        'description': fake.text(max_nb_chars=200),
        'price': round(random.uniform(5.0, 500.0), 2),
        'category_id': random.randint(1, len(category_list)),
        'stock_quantity': random.randint(0, 200),
        'created_at': fake.date_time_between(start_date='-3y', end_date='-1y')
    })

# --- 4. Generate Orders and Order Items ---
print("Generating Orders and Order Items...")
order_item_id_counter = 1
for i in range(1, NUM_ORDERS + 1):
    customer_id = random.randint(1, NUM_CUSTOMERS)
    order_date = fake.date_time_between(start_date=DB_START_DATE, end_date=DB_END_DATE)
    order_status = random.choice(['Delivered', 'Shipped', 'Pending', 'Cancelled'])
    
    orders_data.append({
        'order_id': i,
        'customer_id': customer_id,
        'order_date': order_date,
        'status': order_status
    })

    # For each order, generate order items
    num_items_in_order = random.randint(1, MAX_ITEMS_PER_ORDER)
    order_total_amount = 0
    
    # Ensure products in an order are unique
    products_in_order = random.sample(products_data, num_items_in_order)

    for product in products_in_order:
        if order_status != 'Cancelled':
            quantity = random.randint(1, 3)
            price_per_unit = product['price']
            order_total_amount += quantity * price_per_unit

            order_items_data.append({
                'order_item_id': order_item_id_counter,
                'order_id': i,
                'product_id': product['product_id'],
                'quantity': quantity,
                'price_per_unit': price_per_unit
            })
            order_item_id_counter += 1

    # --- 5. Generate Payments (related to orders) ---
    if order_status != 'Cancelled':
        payment_status = 'Completed' if random.random() > 0.1 else 'Failed' # 10% chance of failure
        if payment_status == 'Completed':
            payments_data.append({
                'payment_id': i, # Simple 1-to-1 mapping with order_id for this mock data
                'order_id': i,
                'payment_date': order_date + timedelta(minutes=random.randint(5, 60)),
                'amount': round(order_total_amount, 2),
                'payment_method': random.choice(['Credit Card', 'PayPal', 'Debit Card', 'Bank Transfer']),
                'status': payment_status
            })

print("Data generation complete. Now writing to CSV files.")

# --- 6. Write all data to CSV files ---
create_csv('categories.csv', ['category_id', 'category_name'], categories_data)
create_csv('customers.csv', ['customer_id', 'first_name', 'last_name', 'email', 'registration_date'], customers_data)
create_csv('products.csv', ['product_id', 'product_name', 'description', 'price', 'category_id', 'stock_quantity', 'created_at'], products_data)
create_csv('orders.csv', ['order_id', 'customer_id', 'order_date', 'status'], orders_data)
create_csv('order_items.csv', ['order_item_id', 'order_id', 'product_id', 'quantity', 'price_per_unit'], order_items_data)
create_csv('payments.csv', ['payment_id', 'order_id', 'payment_date', 'amount', 'payment_method', 'status'], payments_data)

print("\nAll CSV files have been generated in the same directory as the script.")
