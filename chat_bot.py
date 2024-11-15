# Import from your database.py file
from database import Customer, Ticket, session
from openai import OpenAI
import json, time, os
from vector_database import vector_store
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key= openai_api_key)


#### Function calls
# Define the assistant function schema
functions = {
    
        "name": "get_ticket_status",
        "description": "Get the status of a support ticket by ticket ID",
        "parameters": {
            "type": "object",
            "properties": {
                "ticket_id": {
                    "type": "integer",
                    "description": "The ID of the support ticket"
                }
            },
            "required": ["ticket_id"]
        }
    }

#### Functions
# Define a function that will query the ticket status
def get_ticket_status(ticket_id):
    ticket = session.query(Ticket).filter_by(ticket_id=ticket_id).first()
    if ticket:

        return f"""ticket_status: {ticket.status}, issue: {ticket.issue_description}"""

    else:
        return "Ticket not found"

# Function to create a new support ticket using the sender's phone number
def create_ticket(phone_number, issue_description):
    print(phone_number)
    print(issue_description)
    # Find the customer by their phone number
    customer = session.query(Customer).filter_by(phone_number=phone_number).first()
    
    if customer:
        # If customer exists, create a new ticket for that customer
        new_ticket = Ticket(
            customer_id=customer.customer_id,
            status="Open",  # Default status is "Open"
            issue_description=issue_description,
        )
        
        # Add the ticket to the session
        session.add(new_ticket)
        
        # Commit the session to write the ticket to the database
        session.commit()
        
        # Return the ticket ID to confirm creation
        return f"New ticket created successfully for {customer.first_name} {customer.last_name}. Ticket ID: {new_ticket.ticket_id}"
    else:
        # If no customer found, return an error message
        return "Customer not found. Unable to create a ticket."

#### Initialize and instruct assistant
assistant = client.beta.assistants.create(
  name="Margaret.com Assistant",
  instructions=f"""
Provide customer support for Margaret.com by assisting with questions or issues related to the website, using available knowledge and database information.

You have access to the following data:

- **Customers Table:**
  - Fields: customer_id, first_name, last_name, email, phone_number

- **Tickets Table:**
  - Fields: ticket_id, status, customer_id, issue_description, created_at

# User Phone number 

User's phone number (`phone_number`) will you provided along with the source. Extract only the phone number and use it as a function call argument if necessary

# User States

The conversation state (`user_state`) will indicate the user's next expectation. The possible states include:

- **`faq`:** Answer Markate-related FAQs.
- **ticket_status`:** Update the user with ticket status upon receiving a ticket ID.
- **`tech_issue`:** Provide guidance or troubleshooting for technical issues described by the user.

# Steps

- Based on the `user_state`, categorize the user's query.
- Access the knowledge base or relevant table data as needed.
- Formulate a polite and empathetic response, ensuring clarity and accuracy.

# Output Format

For knowledge base/ faq queries:
- Provide a direct answer from the knowledge base.
- Do not cite your response 

For ticket-related queries:
- Structure the response as:
  ```
  Your ticket details:
  - Ticket ID: [ticket_id]
  - Status: [status]
  - Issue: [issue_description]

   Feel free to ask if you have more questions.
  ```

For tech-issues:
-Summarize issue
- Create new ticket
- Structure the response as:
 New ticket has been created:
 - Ticket ID: [ticket_id]
 - Status: [status]
 - Issue: [issue_description]
 - Created on: [created_at]
   Our customer service agent will be in touch with you shortly. Feel free to ask if you have more questions.
  ```

# Notes

- Verify database data accuracy before responding.
- Refer customers to additional support if necessary solutions are unclear.
- Maintain customer satisfaction with polite and empathetic communication.
- Redirect unrelated inquiries to a default message.
""",
  tools=[{"type": "file_search"},
         {"type": "function",
          "function": {
        "name": "get_ticket_status",
        "description": "Get the status of a support ticket by ticket ID",
        "parameters": {
            "type": "object",
            "properties": {
                "ticket_id": {
                    "type": "integer",
                    "description": "The ID of the support ticket"
                }
            },
            "required": ["ticket_id"]
        }
    }
  },
    {"type": "function",
          "function": {
        "name": "create_ticket",
        "description": "create a new ticket for the generated ticket ID and summarized issue",
        "parameters": {
            "type": "object",
            "properties": {
                "phone_number": {
                    "type": "integer",
                    "description": "phone number of the sender"
                },
                "issue" : {
                    "type" : "string",
                    "description": "a short 2 or 3 word summary of the issue"
                }
            },
            "required": ["issue"]
        }
    }
  }

          ],
  tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
  model="gpt-4o-mini",
)

# Dictionary to track user states
user_state = {}
curr_state = ""
# Greeting message
def send_greeting():
    return """Hey there! I'm Mark, Margaret.com's customer service bot 🤖. What would you like me to help you with today?
1. Markate related questions (FAQ questions)
2. Track your ticket status
3. Technical issues"""

# Function to handle user responses and track state
def process_message(user_message, sender):
    global curr_state
    if sender not in user_state:
        # New user, send greeting
        user_state[sender] = "greeting"
        return send_greeting()

    # Handle user response based on current state
    elif user_state[sender] == "greeting":
        if user_message == "1":
            user_state[sender] = "faq"
            curr_state = user_state[sender]
            return """
            
            
            You've selected Markate-related questions. Please ask your FAQ question. 
            
            For more details please visit us at https://www.markate.com/"""
        
        elif user_message == "2":
            user_state[sender] = "ticket_status"
            curr_state = user_state[sender]
            return "You've selected to track your ticket status. Please provide your ticket ID."
        elif user_message == "3":
            user_state[sender] = "tech_issue"
            curr_state = user_state[sender]
            return "You've selected technical issues. Please describe the issue you're facing."
        else:
            return f"""Please select a valid option from the list.
            1. Markate related questions (FAQ questions)
            2. Track your ticket status
            3. Technical issues"""
    else:
        return process_message_gpt(curr_state, user_message, sender)


def process_message_gpt(curr_state, user_message, sender):
    new_thread1 = client.beta.threads.create()
    message = client.beta.threads.messages.create(
    thread_id=new_thread1.id,
    role="user",
    content=f"""user_state: {curr_state}, phone_number: {sender}, user_message: {user_message}"""
    )
    run = client.beta.threads.runs.create_and_poll(
    thread_id=new_thread1.id,
    assistant_id=assistant.id,
    )

    # Define the list to store tool outputs

    
    # Loop through each tool in the required action section
    #retry_counter = 0
    #max_retries = 10  # Adjust as needed

    while run.status != "completed":
        #retry_counter += 1
        tool_outputs = []
        if run.required_action and run.required_action.submit_tool_outputs:
            for tool in run.required_action.submit_tool_outputs.tool_calls:
                if tool.function.name == "get_ticket_status":
                    arguments = json.loads(tool.function.arguments)
                    ticket_id = arguments.get("ticket_id")
                    status = get_ticket_status(ticket_id)
                    tool_outputs.append({
                        "tool_call_id": tool.id,
                        "output": status
                    })
        if tool_outputs:
            try:
                run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                    thread_id=new_thread1.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
                print("Tool outputs submitted successfully.")
            except Exception as e:
                print("Failed to submit tool outputs:", e)
        else:
            print("No tool outputs to submit.")
        #time.sleep(2)  # Optional delay between retries


    # Retrieve the final messages from the conversation
    if run.status == 'completed':
        messages = list(client.beta.threads.messages.list(thread_id=new_thread1.id))
        # After completing the run, reset the state and guide the user back to the main options
        curr_state = ""
        user_state[sender] = "greeting"  # Reset to greeting state
        response_message = messages[0].content[0].text.value
        return f"{response_message}\n\nFor further assistance, please choose from: \n1. Markate related questions \n2. Track your ticket status\n3. Technical issues"
    else:
        return f"Run not completed, current status: {run.status}"



