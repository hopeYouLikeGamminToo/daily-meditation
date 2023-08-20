<template>
    <div class="wisdom-tree-container">
        <button class="refresh-button" @click="resetGame"><i class="fa-solid fa-rotate-right"></i></button>
        <div class="wisdom-tree">
            <!-- Render tree elements based on correct guesses -->
            <transition name="fade" mode="out-in">
                <img class="tree" :src="treeElements[currentTreeIndex]" :key="currentTreeIndex" />
            </transition>
        </div>
        <div class="controls">
            <p class="hint">{{ displayedWord }} </p>
            <p class="game-over" v-if="this.allLettersGuessed">That's it! Well done!</p>
            <p class="game-over" v-if="incorrectGuesses.length >= 5">Word: {{ this.word }}</p>
        </div>
        <div class="alphabet">
            <div v-for="letter in alphabet" :key="letter"
                :class="{ 'circled': correctGuesses.includes(letter), 'crossed-out': incorrectGuesses.includes(letter) }"
                @click="makeGuess(letter)">{{ letter }}</div>
        </div>
    </div>
</template>



<script>
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
    computed: {
        displayedWord() {
            if (this.word && this.word.startsWith("Error:")) {
                return this.word;
            }
            return this.word.split('').map(letter => this.correctGuesses.includes(letter.toUpperCase()) ? letter : '_').join(' ');
        }
    },
    mounted() {
        this.restoreGameState();
    },
    methods: {
        makeGuess(letter) {
            if (this.gameOver) return; 

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
                if (this.incorrectGuesses.length >= 5 || this.allLettersGuessed) {
                        this.gameOver = true;
                        console.log("Game Over!");
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
            if (this.currentTreeIndex < this.treeElements.length - 1) {
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

            // If the game has already been played
            if (savedState && savedState.gameOver) {
                this.gameOver = true;
                return; // Don't allow playing again
            }

            // If there's a saved state, restore it
            if (savedState) {
                this.correctGuesses = savedState.correctGuesses || [];
                this.incorrectGuesses = savedState.incorrectGuesses || [];
                // Restore other relevant state variables
            }
        }
    },
};
</script>

<style>
.tree {
    width: 20%;
    position: relative;
    left: 20%;
    padding-top: 2%;
}

.fade-enter-active, .fade-leave-active {
    transition: opacity 1s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
    transition: opacity 1s;
    opacity: 0;
}


.alphabet {
    display: grid;
    grid-template-columns: repeat(5, 11.5%);
    gap: 3px;
    padding-top: 0%;
    padding-bottom: 30px;
}

.hint {
    font-size: 30px;
    position: relative;
    left: 18%;
    padding-top: 0%;
}

.alphabet>div {
    width: auto;
    height: auto;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    padding-bottom: 5px;
}

.alphabet>div.circled {
    border: 2px solid green;
    border-radius: 50%;
}

.alphabet>div.crossed-out {
    text-decoration: line-through;
    color: red;
}

.game-over {
    position: relative;
    font-size: 25px;
    left: 20%;
}

.refresh-button {
    background: none;
    border: none;
    color: #5a3a22;
    cursor: pointer;
    font-size: 14px;
    position: absolute;
    top: 10px;
    left: 10px;
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
        font-size:20px;
        /* padding-bottom: 10%; */
    }

    .hint {
        font-size: 30px;
        padding-top: 0%;
        position: relative;
        left: 7%;
    }

    .game-over {
        position: relative;
        font-size: 20px;
        left: 25%;
    }
}
</style>
