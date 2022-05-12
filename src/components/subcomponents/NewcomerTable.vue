<template>
<v-container>
<!-- elementUI表单 -->
  <div style="margin: 1.5%">
    <el-table
      ref="filterTable"
      :data="tables"
      style="width: 100%"
    >
      <el-table-column
        v-if="colData[0].istrue && columnShow.name"
        fixed
        key="name"
        property="name"
        label="姓名"
        min-width="120">
        <template slot-scope="scope">
          <el-form :inline="true" :model="formInline" class="demo-form-inline" style="margin-top: 0px; margin-bottom: -30px">
          <el-form-item style="margin-top: 5px">
            <el-avatar :src="scope.row.avatar" size="small" :key="scope.row.avatar"></el-avatar>
          </el-form-item>
          <el-form-item>{{ scope.row.name }}</el-form-item>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column
        v-if="colData[1].istrue && columnShow.joinBootcamp"
        fixed
        key="joinBootcamp"
        label="是否参与Bootcamp"
        show-overflow-tooltip
        min-width="145">
        <template slot-scope="scope">
          <el-switch v-model="scope.row.joinBootcamp" disabled>
          </el-switch>
        </template>
      </el-table-column>
      <el-table-column
          v-if="colData[9].istrue && columnShow.department"
          key="department"
          property="department"
          label="部门"
          min-width="100"
          show-overflow-tooltip>
      </el-table-column>
      <el-table-column
        v-if="colData[2].istrue && columnShow.superior"
        property="superior"
        key="superior"
        label="直属上级"
        show-overflow-tooltip
        width="120">
      </el-table-column>
      <el-table-column
        v-if="colData[3].istrue && columnShow.city"
        property="city"
        key="city"
        label="城市"
        show-overflow-tooltip
        width="120">
      </el-table-column>
      <el-table-column
        v-if="colData[4].istrue && columnShow.employed"
        property="employed"
        key="employed"
        label="入职情况"
        show-overflow-tooltip
        width="120">
        <template slot-scope="scope">
          <el-tag
            :type="scope.row.employed === '待入职' ? 'warning' : 'success'"
            disable-transitions>
            <i v-if="scope.row.employed === '待入职'" class="el-icon-warning-outline"/>
            <i v-else class="el-icon-circle-check"/>
            {{scope.row.employed}}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column
        v-if="colData[5].istrue && columnShow.tutor"
        label="导师分配"
        key="tutor"
        min-width="140">
        
        <template slot-scope="scope">
            {{scope.row.tutor}}
            <el-button v-if="scope.row.tutor === '无'" style="margin-left: 10%" @click="openAssignTutorDialog(scope.row)" type="text">分配</el-button>
        </template>
        
        <!-- 分配导师弹窗 -->
        <v-dialog
          v-model="assignTutorDialog"
          persistent
          max-width="500px"
        >
          <v-card>
              <v-card-title>为新人 {{ selectedNewcomer.name }} 分配导师</v-card-title>
              <v-divider></v-divider>
              <v-card-text style="margin-top: 20px; margin-left: 10px">
                <!-- 选择导师下拉栏 -->
                <el-select v-model="selectedTutor" placeholder="请选择导师">
                  <el-option
                    v-for="tutor in tutors_to_assign"
                    :key="tutor.username"
                    :label="tutor.name"
                    :value="tutor.username">
                  </el-option>
                </el-select>
              </v-card-text>
              <v-card-actions>
              <v-btn
                  color="blue darken-1"
                  text
                  @click="assignTutorDialog = false"
              >
                  取消
              </v-btn>
              <v-btn
                  color="blue darken-1"
                  text
                  @click="assignTutor"
              >
                  分配
              </v-btn>
              </v-card-actions>
          </v-card>
        </v-dialog>
        
      </el-table-column>
      <el-table-column
        v-if="colData[6].istrue && columnShow.graduated"
        label="是否毕业"
        key="graduated"
        width="120">
        <template slot-scope="scope">
          <el-switch v-model="scope.row.graduated" disabled>
          </el-switch>
        </template>
      </el-table-column>
      <el-table-column
        v-if="colData[7].istrue && columnShow.newcomerBoard && !AdminToTutor"
        label="新人看板"
        key="newcomerBoard"
        width="120">
        <template slot-scope="scope">
          <el-button @click="showNewcomerBoard(scope.row)" type="text">查看</el-button>
        </template>
      </el-table-column>
      <el-table-column
        v-if="columnShow.notes"
        label="带新记录"
        key="notes"
        width="120">
        <!-- <template slot-scope="scope">{{ (scope.row.notes == null ? '暂无' : scope.row.notes) }} -->
        <template slot-scope="scope">
          <el-button @click="showNewcomerRecode(scope.row)" type="text">查看</el-button>
        </template>
      </el-table-column>
      <el-table-column
        v-if="colData[8].istrue && columnShow.evaluate"
        label="新人评价"
        key="evaluate"
        width="120">
        <!-- <template slot-scope="scope">{{ (scope.row.evaluate == null ? '暂无' : scope.row.evaluate) }}
          <el-button @click="showNewcomerCommit(scope.row)" type="text">查看</el-button>
        </template> -->
        <template slot-scope="scope">
          <span v-if="scope.row.tutor === '无'">暂无</span>
          <el-button v-else @click="showNewcomerCommit(scope.row)" type="text">查看</el-button>
        </template>
      </el-table-column> 
    </el-table>
  </div>
  <CommitDialog
      :dialogVisible="this.commitDialogVisible"
      :Close="this.closeCommitDialog"
      :send="this.commit"
      :oldCommit="oldCommit"
      :oldScore="oldScore"
  ></CommitDialog>
  <CommitAndScoreDialog
      :Close="this.closeCommitsAndScoreDialog"
      :dialogVisible="this.commitsAndScoreDialogVisible"
      :commitAndScoreData="this.commitsAndScore"
  ></CommitAndScoreDialog>
  <RecodeDialog
      :Close="this.closeRecodeDialog"
      :dialogVisible="this.recodeDialogVisible"
      :send="this.write_recode"
      :tableData="this.recodes"
  ></RecodeDialog>
</v-container>
</template>

<script>
// 表格的组件封装
import COMM from "@/utils/Comm";
import CommitDialog from "@/components/subcomponents/CommitDialog";
import CommitAndScoreDialog from "@/components/subcomponents/commitAndScoreDialog";
import RecodeDialog from "@/components/subcomponents/RecodeDialog";

export default ({
    name: 'NewcomerTable',
    inject: ['GLOBAL'],
    components: {
      CommitDialog,
      CommitAndScoreDialog,
      RecodeDialog
    },
    data() {
        return {
          commitsAndScore: {}, // admin查看相互评价时的存储变量
          recodes:[], //新人的带新记录,传给recodeDialog
          commitsAndScoreDialogVisible: false,
          commitDialogVisible: false,
          oldCommit: "",
          oldScore: 0,
          recodeDialogVisible: false,
          selectedNewcomer: {},  // 点击该新人的分配按钮
          selectedTutor: '', // 下拉框选中的导师
          assignTutorDialog: false, // 分配导师弹窗是否显示
          tutors_to_assign: [ // TODO: 从后端拿来的某新人可选的待分配导师列表
            {
              bio: '',
              city: '',
              department: '',
              dept: '',
              detail: '',
              employed: '',
              employeeType: '',
              isAdmin: '',
              isHRBP: '',
              isNew: '',
              isTeacher: '',
              joinDate: '',
              joinStatus: '',
              leader: '',
              name: 'TutorName',
              registrationDate: '',
              selectedPosition: '',
              superior: '',
              userPositions: '',
              username: 'username',
            },
          ]
        }
    },
    props: {
        AdminToTutor: {type: Boolean, default: false}, // 关掉管理员->导师->新人看板通路
        tutorIdentity: {}, // 这里用来表示是那个老师的新人看板
        formInline: {}, // 输入框（筛选）内容
        tables: [], // table的列项
        colData: [], // 为了显示部分列表项（不同的父组件需要不同的列）
        columnShow: {},  // 因为不同的tab所需要显示的列项内容不同，因此要在表格处做一些筛选，父组件传过来是否显示某些列这一columnShow参数
        checkNewcomerBoard: { // 回调函数，NewcomerTable -> NewcomerManage/LeadNewcomerSub
          type: Function, default: () => {return () => {}}
        },
        reGetData:{  // 重新获取数据，用于刷新
          type: Function, default: () => {return () => {}}
        }
    },
    methods: {
      showNewcomerBoard(data) {
        console.log('showNewcomerBoard:', data)
        this.checkNewcomerBoard(data)
      },
      showNewcomerRecode(data){
        console.log(data)
        this.selectedNewcomer = data
        COMM.get_newcomer_recode(this.selectedNewcomer.username).then(res => {
          console.log("get recode success: ", res.data)
          this.recodes = res.data;
        }, err => {
          console.log("get recode error: ", err)
          this.recodes = [{
            commitTime: '2022-05-03',
            content: "今天新人表现的很不错"
          },]
        })
        this.recodeDialogVisible = true
      },
      showNewcomerCommit(data){
        this.selectedNewcomer = data
        if (this.GLOBAL.ident === "teacher"){  // 导师的视角下, 是可评论的弹窗
          COMM.get_my_commit(this.selectedNewcomer.username).then(
              res => {
                this.oldCommit=res.data.commits
                this.oldScore=res.data.score
              },
              err => {console.log("send commit fail ", err)}
          )
          this.commitDialogVisible = true
        }else if(this.GLOBAL.ident === "admin"){  // 管理员视角下，是只读的弹窗
          COMM.get_commits_and_score(this.selectedNewcomer.username).then(
              res => {
                console.log("get commit success", res)
                this.commitsAndScoreDialogVisible = true
                this.commitsAndScore = res.data
              },
              err => {
                console.log("get commit fail", err)
                this.commitsAndScore = {
                  teacherScore: "无",
                  newcomerScore: "无",
                  newcomerToTeacher: "无",
                  teacherToNewcomer: "无"
                }
              }
          )
        }
      },

      commit(score, commits){
        console.log(score,commits)
        COMM.teacher_commit_newcomer(commits,this.selectedNewcomer.username).then(
            res => {
              console.log("send commit success", res)
              alert("评论成功!")
            },
            err => {
              console.log("send commit fail", err)
              alert("评论失败!")
            }
        )
        COMM.teacher_score_newcomer(score, this.selectedNewcomer.username).then(
            res => {console.log("send score success", res)},
            err => {
              console.log("send score fail", err)
              alert("打分失败!")
            }
        )
      },
      write_recode(content){
        console.log(content)
        COMM.newcomer_recode(content,this.selectedNewcomer.username).then(
            res => {console.log("send recode success", res)},
            err => {console.log("send recode fail", err)}
        )
      },
      closeCommitsAndScoreDialog(){this.commitsAndScoreDialogVisible = false},
      closeCommitDialog(){this.commitDialogVisible = false},
      closeRecodeDialog(){this.recodeDialogVisible = false},
      openAssignTutorDialog(newcomer){
        this.assignTutorDialog = true;
        console.log('openAssignTutorDialog', newcomer)
        COMM.get_duty_teacher_list().then(res => {
          console.log("get admin duty_teacher_list success: ", res)
          this.tutors_to_assign = res.data;
        }, err => {console.log("get admin duty_teacher_list error: ", err)})
        this.selectedNewcomer = newcomer;
      },
      assignTutor(){
        console.log('assignTutor', this.selectedNewcomer.username, this.selectedTutor)
        COMM.assign_teacher(this.selectedNewcomer.username, this.selectedTutor).then(res => {
          console.log("success assigned ", res)
          this.reGetData()
          this.$forceUpdate()
        }, err => {
          console.log("assigen failed maybe muti assign",err)
          alert("assign failed,maybe muti assign")
        })
        this.assignTutorDialog = false;
      },
      resetTutor(){
        this.assignTutorDialog = false;
      }
    },
    mounted() {
        console.log('test newcomertable');
        console.log(this.tables)
        this.assignTutorDialog = false;
    }
})
</script>
