<template>
    <div class="container">
        <div>
            <label>Username</label>
            <input type="text" v-model="username" required />
            <!-- Length Check Messages -->
            <span v-if="lengthCheckFailed" style="color: red">Must be 5 characters</span>
            <span v-else-if="usernameChecked && !incorrectPassword">
                <span v-if="isUsernameAvailable" style="color:rgba(7, 102, 7, 0.704)">Available</span>
                <span v-else style="color:rgba(7, 102, 7, 0.704)">Welcome back</span>
            </span>
            <span v-if="incorrectPassword" style="color: red">Incorrect Password</span>
            <br />
            <label>Password </label>
            <input type="password" v-model="password" required />
        </div>
        <div class="btn-div">
            <button type="submit" @click="emailLogin">Login</button>
            <!-- <button>Google Sign In</button> -->
            <button @click="guestLogin">Play as Guest</button>
        </div>
    </div>
</template>

  
<script>
import axios from 'axios';
import _ from 'lodash';

export default {
    data() {
        return {
            username: '',
            password: '',
            isUsernameAvailable: false,
            usernameChecked: false,
            incorrectPassword: false,
            lengthCheckFailed: false
        };
    },
    created() {
        const savedusername = localStorage.getItem('username');
        const savedPassword = localStorage.getItem('password');

        if (savedusername && savedPassword) {
            this.username = savedusername;
            this.password = savedPassword;
            this.emailLogin();  // Automatically triggers login
        }
    },
    watch: {
        username: _.debounce(async function (newVal) {
            this.usernameChecked = false;
            try {
                const response = await axios.get('/check_availability', { params: { username: newVal } });
                this.isUsernameAvailable = response.data;
                this.usernameChecked = true;
                this.incorrectPassword = false; // Reset incorrectPassword flag
            } catch (err) {
                console.error("Couldn't check username availability:", err);
            }
        }, 300)
    },
    methods: {
        async emailLogin() {
            console.log('Email Login');

            if (this.username.length <= 4 || this.password.length <= 4) {
                this.lengthCheckFailed = true;
                return;
            }
            this.lengthCheckFailed = false;
            this.incorrectPassword = false;

            const signUpRequest = {
                email: this.username,
                username: this.username,
                password: this.password,
                login_type: 'email',
                google_id: null,
            };

            try {
                const response = await axios.post('/sign_up', signUpRequest);
                console.log('User created:', response.data);
                this.$emit('login-complete');
                localStorage.setItem('username', this.username);
                localStorage.setItem('password', this.password);
            } catch (err) {
                console.log('Error signing up:', err);
                if (err.response && err.response.status === 401) {
                    this.incorrectPassword = true;
                    localStorage.removeItem('username');
                    localStorage.removeItem('password');
                }
            }
        },
        async guestLogin() {
            this.$emit('login-complete');
            console.log('guest login');
        },
    },
};
</script>
  
<style scoped>
.container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: auto;
}

.btn-div {
    /* display: flex; */
    flex-direction: column;
    /* align-items: center; */
    /* justify-content: center; */
    /* height: auto; */
}

button {
    margin: 10px;
    background: none;
    /* border: none; */
    border-color: #b6a08e;
    border-radius: 10%;
    color: #5a3a22;
    cursor: pointer;
    font-size: 14px;
}

input {
    margin: 10px;
}
</style>
  