import json
import sqlite3
from models import Customer

# CUSTOMERS = [
#     {
#         "id": 1,
#         "name": "Hannah Hall",
#         "address": "7002 Chestnut Ct"
#     },
#     {
#         "id": 2,
#         "name": "Jack Parsons",
#         "address": "Nunya"
#     },
#     {
#         "id": 3,
#         "name": "Holly Parsons",
#         "address": "Also Nunya"
#     },
#     {
#         "email": "j@j.j",
#         "password": "j",
#         "name": "Jack Parsons",
#         "id": 4
#     }
# ]


def get_all_customers():
    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.name,
            c.address,
            c.email
        FROM customer c
        """)

        customers = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            customer = Customer(row['id'], row['name'], row['address'], row['email'])

            customers.append(customer.__dict__)

        return json.dumps(customers)

# Function with a single parameter


def get_single_customer(id):
    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            c.id,
            c.name,
            c.address,
            c.email,
            c.password
        FROM customer c
        WHERE c.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        customer = Customer(data['id'], data['name'],
                            data['address'], data['email'], data['password'])

        return json.dumps(customer.__dict__)


def get_customer_by_email(email):

    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.name,
            c.address
        FROM Customer c
        WHERE c.email = ?
        """, (email, ))

        data = db_cursor.fetchone()

        # Create an customer instance from the current row
        customer = Customer(data['name'], data['id'], data['address'])

        # Return the JSON serialized Customer object
        return json.dumps(customer.__dict__)


def update_customer(id, new_customer):
    # Iterate the CUSTOMERS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, customer in enumerate(CUSTOMERS):
        if customer["id"] == id:
            # Found the customer. Update the value.
            CUSTOMERS[index] = new_customer
            break


def delete_customer(id):
    # Initial -1 value for customer index, in case one isn't found
    customer_index = -1

    # Iterate the customerS list, but use enumerate() so that you
    # can access the index value of each item
    for index, customer in enumerate(CUSTOMERS):
        if customer["id"] == id:
            # Found the customer. Store the current index.
            customer_index = index

    # If the customer was found, use pop(int) to remove it from list
    if customer_index >= 0:
        CUSTOMERS.pop(customer_index)
