<template>
<v-container>
    <h2 class="px-4 pt-4 pb-3 font-weight-black">导师培训</h2>

    <!-- 导师旅程 -->
    <v-row style="margin: 0.5%">
        <v-col>
            <v-card>
                <v-card-subtitle>我的导师旅程开始于 <strong>{{ tutorInfo.startDate.split('T')[0] }} {{tutorInfo.startDate.split('T')[1]}}</strong></v-card-subtitle>
                <v-card-text>
                  <v-row no-gutters>
                    <!-- 课程进度 -->
                    <v-col>
                      <div class="circleBox">
                        <el-progress 
                          :show-text="false" 
                          type="circle"
                          :width="100" 
                          :percentage="tutorInfo.courseProgress">
                        </el-progress>
                        <div class="circleCenter">
                            <h1 v-if="tutorInfo.courseProgress < 100 && tutorInfo.courseProgress > 0">&nbsp;{{ tutorInfo.courseProgress }}%</h1>
                            <h1 v-else-if="tutorInfo.courseProgress === 0">&nbsp;&nbsp;&nbsp;{{ tutorInfo.courseProgress }}%</h1>
                            <h1 v-else>{{ tutorInfo.courseProgress }}%</h1>
                            <p>课程</p>
                        </div>
                      </div>
                    </v-col>
                    <!-- 考试进度 -->
                    <v-col>
                      <div class="circleBox">
                        <el-progress 
                          :show-text="false" 
                          type="circle"
                          :width="100" 
                          :percentage="tutorInfo.examProgress">
                        </el-progress>
                        <div class="circleCenter">
                            <h1 v-if="tutorInfo.examProgress < 100 && tutorInfo.examProgress > 0">&nbsp;{{ tutorInfo.examProgress }}%</h1>
                            <h1 v-else-if="tutorInfo.examProgress === 0">&nbsp;&nbsp;&nbsp;{{ tutorInfo.examProgress }}%</h1>
                            <h1 v-else>{{ tutorInfo.examProgress }}%</h1>
                            <p>考试</p>
                        </div>
                        <div style="margin-top: 10px">
                          <h3>培训</h3>
                        </div>
                      </div>
                    </v-col>
                    <!-- 任务进度 -->
                    <v-col>
                      <div class="circleBox">
                        <el-progress 
                          :show-text="false" 
                          type="circle"
                          :width="100" 
                          :percentage="tutorInfo.taskProgress">
                        </el-progress>
                        <div class="circleCenter">
                            <h1 v-if="tutorInfo.taskProgress < 100 && tutorInfo.taskProgress > 0">&nbsp;{{ tutorInfo.taskProgress }}%</h1>
                            <h1 v-else-if="tutorInfo.taskProgress === 0">&nbsp;&nbsp;&nbsp;{{ tutorInfo.taskProgress }}%</h1>
                            <h1 v-else>{{ tutorInfo.taskProgress }}%</h1>
                            <p>任务</p>
                        </div>
                      </div>
                    </v-col>
                    <!-- 分割线 -->
                    <!-- <v-col>
                      <v-divider style="margin-top: 52px"/>
                    </v-col> -->
                    <!-- 评价 -->
                    <!-- <v-col>
                      <div class="circleBox">
                        <el-progress 
                          :show-text="false" 
                          type="circle"
                          :width="100" 
                          :percentage="tutorInfo.evaluateProgress">
                        </el-progress>
                        <div class="circleCenter">
                            <h1 v-if="tutorInfo.evaluateProgress < 100">&nbsp;{{ tutorInfo.evaluateProgress }}%</h1>
                            <h1 v-else>{{ tutorInfo.evaluateProgress }}%</h1>
                            <p>评价</p>
                        </div>
                        <div style="margin-top: 10px">
                          <h3>评价</h3>
                        </div>
                      </div>
                    </v-col> -->
                    <!-- 分割线 -->
                    <v-col>
                      <v-divider style="margin-top: 52px"/>
                    </v-col>
                    <!-- 毕业证书 -->
                    <v-col>
                      <div class="circleBox">
                        <!-- <img :src="tutorInfo.certificate" width="100"> -->
                        <div v-if="tutorInfo.graduateDate === '未毕业'" style="margin-top: 40px">
                          <h2><strong>未毕业</strong></h2>
                        </div>
                        
                        <div v-else style="margin-top: 30px">
                          <h2><strong>已毕业</strong></h2>
                          <strong><p>{{ tutorInfo.graduateDate.split('T')[0] }} {{ tutorInfo.graduateDate.split('T')[1] }}</p></strong>
                        </div>
                      </div>
                    </v-col>
                  </v-row>
                </v-card-text>
            </v-card>
        </v-col>
    </v-row>

    <!-- content内容：课程、考试、任务 -->
    <content-display :showAudience="'teacher'"></content-display>

</v-container>
</template>

<script>
import ContentDisplay from './content/ContentDisplay.vue'
import COMM from "@/utils/Comm";

export default ({
    name: "LeadNewcomer",
    inject: ['GLOBAL'],
    components: {
      ContentDisplay,
    },
    data() {
        return {
            name: "",
            tutorInfo: {  // 导师旅程相关数据，从后端获取！
              startDate: '',
              courseProgress: '',
              examProgress: '',
              taskProgress: '',
              evaluateProgress: '',  // TODO
              isGraduate: "",
              graduateDate: '',  // TODO
              // certificate: 'https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fbkimg.cdn.bcebos.com%2Fpic%2F3801213fb80e7bec5c745b6f252eb9389a506b95&refer=http%3A%2F%2Fbkimg.cdn.bcebos.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1652891023&t=95787fffcddad7af9d8633748f291448', // 证书图片
            },
            shownView: "course",  // 只会是 course, exam, task 三种之一，初始化为course
            // 三个visible变量有且恰有一个为true，通过检测shownView变量变化来修改，初始显示课程(course)
            courseVisible: true,
            examVisible: false,
            taskVisible: false,
            courseInfo: [  //
                {
                    courseName: '微积分',
                    courseIntro: '小学一年级课程',
                    lessonNum: 12,
                    finishLessons: 7,
                    // course dialog
                    courseDialog: false,
                    notifications: false,
                    sound: true,
                    widgets: false,
                    courseLink: 'https://view.officeapps.live.com/op/view.aspx?src=http%3a%2f%2fvideo.ch9.ms%2fbuild%2f2011%2fslides%2fTOOL-532T_Sutter.pptx'
                },
                {
                    courseName: '数据结构',
                    courseIntro: '小学二年级课程',
                    lessonNum: 15,
                    finishLessons: 6,
                    // course dialog
                    courseDialog: false,
                    notifications: false,
                    sound: true,
                    widgets: false,
                    courseLink: 'https://view.officeapps.live.com/op/view.aspx?src=newteach.pbworks.com%2Ff%2Fele%2Bnewsletter.docx'
                },
            ],
            examInfo: [
                {
                    examName: '游泳测试',
                    examTimestamp: new Date().getTime()
                },
                {
                    examName: '体育测试',
                    examTimestamp: new Date().getTime()
                },
            ],
            taskInfo: [
                {
                    taskName: '见一次导师',
                    taskIntro: '与被分配到的导师见面',
                    isFinished: true,
                },
                {
                    taskName: '见第二次导师',
                    taskIntro: '与被分配到的导师再见一次面',
                    isFinished: false,
                },
            ],

        }
    },
    methods: {
      teacher_board_summary_info(){
        COMM.teacher_board_summary_info().then(res => {
          console.log("get teacher board summary info success", res)
          this.tutorInfo = res.data;
        }, err => {console.log("get teacher board summary info fail ", err)})
      },
    },

    watch: {
        "shownView": {
            handler(newName) {
                this.courseVisible = (newName === "course")
                this.examVisible = (newName === "exam")
                this.taskVisible = (newName === "task")
            }
        }
    },
    created() {
      this.teacher_board_summary_info();
      this.GLOBAL.contentDisplayAddif = false
      this.GLOBAL.contentDisplayUser = true
      console.log('set: ', this.GLOBAL.contentDisplayAddif, this.GLOBAL.contentDisplayUser)
    },

    mounted() {
      this.teacher_board_summary_info();
      this.GLOBAL.contentDisplayAddif = false
      this.GLOBAL.contentDisplayUser = true
      console.log('set: ', this.GLOBAL.contentDisplayAddif, this.GLOBAL.contentDisplayUser)
    }
    // TODO
})
</script>