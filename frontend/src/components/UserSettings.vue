<template>
    <div class="container">
        <div class="input-container">
            <label class="input-label">Enable Location</label>
            <input type="checkbox" id="enableLocation" v-model="enableLocation">
        </div>
        <div class="input-container">
            <label for="username" class="input-label">Username</label>
            <input id="username" type="text" v-model="username" placeholder="Username">
        </div>
        <div class="input-container">
            <label for="email" class="input-label">Email</label>
            <input id="email" type="email" v-model="email" placeholder="Email">
        </div>
        <div class="input-container">
            <label for="phone_number" class="input-label">Phone</label>
            <input id="phone_number" type="tel" v-model="phone_number" placeholder="Phone Number">
        </div>
        <div class="input-container">
            <label for="currentPassword" class="input-label">Current Password</label>
            <input id="currentPassword" type="password" v-model="currentPassword" placeholder="Current Password">
        </div>
        <div class="input-container">
            <label for="newPassword" class="input-label">New Password</label>
            <input id="newPassword" type="password" v-model="newPassword" placeholder="New Password">
        </div>

        <!-- Save & Sign Out Buttons -->
        <button type="submit" @click="saveSettings">Save</button>
        <button class="signout-button" @click="signOut">Sign Out</button>
    </div>
</template>
  
<script>
import axios from 'axios';

export default {
    data() {
        return {
            enableLocation: false,
            username: null,
            email: null,
            phone_number: null,
            currentPassword: null,
            newPassword: null,
        };
    },
    async created() {
        try {
            const username = localStorage.getItem('username'); // Retrieve username from localStorage or other storage
            if (!username) {
                console.error('No username found in storage.');
                return;
            }
            const response = await axios.get('/get_user', { params: { username: username } });

            if (response.data) {
                this.enableLocation = response.data.enableLocation || false;
                this.username = response.data.username || '';
                this.email = response.data.email || '';
                this.phone_number = response.data.phone_number || '';
            }
        } catch (err) {
            console.error('Error fetching user data:', err);
        }
    },
    methods: {
        async saveSettings() {
            try {
                const params = {
                    currentUsername: localStorage.getItem('username'),
                    newUsername: this.username,
                    email: this.email,
                    phone_number: this.phone_number,
                    currentPassword: this.currentPassword,
                    newPassword: this.newPassword       
                };

                // TODO: not sure why but this request is defaulting to port 8888 - hardcoded locally host API
                const response = await axios.post('http://localhost:8000/update_user', null, {params});

                console.log('User settings saved:', response.data);
            } catch (err) {
                console.error('Error saving user settings:', err);
            }
        },
        signOut() {
            localStorage.removeItem('username');
            localStorage.removeItem('password');
            this.$emit('sign-out');
        }
    }
};
</script>


<style scoped>
.container {
    display: flex;
    flex-direction: column;
    /* align-items: center;
    justify-content: center; */
    /* max-height: 500px; */
    /* Or any height you prefer */
    /* overflow-y: auto; */
    /* Enable vertical scrolling */
    width: 50%;
    margin-left: 25%;
}

input {
    margin: 10px;
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

.input-container {
    display: flex;
    flex-direction: row;
    align-items: center;
    margin-bottom: 10px;
    justify-content: flex-start;
}

.input-label {
    font-weight: bold;
    width: 55px;
    /* Adjust based on your needs */
}

input {
    flex-grow: 1;
}

@media screen and (max-width: 767px) {
    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: auto;
        width: auto;
        margin-left: 5%;
    }
}
</style>