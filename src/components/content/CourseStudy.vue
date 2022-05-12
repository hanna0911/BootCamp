<template>
<v-row style="margin: 1%">
  <v-col cols=3>
    <v-list>
      <v-list-item-group>
        <template v-for='lesson_item in lesson_items'>
          <v-list-item :key='lesson_item.lessonID'>
            <v-list-item-content>
              <v-list-item-title class="text-h6" v-text='lesson_item.name'/>
              <v-list-item-subtitle style="margin-top: 5px" v-text='lesson_item.intro'/>
              <v-list>
                <v-list-item-group>
                  <template v-for='courseware in courseware_items[lesson_item.lessonID]'>
                    <v-list-item :key='courseware.coursewareID'>
                      <v-list-item-content @click='showCourseware(courseware)'>
                        <v-list-item-title class="text-h7" v-text='courseware.name'/>
                        <v-list-item-subtitle v-text="courseware.uploadTime.split('T')[0] + ' ' + courseware.uploadTime.split('T')[1].split('.')[0]"/>
                      </v-list-item-content>
                    </v-list-item>
                  </template>
                </v-list-item-group>
              </v-list>
            </v-list-item-content>
            <a :href="'https://view.officeapps.live.com/op/view.aspx?src='+ docLink">点击查看</a>
            <v-btn v-if="GLOBAL.contentDisplayUser && !GLOBAL.contentDisplayAddif" absolute top right @click="finishLesson(lesson_item.lessonID)">{{lesson_item.isFinished ? '已学完该讲': '学完该讲'}}</v-btn>
          </v-list-item>
        </template>
      </v-list-item-group>
    </v-list>
  </v-col>
  <v-col v-if='showAnything' cols=9>
    <video-player v-if='showType === "video"' class="video-player"
      ref="videoPlayer"
      :playsinline="true"
      :options="playerOptions">
    </video-player>
    <div v-else-if="'msdoc'">
      <!-- <iframe id="iframe1" width="960" height="720" frameborder='no' border='0' marginwidth='0' marginheight='0' scrolling='no' allowtransparency='yes' -->
      <iframe id="iframe"
      :src="'https://view.officeapps.live.com/op/view.aspx?src=' + docLink"></iframe>
    </div>
  </v-col>
</v-row>
</template>

<script>
import COMM from "@/utils/Comm"
import VideoPlayer from "./VideoDisplay"

export default ({
  name: "CourseStudy",
  inject: ['GLOBAL'],
  components: {
    VideoPlayer,
  },
  props: {
    contentID: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      lesson_items: [],
      courseware_items: {},

      showAnything: false,
      toShowCourseware: '',
      showType: '',

      playerOptions: {
        playbackRates: [0.5, 1.0, 1.5, 2.0], 
        autoplay: false, 
        controls: true,
        muted: false, 
        loop: false, 
        // 建议浏览器在<video>加载元素后是否应该开始下载视频数据。auto浏览器选择最佳行为,立即开始加载视频（如果浏览器支持）
        preload: 'auto', 
        language: 'zh-CN',
        aspectRatio: '16:9',
          // 当true时，Video.js player将拥有流体大小。换句话说，它将按比例缩放以适应其容器。
        fluid: true,
        sources: [{
            src: "http://127.0.0.1:8000/files/test.mp4",
            type: "video/mp4"
        }],
        poster: '', 
        //允许覆盖Video.js无法播放媒体源时显示的默认信息。
        notSupportedMessage: '此视频暂无法播放，请稍后再试',
        controlBar: {
            timeDivider: true,
            durationDisplay: true,
            remainingTimeDisplay: false,
            //全屏按钮
            fullscreenToggle: true  
        }
      },

      docLink: '',
    }
  },
  methods: {
    async getAll() {
      this.showAnything = false
      var res = await COMM.content_lesson_list(this.contentID)
      this.lesson_items = res.lessons
      for(var lesson_item of this.lesson_items) {
        res = await COMM.lesson_courseware_list(lesson_item.lessonID)
        res = res.lessons
        for(var courseware of res) {
          // 返回来的是个绝对地址。我把 /files/ 之前的部分都去掉了，就是相对地址
          courseware['url'] = window.location.origin + '/files/'.concat(courseware.url.split('/files/').slice(1))
        }
        this.courseware_items[lesson_item.lessonID] = res
      }
      this.$forceUpdate()
      // console.log(this.lesson_items)
      // console.log(this.courseware_items)
    },
    showCourseware(info) {
      if(this.toShowCourseware === info.coursewareID) {
        return
      }
      console.log(info)
      this.toShowCourseware = info.coursewareID
      var suffix = info.url.split('.').slice(-1)[0]
      if(suffix === 'mp4') {
        this.showType = 'video'
        this.playerOptions.sources = {
          src: info.url,
          type: "video/mp4",
        }
      }
      else if(suffix === 'ppt' || suffix === 'pptx' || suffix === 'pdf') {
        console.log("this is a doc")
        this.showType = 'msdoc'
        this.docLink = info.url
      }
      else {
        this.showType = 'notSupport'
      }
      this.showAnything = true
    },
    async finishLesson(lessonID) {
      await COMM.finish_lesson(this.GLOBAL.username, lessonID)
    }
  },
  watch: {
    contentID() {
      this.getAll()
    }
  },
  created() {
    this.getAll()
    console.log(window.location.origin)
  },
  beforeDestroy() {
  }
})
</script>

<style>
iframe {
  display: block;
  border: none;
  height: 90vh;
  width: 100%;
}
</style>