# Mark - CRM Assistant

Mark is an intelligent CRM assistant designed to help business professionals manage customer data, work orders, and other CRM tasks more efficiently. Integrated with **OpenAI** for language understanding, **Pinecone** for knowledge retrieval, and **HubSpot** API for CRM operations, Mark enables smooth interaction with CRM data, answering FAQs or performing CRUD operations seamlessly.
![WhatsApp Image 2024-11-14 at 21 36 35](https://github.com/user-attachments/assets/34645fa9-ea63-4559-ab15-8cb488439346)

# Demo
Watch a short pitch to understand the working of Mark!

[Watch the Demo Video](https://drive.google.com/file/d/1aDjtAoyz5sTl9jFiv8v5v2gAXGpS9uDR/view?usp=drive_link)

## Features

- **Knowledge Retrieval**: Using a Retrieval-Augmented Generation (RAG) approach, Mark answers frequently asked questions with information stored in a vector database.
- **HubSpot API Integration**: Supports CRUD operations for CRM data stored in HubSpot.
- **AI-Driven Query Resolution**: Powered by OpenAI’s GPT-4, Mark interprets natural language queries, making it easy to interact with complex CRM data.
- **Twilio Integration**: Host on Twilio to enable direct interaction over messaging apps like WhatsApp or SMS.

## Technologies Used

- **FastAPI**: For API server and backend management.
- **LangChain**: To build and manage the RAG pipeline.
- **Pinecone**: For vector storage and retrieval of FAQ answers.
- **OpenAI**: GPT-4 model for natural language understanding.
- **Twilio**: For messaging interface.
- **HubSpot API**: For CRM data operations.


## Setup and Installation

### Prerequisites

- **Python 3.8+**
- **API Keys** for OpenAI, Pinecone, Twilio, and HubSpot.
- **Environment Variables** in a `.env` file for sensitive credentials.

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/mark-crm-assistant.git
   cd mark-crm-assistant
   ```

2. **Create and Activate a Virtual Environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:

   Create a `.env` file in the root directory and add your keys:

   ```plaintext
   OPENAI_API_KEY=your_openai_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   HUBSPOT_API_KEY=your_hubspot_api_key
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   ```

5. **Run the Application Locally**:

   ```bash
   uvicorn app.main:app --reload
   ```

## Project Structure

- `app/`: Main application files.
  - `main.py`: FastAPI server and endpoint configurations.
  - `utils/`: Utility functions and helper modules.
    - `pinecone_utils.py`: Pinecone initialization and helper functions.
    - `hubspot_utils.py`: HubSpot API functions.
- `requirements.txt`: Python package dependencies.
- `.env`: Environment configuration file (add API keys here).
- `README.md`: Project documentation.

## Usage

1. **Twilio Integration**:

   Mark can be connected with Twilio for WhatsApp/SMS messaging. Configure Twilio’s webhook to point to your deployed FastAPI server.

2. **Handling User Queries**:

   - **FAQ Queries**: Mark uses Pinecone vector storage to retrieve answers to frequently asked questions.
   - **HubSpot CRUD Operations**: For operations like adding a customer or creating a work order, Mark communicates directly with the HubSpot API.

3. **RAG Pipeline**:

   Mark utilizes a RAG pipeline to provide answers for FAQs using context retrieval and the GPT-4 model.

### Example API Endpoints

- **FAQ Handling**:

  ```json
  POST /generate_api_call
  {
    "query": "How do I create a new work order?"
  }
  ```

  Returns: Response with information on creating a work order from vector storage.

- **HubSpot CRUD Operations**:

  ```json
  POST /hubspot_api_function
  {
    "endpoint": "/crm/v3/objects/contacts",
    "method": "POST",
    "data": {
      "firstname": "John",
      "lastname": "Doe",
      "email": "john.doe@example.com"
    }
  }
  ```

  Returns: Confirmation of HubSpot CRM operation.

## Deployment

1. **Deploy on Twilio**:

   Use Twilio Functions to configure Mark as a chatbot assistant for customer communication.

2. **Run on a Cloud Server**:

   Deploy on cloud services like **AWS**, **Heroku**, or **Azure** for robust and scalable performance.

3. **Scaling Recommendations**:

   Use **Docker** for containerization and deploy on a managed Kubernetes cluster for larger organizations.

## Contributing

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch-name`.
3. Commit your changes: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature-branch-name`.
5. Submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or issues, please contact:

- **Email**: support@example.com
- **GitHub**: [Your GitHub Username](https://github.com/yourusername)

---

Feel free to customize the README to fit your project requirements or update contact information. Let me know if you need any more details!















