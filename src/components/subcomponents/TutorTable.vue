<template>
  <v-container>
    <!-- <div v-if='!showLearningBoard'> -->
    <div>
      <!-- 完整版表单（上岗导师列表） -->
      <!-- 
        第二步：指定一个key去确认标识这一行的数据，因为若要翻页保留，就需要确认保留的数据是哪一个，
              所以我们就给每一行确定个独一无二的身份标识，这里我们在el-table标签上
              使用row-key去得到每一行的身份标识
      -->
      <el-table
          :row-key="getRowKey"
          ref="multipleTable"
          :data="tables.slice((currentPage - 1) * pageSize, currentPage * pageSize)"
          style="width: 100%"
          @selection-change="handleSelectionChange"
      >
        <!-- 
          第一步：开启选中翻页保留模式 即：:reserve-selection="true" 
                默认是false。即 默认选中翻页不保留之前勾选的数据
        -->
        <el-table-column
            type="selection"
            width="55"
            :reserve-selection="true"
            >
        </el-table-column>
        <el-table-column
            v-if="colData[0].istrue && columnShow.name"
            key="name"
            property="name"
            label="姓名"
            fixed
            min-width="120">
          <template slot-scope="scope">
            <el-form :inline="true" :model="formInline" class="demo-form-inline"
                    style="margin-top: 0px; margin-bottom: -30px">
              <el-form-item style="margin-top: 5px">
                <el-avatar :src="scope.row.avatar" :key="scope.row.avatar" size="small"></el-avatar>
              </el-form-item>
              <el-form-item>{{ scope.row.name }}</el-form-item>
            </el-form>
          </template>
        </el-table-column>

        <!-- TODO -->
        <el-table-column
            v-if="columnShow.currentMembers"
            key="currentMembers"
            property="currentMembers"
            label="当前带新"
            show-overflow-tooltip>
        </el-table-column>

        <!-- TODO -->
        <el-table-column
            v-if="columnShow.historicalMembers"
            key="historicalMembers"
            property="historicalMembers"
            label="累计带新"
            show-overflow-tooltip>
        </el-table-column>

        <el-table-column
            v-if="colData[1].istrue && columnShow.department"
            key="department"
            property="department"
            label="部门"
            min-width="100"
            show-overflow-tooltip>
        </el-table-column>
        <el-table-column
            v-if="colData[2].istrue && columnShow.superior"
            key="superior"
            property="superior"
            label="直属上级"
            min-width="120"
            show-overflow-tooltip>
        </el-table-column>
        <el-table-column
            v-if="colData[3].istrue && columnShow.city"
            key="city"
            property="city"
            label="城市"
            min-width="80"
            show-overflow-tooltip>
        </el-table-column>
        <el-table-column
            v-if="colData[4].istrue && columnShow.joinDate"
            key="joinDate"
            label="入职时间"
            min-width="120"
            show-overflow-tooltip>
          <template slot-scope="scope">{{ (scope.row.joinDate === null) ? '' : scope.row.joinDate.split('T')[0] }}</template>
        </el-table-column>

        <!-- TODO -->
        <el-table-column
            v-if="columnShow.nominateDate"
            key="teacherNominationDate"
            property="teacherNominationDate"
            label="提名时间"
            min-width="120"
            show-overflow-tooltip
        >
          <template slot-scope="scope">{{ (scope.row.teacherNominationDate === null) ? '' : scope.row.teacherNominationDate.split('T')[0] }}</template>
        </el-table-column>

        <el-table-column
            v-if="columnShow.checkStatus"
            key="teacherExaminedStatus"
            property="teacherExaminedStatus"
            label="审核状态"
            min-width="120"
            show-overflow-tooltip
        >
          <template slot-scope="scope">
            <!-- 后端需要提供审核状态的数据 -->
            <!-- <el-tag
                :type="scope.row.checkStatus === '通过' ? 'warning' : 'success'"
                disable-transitions>
                <i v-if="scope.row.checkStatus === '通过'" class="el-icon-warning-outline"/>
                <i v-else class="el-icon-circle-check"/>
                {{scope.row.checkStatus}}
            </el-tag> -->
            <el-tag type="success" v-if="scope.row.teacherExaminedStatus === '通过'" >
              <i class="el-icon-circle-check"/>
              {{ scope.row.teacherExaminedStatus }}
            </el-tag>
            <el-tag type="warning" v-else>
              <i class="el-icon-circle-check"/>
              {{ scope.row.teacherExaminedStatus }}
            </el-tag>
          </template>
        </el-table-column>

        <!-- 导师培训状态（学习状态） -->
        <el-table-column
            v-if="columnShow.trainStatus"
            key="nominateDate"
            property="nominateDate"
            label="导师培训状态"
            width="180"
            show-overflow-tooltip
        >
          <template slot-scope="scope">
            <!-- 后端需要提供导师培训状态的数据 -->
            <!-- <el-tag
                :type="scope.row.trainStatus === '拒绝' ? 'warning' : 'success'"
                disable-transitions>
                <i v-if="scope.row.trainStatus === '拒绝'" class="el-icon-warning-outline"/>
                <i v-else class="el-icon-circle-check"/>
                {{scope.row.trainStatus}}
            </el-tag> -->
            <el-tag>
              <i class="el-icon-warning-outline"/>
              学习中
            </el-tag>
            <el-button style="margin-left: 10%" @click="openLearningBoard(scope.row.name, scope.row.username)" type="text">查看</el-button>
          </template>
        </el-table-column>

      <el-table-column
          v-if="columnShow.teacherDutyDate"
          key="teacherDutyDate"
          property="teacherDutyDate"
          label="上岗时间"
          width="120"
          show-overflow-tooltip>
        <template slot-scope="scope">{{ scope.row.teacherDutyDate.split('T')[0] }}</template>
      </el-table-column>
      
      <el-table-column
          v-if="columnShow.newcomerBoard"
          key="newcomerBoard"
          property="newcomerBoard"
          label="带新看板"
          show-overflow-tooltip>
        <template slot-scope="scope">
          <el-button style="margin-left: 10%" @click="showNewcomerTable(scope.row)" type="text">查看</el-button>
        </template>
      </el-table-column>
      <el-table-column
          v-if="columnShow.teacherScore"
          key="teacherScore"
          property="teacherScore"
          label="综合得分"
          min-width="100px"
          show-overflow-tooltip>
        <template slot-scope="scope">
          {{ scope.row.teacherScore.toFixed(2) }}
          <!-- &nbsp;&nbsp;&nbsp;| -->
          <!-- <el-button style="margin-left: 10%" @click="handleClick(scope.row)" type="text">查看</el-button> -->
        </template>
      </el-table-column>
      <!-- <el-table-column
          v-if="columnShow.OKR"
          key="OKR"
          property="OKR"
          label="OKR"
          show-overflow-tooltip>
        <template slot-scope="scope">
          <el-button style="margin-left: 10%" @click="handleClick(scope.row)" type="text">查看</el-button>
        </template>
      </el-table-column> -->

        <!-- 操作 -->
        <el-table-column
            v-if="columnShow.operation"
            key="operation"
            property="operation"
            label="操作"
            min-width="150"
            show-overflow-tooltip>
          <template slot-scope="scope">
            <el-button @click="accept(scope.row)" type="success" plain size="mini">通过</el-button>
            <el-button @click="reject(scope.row)" type="danger" plain size="mini">拒绝</el-button>
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页器 -->
      <div class="block" style="margin: 20px">
        <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" background
          :current-page="currentPage" :page-sizes="[5, 10, 20, 40]" :page-size="pageSize"
          layout="->, total, sizes, prev, pager, next, jumper" :total="tables.length"></el-pagination>
      </div>
    </div>
    <!-- <NewcomerBoardEdit v-else :closeNewcomerBoard='closeLearningBoard' :newcomerIdentity="infos" :showAudience="'teacher'"/> -->
  </v-container>
</template>

<script>
// 表格的组件封装
import COMM from "@/utils/Comm";
// import NewcomerBoardEdit from './NewcomerBoardEdit.vue'
// import NewcomerTable from './NewcomerTable.vue'

export default ({
  name: 'TutorTable',
  components: {
    // NewcomerTable,
    // NewcomerBoardEdit,
  },
  data() {
    return {
      // 翻页
      currentPage: 1, // 默认第1页
      pageSize: 5, // 默认显示5条
      totalSize: 0, // 默认总条数为0 这个无所谓，前端分页可以计算数组的length


      // showNewcomerTable: false,
      selected_teacher:[],
      // 发送给NewcomerTable的数据
      formInline_newcomer: { // 输入框（筛选）内容
        name: '',
        joinBootcamp: '',
        superior: '',
        city: '',
        employed: '', 
        tutor: '',
        graduated: '',
      },
      colData_newcomer: [  // table的列项
        {title: "姓名",istrue: true},
        {title: "是否参与Bootcamp",istrue: true},
        {title: "直属上级",istrue: true},
        {title: "城市",istrue: true},
        {title: "入职情况",istrue: true},
        {title: "导师分配",istrue: true},
        {title: "是否毕业",istrue: true},
        {title: "新人看板",istrue: true},
        {title: "带新记录",istrue: true},
        {title: "新人评价",istrue: true},
      ],
      colOptions_newcomer: [],
      colSelect_newcomer: [],
      tableData_newcomer: [], // TODO: 后台拿来的数据
      columnShow_newcomer: { // columnShow: 只显示部分列
        // 新人管理
        name: true,
        joinBootcamp: true,
        superior: true,
        city: true, 
        employed: true, 
        tutor: true,
        graduated: true,
        newcomerBoard: true, 
        notes: true, 
        evaluate: true, 
        // 带新看板
        newcomerType: false, 
        checklist: false,
      },

      // showLearningBoard: false,
      // infos: {},
    }
  },
  props: {
    formInline: { // 输入框（筛选）内容
      // name: '',
      // joinBootcamp: '',
      // superior: '',
      // city: '',
      // employed: '',
      // tutor: '',
      // graduated: '',
    },
    tables: [],
    // table的列项
    refreshNominatedList: {
      type:Function,
      default: ()=>{return ()=>{}}
    },
    colData: [
      // {title: "姓名", istrue: true},
      // {title: "是否参与Bootcamp", istrue: true},
      // {title: "直属上级", istrue: true},
      // {title: "城市", istrue: true},
      // {title: "入职情况", istrue: true},
      // {title: "导师分配", istrue: true},
      // {title: "是否毕业", istrue: true},
      // {title: "新人看板", istrue: true},
      // {title: "带新记录", istrue: true},
      // {title: "新人评价", istrue: true},
    ],
    columnShow: {  // 因为不同的tab所需要显示的列项内容不同，因此要在表格处做一些筛选，父组件传过来是否显示某些列这一columnShow参数
      // name: true,
      // currentMembers: false,
      // historicalMembers: false,
      // department: true,
      // superior: true,
      // city: true,
      // joinDate: true,
      // teacherDutyDate: false,
      // newcomerBoard: false,
      // teacherScore: false,
      // OKR: false,
    },
    // 回调函数，TutorTable -> TutorManage
    checkNewcomerTable: {
      type: Function,
      default: () => {
        return () => {}
      }
    },
    // 同上
    checkLearningBoard: {
      type: Function,
      default: () => {
        return () => {}
      }
    },

  },
  mounted() {
    console.log('test tutortable');
    console.log(this.tables)
  },
  watch: {
    selectedTutor: {
      handler(newVal, oldVal) {
        console.log('oldVal:', oldVal)
        console.log('newVal:', newVal)
      },
    }
  },
  methods: {
    // 翻页并保留多选
    // 保存选中的数据id,row-key就是要指定一个key标识这一行的数据
    getRowKey(row) { 
    /*
      第三步，一般我们都是用id作为每一行数据的特殊标识，所以这里返回的是row下面的id作为标识。当然
             这里不return row下面的id也行，只要能够确保某个字段是独一无二的，不会重复的，就可return
             return row下面的这个字段也是可以的
    */
      console.log("看看每一行的数据", row);
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


    accept(data) {
      COMM.accept_nominate(data.username).then(res=>{
        console.log("reject success ", res);
        this.refreshNominatedList();
        alert("通过成功!")
      },err=>{console.log("reject fail", err)})
    },
    handleSelectionChange(val) {
      this.selected_teacher = val;
      console.log(this.selected_teacher)
    },
    reject(data) {
      COMM.reject_nominate(data.username).then(res=>{
        console.log("reject success ", res);
        this.refreshNominatedList();
        alert("拒绝成功!")
      },err=>{console.log("reject fail", err)})
    },
    nominateSelectedTeacher(){
      COMM.nominate_teachers(this.selected_teacher).then(res=>{
        console.log("reject success ", res);
      },err=>{console.log("reject fail", err)})
    },
    showNewcomerTable(data){
      this.checkNewcomerTable(data) // props函数
    },
    // closeLearningBoard() { 
    //   // 提供给子组件NewcomerBoardEdit的回调函数
    //   this.showLearningBoard = false;
    // },
    openLearningBoard(name, username) {
      // console.log("learning board info:", name, username)
      // this.infos = {
      var infos = {
      "username": username,
        "name": name,
      }
      // this.showLearningBoard = true
      this.checkLearningBoard(infos) // props函数
    },
  }
})
</script>
