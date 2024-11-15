from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime


# Set up the SQLite engine
engine = create_engine('sqlite:///support_system.db')
Base = declarative_base()

# Define the Customers table
class Customer(Base):
    __tablename__ = 'customers'
    customer_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone_number = Column(String)

# Define the Tickets table
class Ticket(Base):
    __tablename__ = 'tickets'
    ticket_id = Column(Integer, primary_key=True)
    status = Column(String)
    customer_id = Column(Integer)  # Foreign key to customers table
    issue_description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# Create both tables
Base.metadata.create_all(engine)


# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()
