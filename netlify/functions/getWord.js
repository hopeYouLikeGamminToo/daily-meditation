const axios = require('axios');

const headers = {
    "Access-Control-Allow-Origin": "*", // or "*" to allow any origin
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "POST, GET, OPTIONS"
};


exports.handler = async function (event, context) {
    if (event.httpMethod === "OPTIONS") {
        return {
          statusCode: 204,
          headers: {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
          },
          body: "",
        };
      }

    console.log(event);
    const quote = JSON.parse(event.body).quote;

    try {
        const MAX_TRIES = 3;
        let tries = 0;

        const initialMessages = [
            {
                "role": "system",
                "content": "You are a random word generator."
            },
            {
                "role": "user",
                "content": `You have two inputs a random quote and the author. Using these inputs as inspiration, you are to generate and output one word. The word should be random but related to the quote. Make it reasonably hard to guess.\nquote:${quote['content']}, author: ${quote['author']}`
            }
        ];

        let messages = [...initialMessages];

        while (tries < MAX_TRIES) {
            const payload = {
                "model": "gpt-3.5-turbo",
                "messages": messages
            };

            const response = await axios.post('https://api.openai.com/v1/chat/completions', payload, {
                headers: {
                    'Authorization': `Bearer ${process.env.VUE_APP_OPENAI_API_KEY}`,
                    'Content-Type': 'application/json',
                }
            });

            const generatedWord = response.data.choices[0].message.content;

            // Check if the response is a single word
            if (generatedWord.split(' ').length === 1 && generatedWord.length <= 11) {
                // return generatedWord;
                return {
                    statusCode: 200,
                    headers: headers,
                    body: JSON.stringify({ generatedWord }),
                };
            }

            // Add the assistant's response to the messages
            messages.push({
                "role": "assistant",
                "content": generatedWord
            });

            // Add a user message to request a single word again
            messages.push({
                "role": "user",
                "content": `Please respond with only the generated word. quote:${quote['content']}, author: ${quote['author']}`
            });

            tries++;
        }
        // return "Error: Failed to generate a word after max tries. Please try again later.";
        return {
            statusCode: 500,
            headers: headers,
            body: JSON.stringify({ error: error.message }),
        };
    } catch (error) {
        console.error('An error occurred:', error);
        // return "Error: Failed to generate a word after max tries. Please try again later.";
        return {
            statusCode: 500,
            headers: headers,
            body: JSON.stringify({ error: error.message }),
        };
    }
}