<template>
    <!-- 新人旅程 -->
    <v-row style="margin: 0.5%">
      <v-col>
        <v-card>
          <v-card-subtitle>
            <v-row>
              <v-col>
                {{newcomer}}的新人旅程开始于 <strong>{{ newcomerInfo.startDate.split('T')[0] }} {{ newcomerInfo.startDate.split('T')[1] }}</strong>，
                <p v-if="newcomerInfo.tutor !== '无'">{{newcomer}}的导师是 <strong>{{ newcomerInfo.tutor }}</strong></p>
                <p v-else>{{newcomer}}暂无导师</p>
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
</template>

<script>
export default {
  name: "NewcomerSummary",
  props: {
    newcomerInfo:{},
    newcomer: {}
  },

}
</script>

<style scoped>

</style>