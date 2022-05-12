<template>
<v-container>
    <h2 class="px-4 pt-4 pb-3 font-weight-black">新人看板</h2>

    <!-- 新人旅程 -->
    <v-row style="margin: 0.5%">
        <v-col>
            <v-card>
                <v-card-subtitle>
                  <v-row>
                    <v-col>
                  我的新人旅程开始于 <strong>{{ newcomerInfo.startDate.split('T')[0] }} {{ newcomerInfo.startDate.split('T')[1] }}</strong>，
                  <p v-if="newcomerInfo.tutor !== '无'">我的导师是 <strong>{{ newcomerInfo.tutor }}</strong></p>
                  <p v-else>我暂无导师</p>
                    </v-col>
                    <v-col class="text-right">
                      <v-btn v-if="newcomerInfo.tutor !== '无'" large v-on:click="commitTeacher">给导师评价</v-btn>
                    </v-col>
                  </v-row>
                </v-card-subtitle>

                <v-card-text>
                  <v-row no-gutters>
                    <!-- 课程进度 -->
                    <v-col>
                      <div class="circleBox">
                        <el-progress 
                          :show-text="false" 
                          type="circle"
                          :width="100" 
                          :percentage="newcomerInfo.courseProgress">
                        </el-progress>
                        <div class="circleCenter">
                            <h1 v-if="newcomerInfo.courseProgress < 100 && newcomerInfo.courseProgress > 0">&nbsp;{{ newcomerInfo.courseProgress }}%</h1>
                            <h1 v-else-if="newcomerInfo.courseProgress === 0">&nbsp;&nbsp;&nbsp;{{ newcomerInfo.courseProgress }}%</h1>
                            <h1 v-else>{{ newcomerInfo.courseProgress }}%</h1>
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
                          :percentage="newcomerInfo.examProgress">
                        </el-progress>
                        <div class="circleCenter">
                            <h1 v-if="newcomerInfo.examProgress < 100 && newcomerInfo.examProgress > 0">&nbsp;{{ newcomerInfo.examProgress }}%</h1>
                            <h1 v-else-if="newcomerInfo.examProgress === 0">&nbsp;&nbsp;&nbsp;{{ newcomerInfo.examProgress }}%</h1>
                            <h1 v-else>{{ newcomerInfo.examProgress }}%</h1>
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
                          :percentage="newcomerInfo.taskProgress">
                        </el-progress>
                        <div class="circleCenter">
                            <h1 v-if="newcomerInfo.taskProgress < 100 && newcomerInfo.taskProgress > 0">&nbsp;{{ newcomerInfo.taskProgress }}%</h1>
                            <h1 v-else-if="newcomerInfo.taskProgress === 0">&nbsp;&nbsp;&nbsp;{{ newcomerInfo.taskProgress }}%</h1>
                            <h1 v-else>{{ newcomerInfo.taskProgress }}%</h1>
                            <p>任务</p>
                        </div>
                      </div>
                    </v-col>
                    <!-- 分割线 -->
                    <v-col>
                      <v-divider style="margin-top: 52px"/>
                    </v-col>
                    <!-- 评价 -->
                    <v-col>
                      <div class="circleBox">
                        <el-progress 
                          :show-text="false" 
                          type="circle"
                          :width="100" 
                          :percentage="newcomerInfo.evaluateProgress">
                        </el-progress>
                        <div class="circleCenter">
                            <h1 v-if="newcomerInfo.evaluateProgress < 100 && newcomerInfo.evaluateProgress > 0">&nbsp;{{ newcomerInfo.evaluateProgress }}%</h1>
                            <h1 v-else-if="newcomerInfo.evaluateProgress === 0">&nbsp;&nbsp;&nbsp;{{ newcomerInfo.evaluateProgress }}%</h1>
                            <h1 v-else>{{ newcomerInfo.evaluateProgress }}%</h1>
                            <p>评价</p>
                        </div>
                        <div style="margin-top: 10px">
                          <h3>评价</h3>
                        </div>
                      </div>
                    </v-col>
                    <!-- 分割线 -->
                    <v-col>
                      <v-divider style="margin-top: 52px"/>
                    </v-col>
                    <!-- 毕业证书 -->
                    <!-- <v-col> -->
                      <!-- <div class="circleBox"> -->
                        <!-- <img :src="newcomerInfo.certificate" width="100"> -->
                        <!-- <div style="margin-top: 30px"> -->
                          <!-- <h2 ><strong>{{ newcomerInfo.graduateDate }}</strong></h2> -->
                          <!-- <h4>毕业情况</h4> -->
                          <!-- <p>{{ newcomerInfo.isGraduate }}</p> -->
                        <!-- </div>
                      </div>
                    </v-col> -->

                    <v-col>
                      <div class="circleBox">
                        <div v-if="newcomerInfo.graduateDate === '未毕业'" style="margin-top: 40px">
                          <h2><strong>未毕业</strong></h2>
                        </div>
                        
                        <div v-else style="margin-top: 30px">
                          <h2><strong>已毕业</strong></h2>
                          <strong><p>{{ newcomerInfo.graduateDate.split('T')[0] }} {{ newcomerInfo.graduateDate.split('T')[1] }}</p></strong>
                        </div>
                      </div>
                    </v-col>

                  </v-row>
                </v-card-text>
            </v-card>
        </v-col>
    </v-row>

    <CommitDialog
        :dialogVisible="this.commitDialogVisible"
        :Close="this.closeCommitDialog"
        :send="this.sendCommit"
        :oldCommit="oldCommit"
        :oldScore="oldScore"
    ></CommitDialog>

    <!-- content内容：课程、考试、任务 -->
    <content-display :showAudience="'newcomer'"></content-display>
    
</v-container>
</template>

<script>
import ContentDisplay from './content/ContentDisplay.vue'
import COMM from "@/utils/Comm";
import CommitDialog from "@/components/subcomponents/CommitDialog";

export default ({
    name: "NewcomerBoard",
    inject: ['GLOBAL'],
    components: {
      ContentDisplay,
      CommitDialog
    },
    data() {
        return {
            name: "",
            newcomerInfo: {  // 新人旅程相关数据，从后端获取！
              startDate: '', // TODO: 需要从后端获取新人旅程开始时间的数据
              isGraduate: "",
              tutor: '', // TODO: 需要从后端获取导师的名字
              teacherUsername: "",
              courseProgress: '',  // TODO
              examProgress: '', // TODO
              taskProgress: '',  // TODO
              evaluateProgress: '',  // TODO
              graduateDate: '',  // TODO
              // certificate: 'https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fbkimg.cdn.bcebos.com%2Fpic%2F3801213fb80e7bec5c745b6f252eb9389a506b95&refer=http%3A%2F%2Fbkimg.cdn.bcebos.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1652891023&t=95787fffcddad7af9d8633748f291448', // 证书图片
            },
            identity: 'newcomer', // tutor, HRBP, admin
            shownView: "course",  // 只会是 course, exam, task 三种之一，初始化为course
            // 三个visible变量有且恰有一个为true，通过检测shownView变量变化来修改，初始显示课程(course)
            commitToTeacher: "不错",
            scoreToTeacher: 2,
            courseVisible: true,
            examVisible: false,
            taskVisible: false,
            commitDialogVisible: false,
            oldCommit: "",
            oldScore: 0,
        }
    },
    methods: {
        datetime: function(timestamp) {
            var d = new Date()
            d.setTime(timestamp < 1e10 ? timestamp * 1000 : timestamp)
            return d.toLocaleString()
        },
        newcomer_summary_info(){
          COMM.newcomer_summary_info().then(
              res => {console.log("get newcomer summary info success", res)
                      this.newcomerInfo = res.data;},
              err => {console.log("get newcomer summary info fail ", err)})
        },
        closeCommitDialog(){this.commitDialogVisible = false},

      sendCommit(score,commit){
          COMM.newcomer_commit_teacher(commit).then(
              res => {
                console.log("send commit success", res)
                alert("评论成功!")
              },
              err => {
                console.log("send commit fail ", err)
                alert("评论失败!")
              })
          COMM.newcomer_score_teacher(score).then(
              res => {console.log("send commit success", res)},
              err => {
                console.log("send commit fail ", err)
                alert("打分失败!")
              })
          this.newcomer_summary_info();
      },

        commitTeacher(){
          console.log("commit teacher")
          COMM.get_my_commit(this.GLOBAL.username).then(
              res => {
                this.oldCommit=res.data.commits
                this.oldScore=res.data.score
              },
              err => {console.log("send commit fail ", err)}
          )
          this.commitDialogVisible = true
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
      this.newcomer_summary_info();
      this.GLOBAL.contentDisplayAddif = false
      this.GLOBAL.contentDisplayUser = true
    }
    // TODO
})
</script>

<style>
    .circleBox {
        position: relative;
        text-align: center;
        /* width: 120px; */
        width: 166.7px;
    }
 
    .circleCenter {
        position: absolute;
        /* top: 40px; */
        top: 30px;
        /* left: 28px; */
        /* left: 68px; */
        left: 51px;
    }
</style>
