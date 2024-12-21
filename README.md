Google Generative AI Chat Application

Overview

This project implements a web-based chatbot using Google Generative AI (Gemini 1.5 Flash model). The chatbot provides conversational responses to user inputs by leveraging Google's generative AI capabilities. The application is built using Node.js, Express, and serves a static frontend for interaction.

Features

Integration with Google Generative AI API.

Supports conversational history for context-based replies.

Custom styling for a dark-themed user interface.

Lightweight and extensible backend with Express.js.

Dynamically served CSS and static HTML pages.

Prerequisites

Node.js and npm installed on your machine.

A valid Google Generative AI API key.

Environment file (.env) configured with API_KEY and optionally PORT.

Installation

Clone the repository:

git clone <repository-url>
cd <repository-directory>

Install dependencies:

npm install

Create a .env file in the root directory and add your API key:

API_KEY=your-google-api-key
PORT=2001 # Optional, defaults to 2001 if not specified

Start the server:

npm start

Open your browser and navigate to:

http://localhost:2001

Project Structure

server.js: Main server file containing API logic and routes.

public/: Directory for static HTML files such as index.html and login.html.

Endpoints

GET /

Serves the index.html file as the main interface.

GET /login

Serves the login.html file for user authentication (if applicable).

POST /api

Processes user input, generates AI responses, and returns the results.

Request Body: { "text": "Your input text here" }

Response:

{
    "generatedText": "AI-generated response text"
}

GET /style.css

Serves the CSS for the application, dynamically injected by the server.

Customization

CSS

The CSS styles are injected dynamically through the /style.css route. Modify the styles directly in the server.js file under the /style.css endpoint.

AI Model Configuration

The generationConfig object in the server.js file allows you to customize the behavior of the AI model. Available options:

stopSequences: List of strings to stop text generation.

maxOutputTokens: Maximum number of tokens in the response.

temperature: Controls randomness in output (higher values for more random outputs).

topP and topK: Controls nucleus and top-k sampling.

Error Handling

If an error occurs during content generation, the server will log the error and respond with a 500 status code and the following message:

{
    "error": "Failed to generate content"
}

License

This project is licensed under the MIT License.

Contributing

Feel free to submit issues and pull requests to improve the project.

Acknowledgments

Google Generative AI

Express.js Documentation

Node.js Documentation
