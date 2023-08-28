<template>
    <div class="wisdom-tree-container">
        <!-- <button class="refresh-button" @click="resetGame"><i class="fa-solid fa-rotate-right fa-2xl"></i></button> -->
        <div class="wisdom-tree">
            <!-- Render tree elements based on correct guesses -->
            <transition name="fade" mode="out-in">
                <img class="tree" :src="treeElements[currentTreeIndex]" :key="currentTreeIndex" />
            </transition>
        </div>
        <div class="controls">
            <p class="hint" :style="{ left: hintLeft }">{{ displayedWord }} </p>
            <p class="game-over" :style="{ left: gameOverLeft }" v-if="this.allLettersGuessed">That's it! Well done!</p>
            <p class="game-over" :style="{ left: gameOverLeft }" v-if="incorrectGuesses.length >= 5">Word: {{ this.word }}
            </p>
        </div>
        <div class="alphabet">
            <div v-for="letter in alphabet" :key="letter"
                :class="{ 'circled': correctGuesses.includes(letter), 'crossed-out': incorrectGuesses.includes(letter) }"
                @click="makeGuess(letter)">{{ letter }}</div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    props: ['quote', 'word'],
    data() {
        return {
            correctGuesses: [],
            incorrectGuesses: [],
            currentGuess: '',
            treeElements: [require("../assets/bonsai/bonsai0-nobg.png"), require("../assets/bonsai/bonsai1-nobg.png")],
            alphabet: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split(''),
            gameOver: false,
            allLettersGuessed: false,
            currentTreeIndex: 0, // Add this line
        };
    },
    created() {
        console.log('WisdomTree created');
    },
    computed: {
        hintLeft() {
            // Calculate left offset based on the displayedWord length
            // Adjust this formula as per your needs
            return 17 - (this.displayedWord.length * 0.25) + "%";
        },
        gameOverLeft() {
            const gameOverText = this.allLettersGuessed ? "That's it! Well done!" : `Word: ${this.word}`;
            // Calculate left offset based on the gameOverText length
            // Adjust this formula as per your needs
            return 17 - (gameOverText.length * 0.05) + "%";
        },
        displayedWord() {
            if (this.word && this.word.startsWith("Error:")) {
                return "Unexpected Error."
            }
            return this.word.split('').map(letter => this.correctGuesses.includes(letter.toUpperCase()) ? letter : '_').join(' ');
        }
    },
    async mounted() {
        const username = localStorage.getItem('username');
        if (!username) {
            console.error('No username found in storage.');
            return;
        }
        const response = await axios.get('/get_user', { params: { username: username } });

        if (response.data.last_game) {
            const lastGameDate = new Date(response.data.last_game);

            const currentTime = new Date();
            const offsetMST = -7 * 60 * 60 * 1000; // Offset in milliseconds
            const currentTimeMST = new Date(currentTime.getTime() + offsetMST);

            // Set time to midnight for both dates
            lastGameDate.setHours(0, 0, 0, 0);
            currentTimeMST.setHours(0, 0, 0, 0);

            console.log("Last game date:", lastGameDate);
            console.log("Current time MST:", currentTimeMST);

            console.log("Is lastGameDate < currentTimeMST?", lastGameDate.getTime() < currentTimeMST.getTime());

            // Compare dates
            if (lastGameDate.getTime() < currentTimeMST.getTime()) {
                this.resetGame();
            } else {
                this.restoreGameState();
            }
        }

        // window.addEventListener("beforeunload", this.handleBeforeUnload);
    },
    // beforeUnmount() {
    //     window.removeEventListener("beforeunload", this.handleBeforeUnload);
    // },
    methods: {
        async updateStats(win) {
            try {
                const params = {
                    username: localStorage.getItem('username'),
                    win: win
                };

                // TODO: not sure why but this request is defaulting to port 8888 - hardcoded locally host API
                const response = await axios.post('http://localhost:8000/update_stats', null, { params });
                console.log('updateStats:', response.data);

            } catch (err) {
                console.error('Error saving updateStats:', err);
            }
        },
        makeGuess(letter) {
            if (this.gameOver) return

            console.log(letter);
            const guess = letter.toUpperCase(); // Making sure the guess is uppercase

            if (!this.correctGuesses.includes(letter) && !this.incorrectGuesses.includes(letter)) {
                let found = false;

                for (let i = 0; i < this.word.length; i++) {
                    if (this.word[i].toUpperCase() === guess) {
                        found = true;
                        if (!this.correctGuesses.includes(guess)) {
                            this.correctGuesses.push(guess);
                        }
                    }
                }

                if (found) {
                    this.addTreeElement();
                } else {
                    this.incorrectGuesses.push(guess);
                    this.removeTreeElement();
                }

                this.allLettersGuessed = this.word.split('').every(letter => this.correctGuesses.includes(letter.toUpperCase()));
                if (this.incorrectGuesses.length >= 5) {
                    this.gameOver = true;
                    console.log("loser loser");
                    this.updateStats(0);
                }
                if (this.allLettersGuessed) {
                    this.gameOver = true;
                    console.log("winner winner");
                    this.updateStats(1);
                }
            }

            // Save the current state
            const gameState = {
                correctGuesses: this.correctGuesses,
                incorrectGuesses: this.incorrectGuesses,
                gameOver: this.gameOver,
                // Other relevant state variables
            };
            localStorage.setItem('gameState', JSON.stringify(gameState));

        },
        addTreeElement() {
            // Increment currentTreeIndex by 1, but don't exceed the length of the treeElements array
            if (this.currentTreeIndex < this.treeElements.length - 1 && this.correctGuesses.length > 2) {
                this.currentTreeIndex++;
            }
            console.log("correct!")
        },
        removeTreeElement() {
            // Logic to remove or wither elements from the tree
            // Modify this function to suit the tree growing mechanic
            console.log("incorrect!")
        },
        resetGame() {
            // Clear the saved state from LocalStorage
            localStorage.removeItem('gameState');

            // Reset the component's state
            this.correctGuesses = [];
            this.incorrectGuesses = [];
            this.gameOver = false;
            this.allLettersGuessed = false;
            this.currentTreeIndex = 0;
        },
        restoreGameState() {
            // Retrieve the saved state
            const savedState = JSON.parse(localStorage.getItem('gameState'));

            // If there's a saved state, restore it
            if (savedState) {
                this.correctGuesses = savedState.correctGuesses || [];
                this.incorrectGuesses = savedState.incorrectGuesses || [];
                // Restore other relevant state variables
            }

            // If the game has already been played
            if (savedState && savedState.gameOver) {
                this.gameOver = true;
                return; // Don't allow playing again
            }
        },
        handleBeforeUnload(event) {
            if (this.gameOver) {
                this.resetGame();
            } else {
                // Optionally, warn the user about potential loss of data
                event.preventDefault();
                event.returnValue = 'You have unsaved changes, are you sure you want to leave?';
            }
        },

    },
};
</script>

<style scoped>
.tree {
    width: 20%;
    position: relative;
    left: 15%;
    padding-top: 2%;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 1s;
}

.fade-enter,
.fade-leave-to

/* .fade-leave-active in <2.1.8 */
    {
    transition: opacity 1s;
    opacity: 0;
}


.alphabet {
    display: grid;
    grid-template-columns: repeat(5, 9.75%);
    gap: 3px;
    padding-top: 0%;
    padding-bottom: 30px;
}

.hint {
    font-size: 30px;
    position: relative;
    left: 17%;
    padding-top: 0%;
}

.alphabet>div {
    width: 2vw;
    height: 3vh;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    padding-bottom: 5px;
    margin-left: 35%;
}

.alphabet>div.circled {
    border: 2px solid green;
    border-radius: 50%;
}

.alphabet>div.crossed-out {
    position: relative;
    color: black;
    /* The letter will remain black */
}

.alphabet>div.crossed-out::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 0;
    right: 0;
    height: 2px;
    background: red;
    /* The crossing line will be red */
    transform: rotate(0deg);
    /* For straight line */
}

.alphabet>div.crossed-out::after {
    content: '';
    position: absolute;
    background: red;
    transform: rotate(90deg);
}

.game-over {
    position: relative;
    font-size: 25px;
    left: 17%;
}

.refresh-button {
    background: none;
    border: none;
    color: #5a3a22;
    cursor: pointer;
    font-size: 7px;
    position: absolute;
    top: 75px;
    right: 10px;
}

@media screen and (max-width: 767px) {
    .tree {
        width: 50%;
        position: relative;
        left: 25%;
    }

    .alphabet {
        display: grid;
        grid-template-columns: repeat(5, 23%);
        gap: 5px;
        padding-top: 0%;
        padding-right: 20%;
        font-size: 20px;
        /* padding-bottom: 10%; */
    }

    .hint {
        font-size: 30px;
        padding-top: 0%;
        position: relative;
        left: 7%;
    }

    .refresh-button {
        background: none;
        border: none;
        color: #5a3a22;
        cursor: pointer;
        font-size: 10px;
        position: absolute;
        top: 80px;
        right: 5px;
    }

    .game-over {
        position: relative;
        font-size: 20px;
        left: 17%;
    }
}
</style>
