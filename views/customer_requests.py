CUSTOMERS = []

def get_all_customers():
    return CUSTOMERS

def create_customer(customer):
    if len(CUSTOMERS) != 0:
        max_id = CUSTOMERS[-1]["id"]
        new_id = max_id + 1
        customer["id"] = new_id
        CUSTOMERS.append(customer)
        return customer
    else:
        customer["id"]= 0
        CUSTOMERS.append(customer)
        return customer
    
def update_customer(id, new_customer):
    for index, customer in enumerate(CUSTOMERS):
        if customer["id"] == id:
            CUSTOMERS[index] = new_customer
            break
    
def delete_customer(id):
    customer_index = -1
    for index, customer in enumerate(CUSTOMERS):
        if customer["id"] == id:
            customer_index = index
    if customer_index >= 0:
        CUSTOMERS.pop(customer_index)
