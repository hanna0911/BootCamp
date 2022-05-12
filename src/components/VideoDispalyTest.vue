<template>
  <div>
    <VideoPlayer :options="videoOptions"/>
  </div>
</template>

<script>
import VideoPlayer from "./content/VideoDisplay";

export default {
  name: "VideoExample",
  components: {
    VideoPlayer
  },
  data() {
    return {
      videoOptions: {
        autoplay: true,
        controls: true,
        sources: [
          {
            src: "/api/video/?path=test.mp4",
            type: "video/mp4"
          }
        ]
      }
    };
  }
};
</script>

<style>
@import 'video.js/dist/video-js.css';
</style>