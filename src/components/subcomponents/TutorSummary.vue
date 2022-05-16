<template>
  <!-- 导师旅程 -->
  <v-row style="margin: 0.5%">
    <v-col>
      <v-card>
        <v-card-subtitle>{{tutor}}的导师旅程开始于 <strong>{{ tutorInfo.startDate.split('T')[0] }} {{tutorInfo.startDate.split('T')[1]}}</strong></v-card-subtitle>
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

</template>

<script>
export default {
  name: "TutorSummary",
  props: {
    tutorInfo:{},
    tutor: {}
  },
}
</script>

<style scoped>

</style>