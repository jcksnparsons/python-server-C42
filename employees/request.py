EMPLOYEES = [
    {
        "id": 1,
        "name": "Nandor The Relentless",
        "locationId": 1
    },
    {
        "id": 2,
        "name": "Nadja Cravensworth",
        "locationId": 2
    },
    {
        "id": 3,
        "name": "Lazlo Cravensworth",
        "locationId": 1
    },
    {
        "id": 4,
        "name": "Colin Robinson",
        "locationId": 2
    },
    {
        "name": "Guillermo",
        "locationId": 1,
        "animalId": 3,
        "id": 5
    }
]

def get_all_employees():
    return EMPLOYEES

# Function with a single parameter


def get_single_employee(id):
    # Variable to hold the found employee, if it exists
    requested_employee = None

    # Iterate the ANIMALS list above. Very similar to the
    # for..of loops you used in JavaScript.
    for employee in EMPLOYEES:
        # Dictionaries in Python use [] notation to find a key
        # instead of the dot notation that JavaScript used.
        if employee["id"] == id:
            requested_employee = employee

    return requested_employee