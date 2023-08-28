<template>
    <div class="daily-content-container">
        <div class="daily-content">
            <button class="audio-button" @click="toggleMute"><i class="fa-solid fa-music"></i></button>
            <button class="settings-button" @click="showSettings = !showSettings" v-if="index != 0"><i
                    class="fa-solid fa-gear"></i></button>
            <button @click="nextCard" class="next-button" v-if="index != 0 &&  !showSettings"><i class="fa-solid fa-arrow-right"></i></button>
            <button @click="lastCard" class="last-button" v-if="index != 0 &&  !showSettings"><i class="fa-solid fa-arrow-left"></i></button>

            <div class="login" v-if="index == 0">
                <h2 class="title">Wisdom Tree - Daily Word Game</h2>
                <UserLogin @login-complete="handleLoginSuccess"></UserLogin>
            </div>

            <div class="settings" v-if="showSettings">
                <h2 class="title">Settings</h2>
                <UserSettings v-if="showSettings" @sign-out="handleSignOut"></UserSettings>
            </div>

            <div class="quote" v-if="index == 1 && !showSettings">
                <h2 class="title">{{ currentDate }}</h2>
                <p>{{ quote }}</p>
                <p class="author">{{ author }}</p>
            </div>

            <div class="game" v-if="index == 2 && !showSettings">
                <h2 class="title">Wisdom Tree</h2>
                <UserSettings v-if="showSettings" @sign-out="handleSignOut"></UserSettings>
                <WisdomTree :quote="quote" :word="word"></WisdomTree>
            </div>
            <div class="credits" v-if="index == 3 && !showSettings">
                <h2 class="title">Credits</h2>
                <UserSettings v-if="showSettings" @sign-out="handleSignOut"></UserSettings>
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
import { getDate, getContent } from '../scripts/DailyMeditation'
import WisdomTree from './WisdomTree.vue';
import UserLogin from './UserLogin.vue';
import UserSettings from './UserSettings.vue';



export default {
    props: ['toggleMute', 'sharedData'],
    components: {
        UserLogin,
        UserSettings,
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
            showSettings: false,
            aiCredits: "https://platform.openai.com/docs/api-reference/chat",
            quoteCredits: "https://github.com/lukePeavey/quotable",
            developerCredits: "https://howl0893.github.io/",
            currentDate: getDate(),
            content: null,
            quote: "Finding the quote of the day...",
            author: null,
            word: null
        };
    },
    async mounted() {
        this.content = await getContent();
        console.log(this.content);
        this.quote = this.content.quote['content'];
        this.author = this.content.quote['author'];
        this.word = this.content.word;

        console.log(this.quote);
        console.log(`\t${this.author}`);
        console.log(this.word);
    },
    methods: {
        handleLoginSuccess() {
            this.nextCard();
        },
        handleSignOut() {
            this.index = 0;
            this.showSettings = false;
        },
        nextCard() {
            this.index += 1;
            if (this.index > 3) {
                this.index = 1;
            }
        },
        lastCard() {
            this.index -= 1;
            if (this.index < 1) {
                this.index = 3;
            }
        }

    }
};
</script>
  
<style scoped>
.daily-content-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}

.daily-content {
    color: #5a3a22;
    background: #f4e4d7;
    width: 25vw;
    height: auto;
    padding: 22px;
    border: 1px solid #b6a08e;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    position: absolute;
    /* background-image: url('../assets/scroll.png');
    background-size: cover;
    background-repeat: no-repeat; 
    background-position: center; To center the image */
}

.title {
    margin-top: 5px;  /* Assuming you have a margin, set it to zero */
}

.quote {
    width: auto;
    height: auto;
}

.settings {
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

.settings-button {
    background: none;
    border: none;
    color: #5a3a22;
    cursor: pointer;
    font-size: 14px;
    position: absolute;
    top: 40px;
    right: 10px;
}

.author {
    text-indent: 20px;
}

.coffee-link {
    position: absolute;
    width: 80%;
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
        border: 1px solid #b6a08e;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
        overflow: hidden;
        /* position: absolute; */
        position: relative;
        padding: 10px 30px;
        top: 10%;
        bottom: 10%;
    }

    .quote {
        width: auto;
        height: auto;
        padding: 15px;
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

    .settings-button {
        font-size: 20px;
        position: absolute;
        top: 40px;
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
        width: 50%;
        left: 50px;
    }

    .bmc {
        width: 70%;
        height: 70%;
        padding-bottom: 10%;
    }
}</style>