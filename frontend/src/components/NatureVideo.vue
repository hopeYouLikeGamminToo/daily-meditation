<template>
    <div class="video-container">
        <div ref="youtubePlayer"></div>
        <div class="video-overlay"></div>
    </div>
</template>
  
<script>
/* global YT */

export default {
    data() {
        return {
            player: null,
            videoID: 'glENND73k4Q', // winter: CUIdMusnugs, ireland: ycDLfQ1Cv_Y, autumn: glENND73k4Q, forest: VNu15Qqomt8, summer: QR3lp0ptpy8, yellowstone: prHBhSsrkbU
        };
    },
    mounted() {
        this.loadYouTubeAPI();
        this.$emit('youtube-credits', `https://www.youtube.com/watch?v=${this.videoID}`); 
    },
    methods: {
        loadYouTubeAPI() {
            const tag = document.createElement('script');
            tag.src = 'https://www.youtube.com/iframe_api';
            const firstScriptTag = document.getElementsByTagName('script')[0];
            firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

            if (!window.onYouTubeIframeAPIReady) {
                window.onYouTubeIframeAPIReady = () => {
                    this.initPlayer();
                };
            }
        },
        toggleMute() {
            // console.log("toggle mute!");
            if (this.player.isMuted()) {
            this.player.unMute();
            } else {
            this.player.mute();
            }
        },
        initPlayer() {
            this.player = new YT.Player(this.$refs.youtubePlayer, {
                width: '100%',
                height: '100%',
                videoId: this.videoID,
                playerVars: {
                    autoplay: 1,
                    controls: 0,
                    showinfo: 0,
                    loop: 1,
                    mute: 1,
                    playlist: this.videoID,
                    modestbranding: 1,
                    start: 200,
                },
                events: {
                    onReady: (event) => {
                        event.target.playVideo();
                    },
                },
            });
        },
    },
};
</script>
  

<style>
.video-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    overflow: hidden;
}

.video-container iframe {
    position: absolute;
    width: 130%;
    height: 130%;
    left: -15%;
    top: -15%;
}

.video-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 1;
}

.unmute-button {
  position: absolute;
  bottom: 50px;
  left: 50%;
  transform: translateX(-50%);
  padding: 10px 20px;
  background-color: #ffffff;
  border: none;
  cursor: pointer;
  font-size: 16px;
  z-index: 2;
}

.unmute-button:hover {
  background-color: #f0f0f0;
}

@media screen and (max-width: 767px) and (orientation: portrait) {
    .video-container iframe {
        width: 400%;
        height: 400%;
        left: -150%;
        top: -150%;
    }
}

</style>
