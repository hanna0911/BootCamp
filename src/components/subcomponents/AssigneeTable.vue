<template>
<v-container>
<!-- elementUI表单 -->
  <div style="margin: 1.5%">
    <!-- BUG WITH BUTTON TODO -->
    <el-table
      :row-key="getRowKey"
      ref="filterTable"
      :data="tables.slice((currentPage - 1) * pageSize, currentPage * pageSize)"
      style="width: 100%"
      @selection-change="handleSelectionChange"
    >
      <el-table-column
        type="selection"
        :reserve-selection="true"
        width="55">
      </el-table-column>
      <!-- <el-table-column
          fixed
          label="是否发送"
          min-width="100">
        <template slot-scope="scope">
          <el-checkbox
            v-model="chosen[scope.$index]">
          </el-checkbox>
        </template>
      </el-table-column> -->
      <el-table-column
        v-if="colData[0].istrue && columnShow.name"
        fixed
        key="name"
        property="name"
        label="姓名"
        min-width="150">
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
          v-if="colData[10].istrue && columnShow.department"
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
      <!-- <el-table-column
        v-if="colData[5].istrue && columnShow.tutor"
        label="导师分配"
        key="tutor"
        min-width="140">
        
        <template slot-scope="scope">
            {{scope.row.tutor}}
            <el-button style="margin-left: 10%" @click="openAssignTutorDialog(scope.row)" type="text">分配</el-button>
        </template> -->
        
        <!-- 分配导师弹窗 -->
        <!-- <v-dialog
          v-model="assignTutorDialog"
          persistent
          max-width="500px"
        >
          <v-card>
              <v-card-title>为新人 {{ selectedNewcomer.name }} 分配导师</v-card-title>
              <v-divider></v-divider>
              <v-card-text style="margin-top: 20px; margin-left: 10px"> -->
                <!-- 选择导师下拉栏 -->
                <!-- <el-select v-model="selectedTutor" placeholder="请选择导师">
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
        
      </el-table-column> -->
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
      <!-- <el-table-column
        v-if="colData[7].istrue && columnShow.newcomerBoard"
        label="新人看板"
        key="newcomerBoard"
        width="120">
        <template slot-scope="scope">
          <el-button @click="showNewcomerBoard(scope.row)" type="text">查看</el-button>
        </template>
      </el-table-column>
      <el-table-column
        v-if="colData[8].istrue && columnShow.notes"
        label="带新记录"
        key="notes"
        width="120">
        <template slot-scope="scope">{{ (scope.row.notes == null ? '暂无' : scope.row.notes) }}
          <el-button @click="showNewcomerRecode(scope.row)" type="text">查看</el-button>
        </template>
      </el-table-column>
      <el-table-column
        v-if="colData[9].istrue && columnShow.evaluate"
        label="新人评价"
        key="evaluate"
        width="120">
        <template slot-scope="scope">{{ (scope.row.evaluate == null ? '暂无' : scope.row.evaluate) }}
          <el-button @click="showNewcomerCommit(scope.row)" type="text">查看</el-button>
        </template>
      </el-table-column>  -->
    </el-table>
    
    <!-- 分页器 -->
    <div class="block" style="margin: 20px">
      <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" background
        :current-page="currentPage" :page-sizes="[5, 10, 20, 40]" :page-size="pageSize"
        layout="->, total, sizes, prev, pager, next, jumper" :total="tables.length"></el-pagination>
    </div>

  </div>
  <!-- <CommitDialog
      :dialogVisible="this.commitDialogVisible"
      :Close="this.closeCommitDialog"
      :send="this.commit"
  ></CommitDialog> -->
  <v-row>
    <v-btn @click="uploadNotification" width="100px" style="margin-top: 30px">
      发送
    </v-btn>
  </v-row>
</v-container>
</template>

<script>
// 表格的组件封装
import COMM from "@/utils/Comm";
// import CommitDialog from "@/components/subcomponents/CommitDialog";

export default ({
    name: 'AssigneeTable',
    inject: ['GLOBAL'],
    components: {
    //   CommitDialog
    },
    data() {
        return {
          // 翻页
          currentPage: 1, // 默认第1页
          pageSize: 5, // 默认显示5条
          totalSize: 0, // 默认总条数为0 这个无所谓，前端分页可以计算数组的length

          multipleSelection: [], // 多选获得的数据
          commitDialogVisible: false,
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
          ],
        }
    },
    props: {
        notification: {},
        formInline: {}, // 输入框（筛选）内容
        tables: [], // table的列项
        colData: [], // 为了显示部分列表项（不同的父组件需要不同的列）
        columnShow: {},  // 因为不同的tab所需要显示的列项内容不同，因此要在表格处做一些筛选，父组件传过来是否显示某些列这一columnShow参数
        checkNewcomerBoard: { // 回调函数，NewcomerTable -> NewcomerManage/LeadNewcomerSub
          type: Function,
          default: () => {return () => {}}
        },
        reGetData:{  // 重新获取数据，用于刷新
          type: Function,
          default: () => {return () => {}}
        },
        resetNotification: {
          type: Function,
          default: () => {return () => {}}
        }
    },
    methods: {
      // 翻页功能
      // 保存选中的数据id,row-key就是要指定一个key标识这一行的数据
      getRowKey(row) { 
        // console.log("看看每一行的数据", row);
        // return row.id;
        return row.username;
      },
      // 每页显示条数
      handleSizeChange(pageSize) {
        this.pageSize = pageSize
        console.log(this.pageSize) // 每页下拉显示数据
      },
      // 当前页
      handleCurrentChange(currentPage) {
        this.currentPage = currentPage
        console.log(this.currentPage)
      },

      // 多选选中的内容在这里进行实时更新
      handleSelectionChange(val) {
        this.multipleSelection = val; // 存储在multipleSelection变量中
      },
      showNewcomerBoard(data) {
        console.log('showNewcomerBoard:', data)
        this.checkNewcomerBoard(data)
      },
      showNewcomerRecode(data){
        console.log(data)
        if (this.GLOBAL.ident === "teacher"){
          alert("need to show teacher edit")
          this.selectedNewcomer = data
        }else if(this.GLOBAL.ident === "admin"){
          alert("need to show admin view")
        }
      },
      showNewcomerCommit(data){
        console.log(data)
        if (this.GLOBAL.ident === "teacher"){
          this.commitDialogVisible = true
          this.selectedNewcomer = data

        }else if(this.GLOBAL.ident === "admin"){
          alert("need to show admin view")
        }
      },

      commit(score, commits){
        console.log(score,commits)
        COMM.teacher_commit_newcomer(commits,this.selectedNewcomer.username).then(
            res => {console.log("send commit success", res)},
            err => {console.log("send commit fail", err)}
        )
        COMM.teacher_score_newcomer(score, this.selectedNewcomer.username).then(
            res => {console.log("send commit success", res)},
            err => {console.log("send commit fail", err)}
        )
      },

      closeCommitDialog(){this.commitDialogVisible = false},

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
      },
      async uploadNotification() {
        console.log(this.notification.title, this.notification.content)
        if (this.notification.title === '' || this.notification.content === '') {
          alert('标题和内容不能为空！')
          return
        }
        if (this.multipleSelection.length == 0) {
          alert('请选择用户！')
          return
        }
        var usernames = []
        this.multipleSelection.forEach(item => {
          usernames.push(item.username)
        });
        var apiData = {
          'action': 'create notification',
          'title': this.notification.title,
          'content': this.notification.content,
          'assignees': usernames
        }
        var res = await COMM.create_notification(apiData)
        if (res.result == 'success') {
          alert('发送成功')
        }
        else {
          alert('发送失败，请检查网络并稍后重试')
        }
        this.resetForm()
      },  
      resetForm() {
        this.resetNotification()
        this.reGetData()
      }
    },
    mounted() {
        console.log('test assigneetable');
        console.log(this.tables)
        this.assignTutorDialog = false;
    },
})
</script>
