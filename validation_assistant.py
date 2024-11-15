from openai import OpenAI
import os
import asyncio
from pymongo import MongoClient  # MongoDB integration
#from dnd_kb import DnD_test_store
from dotenv import load_dotenv

# Load API keys
openai_api_key = os.getenv("OPENAI_API_KEY") 
mongo_uri = os.getenv("MONGO_URI")  # Add MongoDB connection URI

client = OpenAI(api_key=openai_api_key)

# Connect to MongoDB
mongo_client = MongoClient(mongo_uri)
db = mongo_client['dnd_database']  # Use your actual database name
characters_collection = db['characters']  # Collection for character data

# Function to query MongoDB for character data
def get_character_info(character_name):
    # Query the character based on character_name
    character = characters_collection.find_one({"character_name": character_name})
    return character


# Validation Assistant setup with function tool
validation_assistant = client.beta.assistants.create(
    name="Validation Assistant",
    instructions=f"""
 Validate player actions based on their character's attributes, abilities, and the game's context.

# Steps

1. **Retrieve Character Information**: Access the MongoDB database to obtain the player's character information using their character name.
2. **Action Validation**:
   - Compare the player's attempted action with their character's attributes and abilities.
   - Determine if the action aligns with what the character can perform within the game's context.
3. **Determine Validity**:
   - Conclude whether the action is valid (True) or invalid (False) based on the validation process.
4. **Provide Reasoning**: Clarify the reasons behind the validity decision, ensuring it's comprehensive and related to the character’s attributes.
5. **Suggest Alternatives**: If the action is deemed invalid, offer a feasible and contextually suitable alternative action.

# Output Format

The output should be in JSON format and include the following fields:
- `action`: The action the player attempted.
- `validity`: A boolean value indicating the validity of the action.
- `reason`: A descriptive string explaining why the action is valid or invalid.
- `suggestion`: If the action is invalid, provide a recommended alternative action.

# Example

**Input:**
- Player action: "Fly across the sky"
- Character: "Pureblood"

**Output:(JSON Format)**


  "action": "Fly across the sky",
  "validity": false,
  "reason": "Purebloods cannot fly.",
  "suggestion": "Consider using Noble Strike instead."


# Notes

- Ensure your validation process relies on character attributes retrieved from the MongoDB database.
- Suggestions should be contextually appropriate and provide the player with viable alternative actions.
    """,
    tools=[
        {"type": "function",
         "function": {
            "name": "get_character_info",
            "description": "Get the information of a character by their character name",
            "parameters": {
                "type": "object",
                "properties": {
                    "character_name": {
                        "type": "string",
                        "description": "The name of the character to retrieve info for"
                    }
                },
                "required": ["character_name"]
            }
        }}
    ],
    model="gpt-4o",
)


# Function to handle assistant logic and generate a validation response
async def get_validation_response(character_name, action):
    # Create a new thread for the conversation
    new_thread = client.beta.threads.create()

    # Create a message in the new thread with the content from the player
    client.beta.threads.messages.create(
        thread_id=new_thread.id,
        role="user",
        content=f"Character Name: {character_name}, Action: {action}"
    )

    # Run the assistant using the thread and retrieve the response
    run = client.beta.threads.runs.create_and_poll(
        thread_id=new_thread.id,
        assistant_id=validation_assistant.id
    )

    if run.status == 'completed':
        # Retrieve messages from the thread
        messages = client.beta.threads.messages.list(thread_id=new_thread.id)
        
        # Extract the content of the assistant's response
        assistant_message = messages.data[0].content[0].text

        # Log the assistant's message for debugging
        print(f"Assistant's response: {repr(assistant_message)}")  # Use repr to show raw string for debugging

    else:
        print(f"Error: Run status was not completed. Status: {run.status}")
        return None, None

# Example usage of the validation assistant
async def main():
    character_name = "Pureblood"
    action = "Fly across the sky"


# Run the asynchronous main function
if __name__ == "__main__":
    asyncio.run(main())
