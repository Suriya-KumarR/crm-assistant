

# Example: Insert sample data into the tables
customer = Customer(first_name="John", last_name="Doe", email="john.doe@example.com", phone_number="555-1234")
session.add(customer)
session.commit()

ticket = Ticket(status="Open", customer_id=customer.customer_id, issue_description="Unable to access account")
session.add(ticket)
session.commit()

# Verify the insertion
customers = session.query(Customer).all()
tickets = session.query(Ticket).all()

print(customers)
print(tickets)