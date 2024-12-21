import { GoogleGenerativeAI } from '@google/generative-ai';
import dotenv from 'dotenv';
import express from 'express';
import cors from 'cors';
import bodyParser from 'body-parser';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

dotenv.config();

const app = express();
const port = process.env.PORT || 2001;

app.use(cors({
    origin: "*",
    credentials: true
}));
app.use(bodyParser.json());

const genAI = new GoogleGenerativeAI(process.env.API_KEY);
const generationConfig = {
    stopSequences: ["\n\n"], 
    maxOutputTokens: 200,
    temperature: 1,
    topP: 0.9,
    topK: 40,
};

const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" }, generationConfig);

let history = [];

function removeMarkdown(text) {
    return text.replace(/[_*~`<>#\[\]]+/g, '');
}

function formatText(text) {
    return text.replace(/(\.\s*\d+)/g, '.\n$1');
}

async function run(prompt = "") {
    try {
        const historyContext = history.join('\n') + '\n' + prompt;
        const result = await model.generateContent(historyContext);
        const text = result.response.text();
        const plainText = removeMarkdown(text);
        const formattedText = formatText(plainText);
        history.push(prompt);
        history.push(formattedText);

        if (history.length > 20) {
            history = history.slice(-20);
        }

        return formattedText;
    } catch (error) {
        console.error('Error generating content:', error);
        throw error;
    }
}

const __filename = fileURLToPath(import.meta.url);
const _dirname = dirname(_filename);

app.use(express.static(path.join(__dirname, 'public')));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/login', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'login.html'));
});

app.post("/api", async (req, res) => {
    const { text } = req.body;
    try {
        const data = await run(text);
        res.json({ generatedText: data });
    } catch (error) {
        console.error('Error processing request:', error);
        res.status(500).json({ error: 'Failed to generate content' });
    }
});

// Inject the CSS directly into the HTML file
app.get('/style.css', (req, res) => {
    const css = `
    /* styles.css */
    body {
        background-color: #1e1e1e;
        color: #e0e0e0;
        font-family: 'Arial', sans-serif;
        margin: 0;
        padding: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        flex-direction: column;
    }

    .container {
        background-color: #333;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
        max-width: 400px;
        width: 100%;
        display: flex;
        flex-direction: column;
    }

    h1 {
        text-align: center;
        margin-bottom: 20px;
        color: #fff;
    }

    form {
        display: flex;
        flex-direction: column;
        margin-top: 10px;
    }

    label {
        margin-bottom: 10px;
        color: #bbb;
    }

    input[type="text"], input[type="password"], input[type="email"] {
        padding: 10px;
        margin-bottom: 20px;
        border: none;
        border-radius: 5px;
        background-color: #555;
        color: #fff;
        font-weight: bold;  /* Make text bold */
        width: 100%;  /* Make text box fit the screen */
    }

    button {
        padding: 10px;
        border: none;
        border-radius: 5px;
        background-color: #007bff;
        color: #fff;
        cursor: pointer;
    }

    button:hover {
        background-color: #0056b3;
    }

    .message-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
        width: 100%;  /* Ensure container is full width */
        max-height: calc(100vh - 200px); /* Adjust the height dynamically */
        overflow-y: auto;
        margin-bottom: 20px;
    }

    .message {
        padding: 10px;
        border-radius: 10px;
    }

    .message.user {
        background-color: #007bff;
        align-self: flex-end;
        color: #fff;
        font-weight: bolder; /* Make user message text bolder */
    }

    .message.bot {
        background-color: #444;
        align-self: flex-start;
        color: #fff;
        font-weight: normal; /* Keep bot response text normal */
    }

    input[type="text"] {
        padding: 10px;
        margin-top: 10px;
        width: 100%;  /* Ensure it fits the screen */
        border: none;
        border-radius: 5px;
        background-color: #555;
        color: #fff;
        font-weight: bold;  /* Make text bold */
    }

    #chatForm {
        display: flex;
        justify-content: space-between;
        width: 100%;
    }

    #generatedText {
        margin-top: 10px;
        padding: 10px;
        border-radius: 5px;
        background-color: #444;
    }

    #textForm button, #chatForm button {
        padding: 10px;
        border: none;
        border-radius: 5px;
        background-color: #007bff;
        color: #fff;
        cursor: pointer;
    }

    #textForm button:hover, #chatForm button:hover {
        background-color: #0056b3;
    }
    `;
    res.type('text/css').send(css);
});

app.listen(port, () => {
    console.log(Server running on port ${port});
});