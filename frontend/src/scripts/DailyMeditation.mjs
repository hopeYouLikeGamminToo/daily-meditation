import axios from 'axios';

export function getDate() {
    return new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }); // "Monday, October 23, 2023" 
}

export async function getContent() {
    const today = getDate();

    let res = await axios.get(`/get_content?date=${today}`);

    // get word history
    let wordHistory = null;
    try {
        console.log("/get_word_history")
        const response = await axios.get('/get_word_history', {});
        if (response.data) {
            wordHistory = response.data;
        }
    } catch (err) {
        console.error('Error fetching user data:', err);
    }

    if (res.data) {
        if (res.data.quote === null || res.data.word === null) {
            // Fetch new quote and word
            const MAX_ATTEMPTS = 3; // Adjust this value as needed
            let attempts = 0;
    
            while (attempts < MAX_ATTEMPTS) {
                try {
                    console.log("getting quote")
                    const quoteData = await fetchNewQuote();
                    console.log(quoteData);
                    if (!quoteData.content || !quoteData.author) {
                        console.warn('Quote content or author is undefined. Fetching a new quote.');
                        attempts++;
                        continue; // Skip the rest of the loop body and fetch a new quote
                    } else {
                        console.log("quote: ", quoteData);
                    }

                    console.log("getting word")
                    const wordData = await fetchNewWord(quoteData, wordHistory);

                    // Check if a valid word was returned
                    if (wordData && wordData.split(' ').length === 1 && wordData.length <= 11) {
                        // Save them to your database
                        console.log("word: ", wordData);
                        console.log("saving content")

                        const params = { 
                            date: today, 
                            word: wordData, 
                            quote: quoteData.content, 
                            author: quoteData.author 
                        };
                        let ret = await axios.post('http://localhost:8000/save_content', null, { params });
                        
                        return { quote: quoteData, word: wordData };
                    }
                } catch (error) {
                    console.error('An error occurred while fetching a word:', error);
                }
                attempts++;
            }

            if (attempts === MAX_ATTEMPTS) {
                console.log("max tries!");
                return {
                    quote: { content: res.data.quote, author: res.data.author },
                    word: "Error: Please try again."
                };
            }
        }

        return {
            quote: { content: res.data.quote, author: res.data.author },
            word: res.data.word
        };
    }

    // If res.data is null, you can decide what to do here.
    return {
        quote: { content: "Error: Please try again.", author: null },
        word: "Error: Please try again."
    };
}

async function fetchNewQuote() {
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

    return quote;
}

async function fetchNewWord(quote, wordHistory) {
    try {
        // development - http://localhost:8888/.netlify/functions/getWord 
        // production - /.netlify/functions/getWord
        const response = await axios.post('http://localhost:8888/.netlify/functions/getWord', JSON.stringify({ quote: quote, wordHistory: wordHistory}), {
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
