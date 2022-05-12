<template>
<v-container>
  <div v-if="!newcomerBoardVisible">
  <h2 class="px-4 pt-4 pb-3 font-weight-black">新人管理</h2>
  <v-spacer></v-spacer>
    
  <!-- elementUI输入框 -->
  <!-- 输入框一行一个el-form -->
  <el-form :inline="true" :model="formInline" class="demo-form-inline">
      <el-form-item label="新人姓名:" style="margin-left: 1.5%; margin-right: 1%" size="medium">
          <el-input v-model="formInline.name" placeholder="请输入" style="width:150px"></el-input>
      </el-form-item>
      <el-form-item label="是否参与Bootcamp:" style="margin-left: 1.5%; margin-right: 1%" size="medium">
          <el-select v-model="formInline.joinBootcamp" placeholder="请选择" style="width:120px">
            <el-option label="全部" value="全部"></el-option>
            <el-option label="是" value="是"></el-option>
            <el-option label="否" value="否"></el-option>
          </el-select>
      </el-form-item>
      <el-form-item label="直属上级:" style="margin-left: 1.5%; margin-right: 1%" size="medium">
          <el-select v-model="formInline.superior" placeholder="请选择" style="width:150px">
            <el-option label="全部" value="全部"></el-option>
            <el-option
              v-for="item in superiorOptions"
              :key="item"
              :label="item"
              :value="item">
            </el-option>
          </el-select>
      </el-form-item>
  </el-form>
  <el-form :inline="true" :model="formInline" class="demo-form-inline">
      <el-form-item label="城市:" style="margin-left: 1.5%; margin-right: 1%" size="medium">
          <el-select v-model="formInline.city" placeholder="请选择" style="width:150px">
            <el-option label="全部" value="全部"></el-option>
            <el-option
              v-for="item in cityOptions"
              :key="item"
              :label="item"
              :value="item">
            </el-option>
          </el-select>
      </el-form-item>
      <el-form-item label="入职情况:" style="margin-left: 1.5%; margin-right: 1%" size="medium">
          <el-select v-model="formInline.employed" placeholder="请选择" style="width:150px">
            <el-option label="全部" value="全部"></el-option>
            <el-option
              v-for="item in employedOptions"
              :key="item"
              :label="item"
              :value="item">
            </el-option>
          </el-select>
      </el-form-item>
      <el-form-item label="导师分配:" style="margin-left: 1.5%; margin-right: 1%" size="medium">
          <el-select v-model="formInline.tutor" placeholder="请选择" style="width:150px">
            <el-option label="全部" value="全部"></el-option>
            <el-option
              v-for="item in tutorOptions"
              :key="item"
              :label="item"
              :value="item">
            </el-option>
          </el-select>
      </el-form-item>
  </el-form>
  <el-form :inline="true" :model="formInline" class="demo-form-inline">
      <el-form-item label="是否毕业:" style="margin-left: 1.5%; margin-right: 1%" size="medium">
          <el-select v-model="formInline.graduated" placeholder="请选择" style="width:150px">
          <el-option label="全部" value="全部"></el-option>
          <el-option label="已毕业" value="已毕业"></el-option>
          <el-option label="未毕业" value="未毕业"></el-option>
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
  <newcomer-table 
    :tables="tables" 
    :colData="colData" 
    :formInline="formInline" 
    :checkNewcomerBoard="checkNewcomerBoard"
    :columnShow="columnShow"
    :reGetData="getDataFromBackend"
    ></newcomer-table>
  
  </div>
  <newcomer-board-edit v-else :closeNewcomerBoard="closeNewcomerBoard" :newcomerIdentity="newcomerIdentity" :showAudience="'newcomer'"></newcomer-board-edit>
</v-container>
</template>


<script>
import COMM from "@/utils/Comm"
import NewcomerBoardEdit from './subcomponents/NewcomerBoardEdit.vue'
import NewcomerTable from './subcomponents/NewcomerTable.vue'

  export default {
    name: 'NewcomerManage',
    inject: ['GLOBAL'],
    components: {
      NewcomerBoardEdit,
      NewcomerTable,
    },
    data () {
      return {
        // 筛选栏修改
        superiorOptions: ["上级A", "上级B"],
        cityOptions: ["北京", "上海", "深圳"],
        employedOptions: ["已入职", "待入职"],
        tutorOptions: ["导师A", "导师B"],

        newcomerIdentity: {}, // 该新人的所有数据在此字典中，辅助用于从后端获取该新人的数据
        formInline: { // 输入框（筛选）内容
            name: '',
            joinBootcamp: '',
            superior: '',
            city: '',
            employed: '', 
            tutor: '',
            graduated: '',
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
          // {title: "带新记录",istrue: true}, // 8
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
          notes: false,
          evaluate: true, 
          // 带新看板
          newcomerType: false, 
          checklist: false,
        },
      }
    },
    computed: {
      tables() {  // 前端筛选后的数据
        if(this.formInline.name || this.formInline.employed || this.formInline.joinBootcamp || this.formInline.city || this.formInline.graduated || this.formInline.superior || this.formInline.tutor){
          return this.tableData.filter(data => !this.formInline.name || data.name.toLowerCase().includes(this.formInline.name.toLowerCase()))
          .filter(data => (!this.formInline.joinBootcamp || this.formInline.joinBootcamp === "全部") || data.joinBootcamp === (this.formInline.joinBootcamp === "是"))
          .filter(data => (!this.formInline.employed || this.formInline.employed === "全部") || data.employed === this.formInline.employed)
          .filter(data => (!this.formInline.city || this.formInline.city === "全部") || data.city === this.formInline.city)
          .filter(data => (!this.formInline.graduated || this.formInline.graduated === "全部") || data.graduated === (this.formInline.graduated === "已毕业"))
          .filter(data => (!this.formInline.superior || this.formInline.superior === "全部") || data.superior === this.formInline.superior)
          .filter(data => (!this.formInline.tutor || this.formInline.tutor === "全部") || data.tutor === this.formInline.tutor)
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
      initializeSelectOptions(){
        /* 
        初始化筛选框
        是否应该优化成watch(tabledata) -> initializeSelectOptions?
        */
        var tableData = this.tableData;
        var superiorOptions = [];
        var cityOptions = [];
        var employedOptions = [];
        var tutorOptions = [];
        for(var i = 0; i < tableData.length; i++){
            superiorOptions.push(tableData[i].superior);
            cityOptions.push(tableData[i].city);
            employedOptions.push(tableData[i].employed);
            tutorOptions.push(tableData[i].tutor);
        }
        this.superiorOptions = Array.from(new Set(superiorOptions));
        this.cityOptions = Array.from(new Set(cityOptions));
        this.employedOptions = Array.from(new Set(employedOptions));
        this.tutorOptions = Array.from(new Set(tutorOptions));
      },
      resetFilter() {  // 重置filter
        this.formInline = {}
      },
      getDataFromBackend() {
        // 从后端获取新人列表的table信息，存储在this.tableData中
        COMM.get_admin_newcomer_list().then(res => {
                console.log("get admin_newcomer_list success: ", res)
                this.tableData = res.data;
                this.initializeSelectOptions();
            }, err => {
                console.log("get admin_newcomer_list error: ", err)
            })
      },
      checkNewcomerBoard(data) {
        // 显示新人看板
        this.newcomerIdentity = data;
        this.newcomerBoardVisible = true;
      },
      closeNewcomerBoard() { 
        // 提供给子组件NewcomerBoardEdit的回调函数
        this.newcomerBoardVisible = false;
      },
    },
    created() {
      this.getDataFromBackend();
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