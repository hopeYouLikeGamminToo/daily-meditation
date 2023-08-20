<template>
    <div class="daily-content-container">
        <div class="daily-content">
            <div class="quote" v-if="index == 0">
                <h2 class="title">{{ currentDate }}</h2>
                <button @click="toggleMute" class="audio-button"><i class="fa-solid fa-music"></i></button>
                <button @click="nextCard" class="next-button"><i class="fa-solid fa-arrow-right"></i></button>
                <button @click="lastCard" class="last-button"><i class="fa-solid fa-arrow-left"></i></button>
                <p>{{ quote['content'] }}</p>
                <p class="author">{{ quote['author'] }}</p>
            </div>
            <div class="game" v-if="index == 1">
                <h2 class="title">Wisdom Tree</h2>
                <button @click="toggleMute" class="audio-button"><i class="fa-solid fa-music"></i></button>
                <button @click="nextCard" class="next-button"><i class="fa-solid fa-arrow-right"></i></button>
                <button @click="lastCard" class="last-button"><i class="fa-solid fa-arrow-left"></i></button>
                <WisdomTree :quote="quote" :word="word"></WisdomTree>
            </div>
            <div class="credits" v-if="index == 2">
                <h2 class="title">Credits</h2>
                <button @click="toggleMute" class="audio-button"><i class="fa-solid fa-music"></i></button>
                <button @click="nextCard" class="next-button"><i class="fa-solid fa-arrow-right"></i></button>
                <button @click="lastCard" class="last-button"><i class="fa-solid fa-arrow-left"></i></button>

                <p>Video: <a :href="sharedData">{{ sharedData }}</a></p>
                <p>Quote: <a :href="quoteCredits">{{ quoteCredits }}</a></p>
                <p>NLP AI: <a :href="aiCredits">{{ aiCredits }}</a></p>
                <p>Developer: <a :href="developerCredits">{{ developerCredits }}</a></p>
                <div class="coffee-link">
                    <a href="https://www.buymeacoffee.com/dailymeditations" target="_blank">
                        <img class="bmc" src="../assets/bmc/bmc-no-bg.png" />
                    </a>
                </div>
            </div>
        </div>
    </div>
</template>
  
  
<script>
import { getDate, getQuote, getWord } from '../scripts/DailyMeditation'
import WisdomTree from './WisdomTree.vue';


export default {
    props: ['toggleMute', 'sharedData'],
    components: {
        WisdomTree,
    },
    watch: {
        sharedData(newValue) {
            console.log('Shared data has been updated:', newValue);
        }
    },
    data() {
        return {
            index: 0,
            aiCredits: "https://platform.openai.com/docs/api-reference/chat",
            quoteCredits: "https://github.com/lukePeavey/quotable",
            developerCredits: "https://howl0893.github.io/",
            currentDate: getDate(),
            quote: "Finding the quote of the day...",
        };
    },
    async mounted() {
        const MAX_ATTEMPTS = 3; // Adjust this value as needed
        let attempts = 0;

        while (attempts < MAX_ATTEMPTS) {
            try {
                this.quote = await getQuote();

                // Check if the quote content or author is undefined
                if (!this.quote.content || !this.quote.author) {
                    console.warn('Quote content or author is undefined. Fetching a new quote.');
                    attempts++;
                    continue; // Skip the rest of the loop body and fetch a new quote
                }

                this.word = await getWord(this.quote);
                console.log(this.quote.content);
                console.log(`\t${this.quote.author}`);
                console.log(this.word);

                // Check if a valid word was returned
                if (this.word && this.word.split(' ').length === 1 && this.word.length <= 11 && this.word !== "Error fetching content. Please try again later.") {
                    break; // Valid word found, exit loop
                }
            } catch (error) {
                console.error('An error occurred while fetching a word:', error);
            }
            attempts++;
        }

        // Handle the case where no valid word was found after max attempts
        if (attempts === MAX_ATTEMPTS) {
            this.word = "Error: Please try again later.";
        }
    },
    methods: {
        nextCard() {
            this.index += 1;
            if (this.index > 2) {
                this.index = 0;
            }
        },
        lastCard() {
            this.index -= 1;
            if (this.index < 0) {
                this.index = 2;
            }
        }

    }
};
</script>
  
<style>
.daily-content-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;}

.daily-content {
    /* background-image: url('../assets/scroll.png');
    background-size: cover;
    background-repeat: no-repeat; 
    background-position: center; To center the image */


    color: #5a3a22;
    background: #f4e4d7;
    width: 30vw;
    height: auto;
    padding: 20px;
    border: 1px solid #b6a08e;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    position: absolute;
}

.quote {
    width: auto;
    height: auto;
}

.game {
    width: 50vw;
    height: auto;
}

.credits {
    width: auto;
    height: 25vh;
}

.next-button {
    background: none;
    border: none;
    color: #5a3a22;
    cursor: pointer;
    font-size: 14px;
    position: absolute;
    bottom: 10px;
    right: 10px;
}

.last-button {
    background: none;
    border: none;
    color: #5a3a22;
    cursor: pointer;
    font-size: 14px;
    position: absolute;
    bottom: 10px;
    left: 10px;
}

.audio-button {
    background: none;
    border: none;
    color: #5a3a22;
    cursor: pointer;
    font-size: 14px;
    position: absolute;
    top: 10px;
    right: 10px;
}

.author {
    text-indent: 20px;
}

.coffee-link {
    position: absolute;
    width:80%;
    /* height: 80%; */
    /* bottom: 20px; */
    left: 50px;
}

.bmc {
    width: 25%;
    height: 25%;
}

@media screen and (max-width: 767px) {
    .video-container iframe {
        width: 320%;
        height: 180%;
        left: -80%;
        top: -40%;
    }

    /* .title {
        font-size: medium;
    } */

    .daily-content-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 80vh;
    }

    .daily-content {
        color: #5a3a22;
        background: #f4e4d7;
        width: 60vw;
        height: auto;
        padding: 30px;
        border: 1px solid #b6a08e;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
        overflow: hidden;
        /* position: absolute; */
        position: relative;
        padding: 10px 30px;
        top:10%;
        bottom: 10%;
    }

    .quote {
        width: auto;
        height: auto;
        padding: 10px;
    }

    .game {
        width: auto;
        height: auto;
    }

    .credits {
        width: auto;
        height: 45vh;
    }

    .credits a {
        word-wrap: break-word;
        overflow-wrap: break-word;
        display: inline-block;
        max-width: 95%;
    }

    .audio-button {
        font-size: 20px;
        position: absolute;
        top: 5px;
        right: 5px;
    }

    .next-button {
        font-size: 20px;
        position: absolute;
        bottom: 5px;
        right: 5px;
        padding-top: 20%;
    }

    .last-button {
        font-size: 20px;
        position: absolute;
        bottom: 5px;
        left: 5px;
        padding-top: 20%;
    }


    .coffee-link {
        position: absolute;
        width:50%;
        left: 50px;
    }

    .bmc {
        width: 70%;
        height: 70%;
        padding-bottom: 10%;
    }
}
</style>