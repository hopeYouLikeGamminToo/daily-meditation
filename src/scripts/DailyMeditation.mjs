import axios from 'axios';

export function getDate() {
    return new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }); // "Monday, October 23, 2023" 
}

export async function getQuote() {
    // let content = "I hope we shall crush in its birth the aristocracy of our monied corporations which dare already to challenge our government to a trial by strength, and bid defiance to the laws of our country.";
    // let author = "Thomas Jefferson";
    // return {'content': content, 'author': author};
    // return {'content': false, 'author': false};

    const authors = [
        // Philosophers
        "Plato",
        "Aristotle",
        "Immanuel Kant",
        "Friedrich Nietzsche",
        "Søren Kierkegaard",
        "Jean-Jacques Rousseau",
        "Thomas Hobbes",
        "John Locke",
        "Voltaire",
        "Confucius",
        "Laozi",

        // Writers and Scholars
        "William Shakespeare",
        "Ralph Waldo Emerson",
        "Henry David Thoreau",
        "Mark Twain",
        "George Orwell",
        "Leo Tolstoy",
        "Fyodor Dostoevsky",
        "Franz Kafka",
        "James Baldwin",
        "Mary Wollstonecraft",

        // Historical Figures
        "Winston Churchill",
        "Mahatma Gandhi",
        "Martin Luther King Jr.",
        "Nelson Mandela",
        "Eleanor Roosevelt",
        "Abraham Lincoln",
        "Benjamin Franklin",
        "Thomas Jefferson"
    ];
    const randomAuthor = authors[Math.floor(Math.random() * authors.length)];

    const url = `https://api.quotable.io/random?author=${encodeURIComponent(randomAuthor)}`;

    const response = await fetch(url);
    const quote = await response.json();

    return { content: quote.content, author: quote.author };
}

// randomQuote().then(({ content, author }) => {
// console.log(content);
// console.log(`\t${author}`);
// });

export async function getWord(quote) {
    try {
        const response = await axios.post('/.netlify/functions/getWord', JSON.stringify({ quote: quote }), { // http://localhost:8888/.netlify/functions/getWord
            headers: {
                'Content-Type': 'application/json',
            },
        });
        console.log(response);
        return response.data.generatedWord;
    } catch (error) {
        console.error('An error occurred:', error);
        return "Error: Failed to generate a word after max tries. Please try again later.";
    }
}

/*
// for local development - no proxy to neltify functions
export async function getWord(quote) {
    // return "Revolution";
    // return "Error: Failed to generate a word after max tries. Please try again later.";

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
                return generatedWord;
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
        return "Error: Failed to generate a word after max tries. Please try again later.";

    } catch (error) {
        console.error('An error occurred:', error);
        return "Error: Failed to generate a word after max tries. Please try again later.";
    }
}
*/
