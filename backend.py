from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from chat_bot import process_message

app = Flask(__name__)

# Webhook to receive incoming messages from Twilio
@app.route("/webhook", methods=["POST"])
def receive_message():
    incoming_msg = request.form.get('Body')  # Get the message content from Twilio
    sender = request.form.get('From')  # Get the sender's phone number (optional)
    print(sender)
    print(incoming_msg)

    # Process the incoming message using the chatbot
    response_msg = process_message(incoming_msg, sender)
    
    # Create a Twilio response object
    resp = MessagingResponse()
    resp.message(response_msg)
    print(response_msg)
    return str(resp)

if __name__ == "__main__":
    app.run(port=5000)
