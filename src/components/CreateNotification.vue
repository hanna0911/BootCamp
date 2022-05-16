<template>
<v-container>
  <div v-if="!newcomerBoardVisible">
  <h2 class="px-4 pt-4 pb-3 font-weight-black">发布公告</h2>
  <h3 class="px-4 pt-4 pb-3 font-weight-black">公告内容</h3>
  <v-spacer></v-spacer>
  <el-form :model="toAddNotification" label-width="100px" style="margin-left: 30px">
    <el-form-item label="公告标题："  required>
        <el-input v-model="toAddNotification.title"></el-input>
    </el-form-item>
    <el-form-item label="公告内容：" required>
        <el-input v-model="toAddNotification.content" type="textarea" :rows="8"></el-input>
    </el-form-item>
  </el-form>
  <h3 class="px-4 pt-4 pb-3 font-weight-black">发送对象</h3>
  <v-row>
    <h4 class="px-4 pt-4 pb-3 font-weight-black" style="margin-left: 12px">发送对象选择范围</h4>
    <el-select v-model="assign_option"  placeholder="请选择" style="margin-top: 10px;">
      <el-option 
        v-for="(item, index) in assign_options" 
        :label="item.label" 
        :value="item.value" 
        :key="index"
      >
      </el-option>
    </el-select>
  </v-row>
  <!-- elementUI输入框 -->
  <!-- 输入框一行一个el-form -->
  <v-card style="margin-top: 30px" v-if="assign_option==='list'">
    <v-card-title>
      用户列表
    </v-card-title>
    <v-card-text style="wrap-content">
      <el-form :inline="true" :model="formInline" class="demo-form-inline" style="margin-left: 30px; margin-top: 30px" v-if="assign_option=='list'">
          <el-form-item label="新人姓名:" style="margin-left: 1.5%; margin-right: 1%" size="medium">
              <el-input v-model="formInline.name" placeholder="请输入" style="width:150px"></el-input>
          </el-form-item>
          <!-- <el-form-item label="是否参与Bootcamp:" style="margin-left: 1.5%; margin-right: 1%" size="medium">
              <el-select v-model="formInline.joinBootcamp" placeholder="请选择" style="width:120px">
                <el-option label="全部" value="全部"></el-option>
                <el-option label="是" value="是"></el-option>
                <el-option label="否" value="否"></el-option>
              </el-select>
          </el-form-item> -->
          <el-form-item label="用户身份:" style="margin-left: 1.5%; margin-right: 1%" size="medium">
              <el-select v-model="formInline.role" placeholder="请选择" style="width:150px">
              <el-option label="全部" value="全部"></el-option>
              <el-option label="新人" value="新人"></el-option>
              <el-option label="导师" value="导师"></el-option>
              <el-option label="HRBP" value="HRBP"></el-option>
              <el-option label="管理员" value="管理员"></el-option>
              </el-select>
          </el-form-item>
          <el-form-item label="城市:" style="margin-left: 1.5%; margin-right: 1%" size="medium">
              <el-select v-model="formInline.city" placeholder="请选择" style="width:150px">
                <el-option label="全部" value="全部"></el-option>
                <el-option label="北京" value="北京"></el-option>
                <el-option label="上海" value="上海"></el-option>
                <el-option label="深圳" value="深圳"></el-option>
              </el-select>
          </el-form-item>
      </el-form>
      <el-form :inline="true" :model="formInline" class="demo-form-inline" style="margin-left: 30px" v-if="assign_option=='list'"> 
          <el-form-item label="是否毕业:" style="margin-left: 1.5%; margin-right: 1%" size="medium">
              <el-select v-model="formInline.graduated" placeholder="请选择" style="width:150px">
              <el-option label="全部" value="全部"></el-option>
              <el-option label="已毕业" value="已毕业"></el-option>
              <el-option label="未毕业" value="未毕业"></el-option>
              </el-select>
          </el-form-item>
          <el-form-item label="入职情况:" style="margin-left: 1.5%; margin-right: 1%" size="medium">
              <el-select v-model="formInline.employed" placeholder="请选择" style="width:150px">
              <el-option label="全部" value="全部"></el-option>
              <el-option label="在职" value="在职"></el-option>
              <el-option label="待入职" value="待入职"></el-option>
              </el-select>
          </el-form-item>
          <div style="margin-top:-57px; margin-bottom: 3%; margin-left: 1.5%; margin-right: 1.5%" align="right">
            <el-button size="small" @click="resetFilter">重置</el-button>
            <!-- 选择特定列呈现 -->
            <el-popover placement="right" width="400" trigger="click">
              <el-checkbox-group v-model="colOptions">
                  <el-checkbox v-for="item in colSelect" :label="item" :key="item" ></el-checkbox>
              </el-checkbox-group>
              <el-button size="small" icon="el-icon-more" slot="reference" style="margin-left: 1%"></el-button>
            </el-popover>
          </div>
      </el-form>

      <!-- elementUI表单 -->
      <assignee-table 
        style="margin-left: 30px"
        v-if="assign_option === 'list'"
        :tables="tables" 
        :colData="colData" 
        :formInline="formInline" 
        :checkNewcomerBoard="checkNewcomerBoard"
        :columnShow="columnShow"
        :reGetData="getDataFromBackend"
        :notification="toAddNotification"
        :resetNotification="resetNotification"
        >
      </assignee-table>
    </v-card-text>
  </v-card>

  </div>
  <!--<newcomer-board-edit v-else :closeNewcomerBoard="closeNewcomerBoard" :newcomerIdentity="newcomerIdentity"></newcomer-board-edit>-->
  <div v-if="assign_option=='group'&&groupList.length==0" style="margin-left: 1%">
    暂无群组信息
  </div>
  <v-list two-line v-if="assign_option=='group'">
    <template v-for="(groupItem, index) in groupList">
      <v-list-item
        :key="groupItem.groupName"
      >
        <v-list-item-action>
        <v-checkbox v-model="chosenGroup[index]">
        </v-checkbox>
        </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title v-html="groupItem.groupName"></v-list-item-title>
          <v-list-item-subtitle v-html="renderMemberCount(index)"></v-list-item-subtitle>
        </v-list-item-content>
        <v-list-item-action>
          <v-row>
            <v-btn @click="editGroup(index)">
              成员详情
            </v-btn>
            <v-btn @click="deleteGroup(index)" style="margin-left: 20px">
              删除群组
            </v-btn>
          </v-row>
        </v-list-item-action>
      </v-list-item>
    </template>
  </v-list>
  <div>
    <v-btn @click="createGroup()" style="margin-left: 40%" v-if="assign_option=='group'">
      创建新群组
    </v-btn>
  </div>
  <v-btn @click="handleSendGroupMessage" v-if="assign_option=='group'" min-width="100px">
    发送
  </v-btn>
  <v-dialog
    v-model="editGroupDialog"
    v-if="assign_option=='group'&&groupList.length>0"
  >
    <v-card>
      <v-card-text>
        <h3 class="px-4 pt-4 pb-3 font-weight-black">群组成员</h3>
        <v-list two-line v-if="assign_option=='group'">
          <template v-for="(userItem) in groupList[selectedIndex].members">
            <v-list-item
              :key="userItem.username"
            >
              <v-list-item-content>
                <v-list-item-title v-html="userItem.name"></v-list-item-title>
                <v-list-item-subtitle v-html="userItem.username + ' ' + userItem.dept"></v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <v-btn @click="deleteMember(userItem.username, selectedIndex)" min-width="100">
                  删除成员
                </v-btn>
              </v-list-item-action>
            </v-list-item>
          </template>
        </v-list>
      </v-card-text>
      <v-card-actions style="margin-left: 40%">
        <v-btn @click="addMember(groupList[selectedIndex])">
          添加成员
        </v-btn>
        <v-btn @click="editGroupDialog=false">
          取消
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
  <v-dialog
    v-model="createGroupDialog"
    v-if="assign_option=='group'"
  >
    <v-card>
      <v-card-title>创建群组</v-card-title>
      <v-divider></v-divider>
      <v-card-text style="wrap-content">
        <el-form :model="toAddGroup" ref="toAddTest" label-width="100px">
          <el-form-item label="群组名称："  style="margin-top: 20px" required>
              <el-input v-model="toAddGroup.name"></el-input>
          </el-form-item>
        </el-form>
        <h3 class="px-4 pt-4 pb-3 font-weight-black">群组成员</h3>
        <v-list two-line v-if="assign_option=='group'">
          <template v-for="(userItem, index) in tableData">
            <v-list-item
              :key="userItem.username"
            >
              <v-list-item-action>
                <v-checkbox v-model="chosenUser[index]">
                </v-checkbox>
              </v-list-item-action>
              <v-list-item-content>
                <v-list-item-title v-html="userItem.name"></v-list-item-title>
                <v-list-item-subtitle v-html="userItem.username"></v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </template>
        </v-list>
      </v-card-text>
      <v-card-actions>
        <v-btn @click="handleCreateGroupComplete()">
          创建群组
        </v-btn>
        <v-btn @click="resetCreateGroup">
          取消
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-dialog
    v-model="addMemberDialog"
    v-if="assign_option=='group'"
  >
    <v-card>
      <v-card-title>添加成员</v-card-title>
      <v-divider></v-divider>
      <v-card-text style="wrap-content">
        <h3 class="px-4 pt-4 pb-3 font-weight-black">可选成员</h3>
        <v-list two-line v-if="assign_option=='group'">
          <template v-for="(userItem, index) in exclusiveTableData">
            <v-list-item
              :key="userItem.username"
            >
              <v-list-item-action>
                <v-checkbox v-model="chosenUserForAddMember[index]">
                </v-checkbox>
              </v-list-item-action>
              <v-list-item-content>
                <v-list-item-title v-html="userItem.name"></v-list-item-title>
                <v-list-item-subtitle v-html="userItem.username"></v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </template>
        </v-list>
      </v-card-text>
      <v-card-actions>
        <v-btn @click="handleAddMemberComplete">
          添加成员
        </v-btn>
        <v-btn @click="resetAddMember">
          取消
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</v-container>
</template>


<script>
import COMM from "@/utils/Comm"
// import NewcomerBoardEdit from './subcomponents/NewcomerBoardEdit.vue'
import AssigneeTable from './subcomponents/AssigneeTable.vue'

  export default {
    name: 'CreateNotification',
    inject: ['GLOBAL'],
    components: {
      // NewcomerBoardEdit,
      AssigneeTable,
    },
    data () {
      return {
        newcomerIdentity: {}, // 该新人的所有数据在此字典中，辅助用于从后端获取该新人的数据
        formInline: { // 输入框（筛选）内容
            name: '',
            superior: '',
            city: '',
            employed: '', 
            graduated: '',
            role: ''
        },
        colData: [ // table的列项
          {title: "姓名",istrue: true}, // 0
          {title: "是否参与Bootcamp",istrue: true}, // 1
          {title: "直属上级",istrue: true}, // 2
          {title: "城市",istrue: true}, // 3
          {title: "入职情况",istrue: true}, // 4
          {title: "导师分配",istrue: true}, // 5
          {title: "是否毕业",istrue: true}, // 6
          {title: "新人看板",istrue: true}, // 7
          {title: "带新记录",istrue: true}, // 8
          {title: "新人评价",istrue: true}, // 9
          {title: "部门", istrue: true}, // 10
        ],
        colOptions: [],
        colSelect: [],
        tableData: [], // 后台拿来的数据
        // 显示新人看板
        newcomerBoardVisible: false,
        // columnShow: 只显示部分列
        columnShow: {
          // 新人管理
          name: true,
          joinBootcamp: true,
          department: true,
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
        toAddNotification: {
          title: "",
          content: ""
        },
        assign_options: [{
          label: '从列表选择',
          value: 'list'
        }, {
          label: '群组发送',
          value: 'group'
        }],
        assign_option: 'list',
        groupList: {},
        editGroupDialog: false,
        selectedIndex: 0,
        createGroupDialog: false,
        chosenUser: [],
        chosenGroup: [],
        curGroupID: 0,
        toAddGroup: {
          name: ""
        },
        exclusiveTableData: [],
        chosenUserForAddMember: [],
        addMemberDialog: false,
      }
    },
    computed: {
      tables() {  // 前端筛选后的数据
        if(this.formInline.name || this.formInline.employed  || this.formInline.city || this.formInline.graduated || this.formInline.superior || this.formInline.role){
          return this.tableData.filter(data => !this.formInline.name || data.name.toLowerCase().includes(this.formInline.name.toLowerCase()))
          .filter(data => (!this.formInline.employed || this.formInline.employed === "全部") || data.employed === this.formInline.employed)
          .filter(data => (!this.formInline.city || this.formInline.city === "全部") || data.city === this.formInline.city)
          .filter(data => (!this.formInline.graduated || this.formInline.graduated === "全部") || data.graduated === (this.formInline.graduated === "已毕业"))
          .filter(data => (!this.formInline.superior || this.formInline.superior === "全部") || data.superior === this.formInline.superior)
          .filter(data => (!this.formInline.role || this.formInline.role === '全部') || (this.formInline.role === '新人' && data.isNew) || (this.formInline.role === '导师' && data.isTeacher) || (this.formInline.role === 'HRBP' && data.isHRBP) || (this.formInline.role === '管理员' && data.isAdmin))
        }
        else return this.tableData
      }
    },
    watch: {
      colOptions(valArr) {  // 列项选择
        var arr = this.colSelect.filter(i => valArr.indexOf(i) < 0); // 未选中
        this.colData.filter(i => {
          i.istrue = arr.indexOf(i.title) === -1;
        });
      }
    },
    methods: {
      resetFilter() {  // 重置filter
        this.formInline = {}
      },
      async getDataFromBackend() {
        // 从后端获取新人列表的table信息，存储在this.tableData中
        var idRes = await COMM.getCurRole()
        var role = idRes.role
        if (role == 'admin') {
          var res = await COMM.get_admin_all_user_list()
          console.log("get admin_newcomer_list success: ", res)
          this.tableData = res.data;
          for(var i = 0; i < this.tableData.length; i++)
            this.chosenUser.push(false)
        }
          // COMM.get_admin_newcomer_list().then(res => {
          //         console.log("get admin_newcomer_list success: ", res)
          //         this.tableData = res.data;
          //         for(var i = 0; i < this.tableData.length; i++)
          //           this.chosenUser.push(false)
          //     }, err => {
          //         console.log("get admin_newcomer_list error: ", err)
          //     })
        else if (role == 'teacher')
          COMM.get_teacher_newcomer_list().then(res => {
              console.log("get admin_newcomer_list success: ", res)
              this.tableData = res.data;
              for(var i = 0; i < this.tableData.length; i++)
                this.chosenUser.push(false)
          }, err => {
              console.log("get admin_newcomer_list error: ", err)
          })
      },
      async getGroupList() {
        this.chosenGroup = []
        var res = await COMM.retrieve_group()
        if (res.result == 'success') {
          this.groupList = res.groups
          for (var i = 0; i < this.groupList.length; i++)
            this.chosenGroup.push(false)
        }
      },
      resetGroupMessage() {
        this.getGroupList()
        this.resetNotification()
        this.resetCreateGroup()
        this.resetAddMember()
      },
      async handleSendGroupMessage() {
        if (this.toAddNotification.title === '' || this.toAddNotification.content === '') {
          alert('标题和内容不能为空！')
          return 
        }
        var groups = []
        for(var i = 0; i < this.groupList.length; i++)
          if(this.chosenGroup[i])
            groups.push(this.groupList[i].groupID)
        if (groups.length == 0) {
          alert('请选择群组！')
          return
        }
        var postData = {
          'action': 'create group notification',
          'title': this.toAddNotification.title,
          'content': this.toAddNotification.content,
          'groups': groups
        }
        var res = await COMM.create_group_notification(postData)
        if (res.result == 'success')
          alert('发送成功')
        this.resetGroupMessage()
      },
      checkNewcomerBoard(data) {
        // 显示新人看板
        this.newcomerIdentity = data;
        this.newcomerBoardVisible = true;
      },
      resetNotification() {
        this.toAddNotification = {
          title: "",
          content: ""
        }
      },
      closeNewcomerBoard() { 
        // 提供给子组件NewcomerBoardEdit的回调函数
        this.newcomerBoardVisible = false;
      },
      renderMemberCount(index) {
        return "群组成员数：" + String(this.groupList[index].members.length)
      },
      editGroup(index) {
        this.selectedIndex = index
        this.editGroupDialog = true
      },
      createGroup() {
        this.createGroupDialog = true
      },
      async handleCreateGroupComplete() {
        if (this.toAddGroup.name === '') {
          alert('请填写群组名称！')
          return
        }
        var members = []
        for(var i = 0; i < this.tableData.length; i++)
          if(this.chosenUser[i])
            members.push(this.tableData[i].username)
        console.log(members)
        var postData = {
          'action': 'create group',
          'groupName': this.toAddGroup.name,
          'members': members
        }
        var res = await COMM.create_group(postData)
        if (res.result == 'success')
          alert('创建成功')
        this.resetCreateGroup()
      },
      resetCreateGroup() {
        this.createGroupDialog = false
        for(var i = 0; i < this.tableData.length; i++)
          this.chosenUser[i] = false
        this.toAddGroup.name = ""
        this.getGroupList()
      },
      addMember(group) {
        this.exclusiveTableData = []
        this.chosenUserForAddMember = []
        var oldMembers = new Set()
        for (var i = 0; i < group.members.length; i++)
          oldMembers.add(group.members[i].username)
        for (i = 0; i < this.tableData.length; i++)
          if (!(oldMembers.has(this.tableData[i].username)))
            this.exclusiveTableData.push(this.tableData[i])
        for (i = 0; i < this.exclusiveTableData.length; i++)
          this.chosenUserForAddMember.push(false)
        this.addMemberDialog = true
      },
      async handleAddMemberComplete() {
        // var success = true
        var newMembers = []
        for(var i = 0; i < this.exclusiveTableData.length; i++)
          if(this.chosenUserForAddMember[i]) {
            // var postData = {
            //   'action': 'add group member',
            //   'groupID': this.groupList[this.selectedIndex].groupID,
            //   'username': this.exclusiveTableData[i].username
            // }
            // var res = await COMM.add_group_member(postData)
            // success &= (res.result == 'success')
            newMembers.push(this.exclusiveTableData[i].username)
          }
          var postData = {
            'action': 'add group member',
            'groupID': this.groupList[this.selectedIndex].groupID,
            'username': newMembers
          }
        var res = await COMM.add_group_member(postData)
        if (res.result == 'success')
          alert('成员添加成功')
        else
          alert('网络异常，请重新检查此群组状态')
        this.resetAddMember()
      },
      resetAddMember() {
        this.addMemberDialog = false
        this.editGroupDialog = false
        for (var i = 0; i < this.exclusiveTableData.length; i++)
          this.chosenUserForAddMember = false
        this.getGroupList()
      },
      async deleteMember(username, groupIndex) {
        var groupID = this.groupList[groupIndex].groupID
        var postData = {
          'action': 'delete member',
          'groupID': groupID,
          'memberUsername': username
        }
        var res = await COMM.delete_member(postData)
        if (res.result == 'success') 
          this.getGroupList()
      },
      async deleteGroup(index) {
        var groupID = this.groupList[index].groupID
        var postData = {
          'action': 'delete group',
          'groupID': groupID
        }
        var res = await COMM.delete_group(postData)
        if (res.result === 'success') {
          alert('群组删除成功')
          this.getGroupList()
        }
      }
    },
    created() {
      this.getDataFromBackend();
      this.getGroupList();
      // 初始化列项选择
      var _this = this;
      for (let i = 0; i < _this.colData.length; i++) {
        _this.colSelect.push(_this.colData[i].title);
        if (_this.colData[i].title === '不想展示的名字') { //初始化不想展示的列可以放在这个条件里
          continue;
        }
        _this.colOptions.push(_this.colData[i].title); 
      }
      this.GLOBAL.contentDisplayAddif = true
    }
  }
</script>