<template>
    <div id="app">
        <NatureVideo ref="natureVideoRef" @youtube-credits="updateSharedData"></NatureVideo>
        <DailyContent :toggleMute="toggleMuteMethod" :shared-data="sharedData"></DailyContent>
    </div>
</template>
  
<script>
import NatureVideo from './components/NatureVideo.vue';
import DailyContent from './components/DailyContent.vue';

export default {
    name: 'App',
    components: {
        NatureVideo,
        DailyContent
    },
    data() {
        return {
            sharedData: null // The data to be shared between children
        };
    },

    methods: {
        toggleMuteMethod() {
            this.$refs.natureVideoRef.toggleMute();
        },
        updateSharedData(value) {
            this.sharedData = value; // Update the shared data
        }
    }
}
</script>

<style>
@font-face {
  font-family: 'berylium';
  src: url('./assets/fonts/berylium/berylium.otf') format('opentype');
}

body {
    font-family: 'berylium';
    overflow: hidden;
}
</style>
  