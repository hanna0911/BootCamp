<template>
    <v-container>
        <div v-if="!showLeadNewcomer && !showTutorLearn">
        <h2 class="px-4 pt-4 font-weight-black">导师管理</h2>

        <!-- tab切换栏 -->
        <v-tabs v-model="tab">
            <v-tabs-slider></v-tabs-slider>
            <v-tab
                v-for="item in items"
                :key="item.tab"
            >
                {{ item.tab }}
            </v-tab>
        </v-tabs>

        <!-- TODO: 每个tab底下的内容 -->
        <v-tabs-items v-model="tab" style="margin: 1%">
            <v-tab-item
                v-for="item in items"
                :key="item.tab"
            >

                <!-- 上岗导师 -->
                <v-card v-if="item.tab === '上岗导师'" flat style="margin-top: 15px;">
                    <!-- 筛选输入框input form -->
                    <el-form :inline="true" :model="formInline" class="demo-form-inline">
                        <el-form-item label="导师姓名:" style="margin-left: 1.5%; margin-right: 1%" size="medium">
                            <el-input v-model="formInline.name" placeholder="请输入" style="width:150px"></el-input>
                        </el-form-item>
                        <el-form-item label="直属上级:" style="margin-left: 1.5%; margin-right: 1%" size="medium">
                            <el-select v-model="formInline.superior" placeholder="请选择" style="width:130px">
                                <el-option label="全部" value="全部"></el-option>
                                <el-option
                                    v-for="item in superiorOptions"
                                    :key="item"
                                    :label="item"
                                    :value="item">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="城市:" style="margin-left: 1.5%; margin-right: 1%" size="medium">
                            <el-select v-model="formInline.city" placeholder="请选择" style="width:130px">
                                <el-option label="全部" value="全部"></el-option>
                                <el-option
                                    v-for="item in cityOptions"
                                    :key="item"
                                    :label="item"
                                    :value="item">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-form>
                    <el-form :inline="true" style="margin-top: -58px; margin-right: 1%" :model="formInline" class="demo-form-inline" align="right">
                        <el-form-item style="margin-left: 1.5%; margin-right: 0.5%" size="medium">
                            <el-button size="small" @click="resetFilter">重置</el-button>
                        </el-form-item>
                        <el-form-item style="margin-left: 0.5%; margin-right: 0.5%" size="medium">
                            <!-- 选择特定列呈现 -->
                            <el-popover placement="right" width="400" trigger="click">
                            <el-checkbox-group v-model="colOptions">
                                <el-checkbox v-for="item in colSelect" :label="item" :key="item" ></el-checkbox>
                            </el-checkbox-group>
                            <el-button size="small" icon="el-icon-more" slot="reference"></el-button>
                            </el-popover>
                        </el-form-item>
                    </el-form>
                    
                    <!-- table表格 -->
                    <tutor-table 
                        :tables="tables" 
                        :colData="colData" 
                        :formInline="formInline" 
                        :columnShow="columnShow" 
                        :refreshNominatedList="getNominatedList"
                        :checkNewcomerTable="checkNewcomerTable"
                    ></tutor-table>
                </v-card>

                <!-- 提名进度 -->
                <v-card v-else-if="item.tab === '提名进度' && GLOBAL.ident === 'admin'" flat style="margin-top: 15px;">
                    <!-- 筛选输入框input form -->
                    <el-form :inline="true" :model="formInline" class="demo-form-inline">
                        <el-form-item label="导师姓名:" style="margin-left: 1.5%; margin-right: 1%" size="medium">
                            <el-input v-model="formInline.name" placeholder="请输入" style="width:150px"></el-input>
                        </el-form-item>
                        <el-form-item label="直属上级:" style="margin-left: 1.5%; margin-right: 1%" size="medium">
                            <el-select v-model="formInline.superior" placeholder="请选择" style="width:130px">
                                <el-option label="全部" value="全部"></el-option>
                                <el-option
                                    v-for="item in superiorOptions"
                                    :key="item"
                                    :label="item"
                                    :value="item">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="城市:" style="margin-left: 1.5%; margin-right: 1%" size="medium">
                            <el-select v-model="formInline.city" placeholder="请选择" style="width:130px">
                                <el-option label="全部" value="全部"></el-option>
                                <el-option
                                    v-for="item in cityOptions"
                                    :key="item"
                                    :label="item"
                                    :value="item">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-form>
                    <el-form :inline="true" style="margin-top: -58px; margin-right: 1%" :model="formInline" class="demo-form-inline" align="right">
                        <el-form-item style="margin-left: 1.5%; margin-right: 0.5%" size="medium">
                            <el-button size="small" @click="resetFilter">重置</el-button>
                        </el-form-item>
                        <el-form-item style="margin-left: 0.5%; margin-right: 0.5%" size="medium">
                            <!-- 选择特定列呈现 -->
                            <el-popover placement="right" width="400" trigger="click">
                            <el-checkbox-group v-model="colOptions">
                                <el-checkbox v-for="item in colSelect" :label="item" :key="item" ></el-checkbox>
                            </el-checkbox-group>
                            <el-button size="small" icon="el-icon-more" slot="reference"></el-button>
                            </el-popover>
                        </el-form-item>
                        <!-- <el-form-item style="margin-left: 0.5%; margin-right: 0.5%" size="medium">
                            <el-button size="small" type="primary" @click="nominate">提名</el-button>
                        </el-form-item> -->
                    </el-form>
                    
                    <!-- table表格 -->
                    <tutor-table 
                        :tables="tables" 
                        :colData="colData" 
                        :formInline="formInline" 
                        :columnShow="columnShow" 
                        :refreshNominatedList="getNominatedList"
                        :checkLearningBoard="checkLearningBoard"
                    ></tutor-table>
                
                </v-card>

                <!-- 提名审核 -->
                <v-card v-else-if="item.tab === '提名审核'" flat style="margin-top: 15px;">
                    <!-- 筛选输入框input form -->
                    <el-form :inline="true" :model="formInline" class="demo-form-inline">
                        <el-form-item label="导师姓名:" style="margin-left: 1.5%; margin-right: 1%" size="medium">
                            <el-input v-model="formInline.name" placeholder="请输入" style="width:150px"></el-input>
                        </el-form-item>
                        <el-form-item label="直属上级:" style="margin-left: 1.5%; margin-right: 1%" size="medium">
                            <el-select v-model="formInline.superior" placeholder="请选择" style="width:130px">
                                <el-option label="全部" value="全部"></el-option>
                                <el-option
                                    v-for="item in superiorOptions"
                                    :key="item"
                                    :label="item"
                                    :value="item">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="城市:" style="margin-left: 1.5%; margin-right: 1%" size="medium">
                            <el-select v-model="formInline.city" placeholder="请选择" style="width:130px">
                                <el-option label="全部" value="全部"></el-option>
                                <el-option
                                    v-for="item in cityOptions"
                                    :key="item"
                                    :label="item"
                                    :value="item">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-form>
                    <el-form :inline="true" style="margin-top: -58px; margin-right: 1%" :model="formInline" class="demo-form-inline" align="right">
                        <el-form-item style="margin-left: 1.5%; margin-right: 0.5%" size="medium">
                            <el-button size="small" @click="resetFilter">重置</el-button>
                        </el-form-item>
                        <el-form-item style="margin-left: 0.5%; margin-right: 0.5%" size="medium">
                            <!-- 选择特定列呈现 -->
                            <el-popover placement="right" width="400" trigger="click">
                            <el-checkbox-group v-model="colOptions">
                                <el-checkbox v-for="item in colSelect" :label="item" :key="item" ></el-checkbox>
                            </el-checkbox-group>
                            <el-button size="small" icon="el-icon-more" slot="reference"></el-button>
                            </el-popover>
                        </el-form-item>
                    </el-form>
                    
                    <!-- table表格 -->
                    <tutor-table 
                        :tables="tables" 
                        :colData="colData" 
                        :formInline="formInline" 
                        :columnShow="columnShow" 
                        :refreshNominatedList="getNominatedList"
                        :checkLearningBoard="checkLearningBoard"
                    ></tutor-table>

                </v-card>

                <!-- 候选人列表-导师提名 -->
                <v-card v-else-if="item.tab === '候选人列表-导师提名' && GLOBAL.ident === 'admin'" flat style="margin-top: 15px;">
                    <!-- 筛选输入框input form -->
                    <el-form :inline="true" :model="formInline" class="demo-form-inline">
                        <el-form-item label="导师姓名:" style="margin-left: 1.5%; margin-right: 1%" size="medium">
                            <el-input v-model="formInline.name" placeholder="请输入" style="width:150px"></el-input>
                        </el-form-item>
                        <el-form-item label="直属上级:" style="margin-left: 1.5%; margin-right: 1%" size="medium">
                            <el-select v-model="formInline.superior" placeholder="请选择" style="width:130px">
                                <el-option label="全部" value="全部"></el-option>
                                <el-option
                                    v-for="item in superiorOptions"
                                    :key="item"
                                    :label="item"
                                    :value="item">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="城市:" style="margin-left: 1.5%; margin-right: 1%" size="medium">
                            <el-select v-model="formInline.city" placeholder="请选择" style="width:130px">
                                <el-option label="全部" value="全部"></el-option>
                                <el-option
                                    v-for="item in cityOptions"
                                    :key="item"
                                    :label="item"
                                    :value="item">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-form>
                    <el-form :inline="true" style="margin-top: -58px; margin-right: 1%" :model="formInline" class="demo-form-inline" align="right">
                        <el-form-item style="margin-left: 1.5%; margin-right: 0.5%" size="medium">
                            <el-button size="small" @click="resetFilter">重置</el-button>
                        </el-form-item>
                        <el-form-item style="margin-left: 0.5%; margin-right: 0.5%" size="medium">
                            <!-- 选择特定列呈现 -->
                            <el-popover placement="right" width="400" trigger="click">
                            <el-checkbox-group v-model="colOptions">
                                <el-checkbox v-for="item in colSelect" :label="item" :key="item" ></el-checkbox>
                            </el-checkbox-group>
                            <el-button size="small" icon="el-icon-more" slot="reference"></el-button>
                            </el-popover>
                        </el-form-item>
                        <el-form-item style="margin-left: 0.5%; margin-right: 0.5%" size="medium">
                            <el-button size="small" type="primary" @click="nominate">提名</el-button>
                        </el-form-item>
                    </el-form>
                    
                    <!-- table表格 -->
                    <TutorTable
                        ref="waitList"
                        :tables="tables" 
                        :colData="colData" 
                        :formInline="formInline" 
                        :columnShow="columnShow" 
                        :refreshNominatedList="getNominatedList"
                        :checkNewcomerTable="checkNewcomerTable"
                        :checkLearningBoard="checkLearningBoard"
                    ></TutorTable>
  
                </v-card>

            </v-tab-item>
        </v-tabs-items>
        </div>

        <div v-else-if="showLeadNewcomer">
            <div style="margin-left: 20px; margin-top: 10px; margin-bottom: -20px">
                <v-btn @click="showLeadNewcomer = false">返回</v-btn>
                <h2 class="px-4 pt-4 pb-3 font-weight-black">导师 {{ tutorIdentity.name }} 的带新看板</h2>
            </div>
            <!-- 带新看板 -->
            <lead-newcomer-sub :tutorIdentity="tutorIdentity"/>
        </div>

        <div v-else-if="showTutorLearn">
            <!-- 导师培训 -->
            <NewcomerBoardEdit :newcomerIdentity="infos" :showAudience="'teacher'" :closeNewcomerBoard="closeNewcomerBoard"/>
        </div>

    </v-container>
</template>

<script>
import COMM from "@/utils/Comm";
import TutorTable from './subcomponents/TutorTable.vue'
import LeadNewcomerSub from './subcomponents/LeadNewcomerSub.vue'
import NewcomerBoardEdit from './subcomponents/NewcomerBoardEdit.vue'

export default({
    name: "TutorManage",
    components: {
        TutorTable,
        LeadNewcomerSub,
        NewcomerBoardEdit,
    },
    inject: ["GLOBAL"],
    data () {
        return {
            infos: {},

            // 筛选栏修改
            superiorOptions: ["上级A", "上级B"],
            cityOptions: ["北京", "上海", "深圳"],

            tutorIdentity: {}, // 导师身份（点击【查看带新看板】时对应导师的所有信息）
            showLeadNewcomer: false, // 显示带新看板
            showTutorLearn: false, // same
            tab: null,  // vuetify默认设置
            items: [  // tab栏+内容（内容暂时无用，考虑是否删掉）
                { tab: '上岗导师', content: 'Tab 1 Content' },
                { tab: '提名进度', content: 'Tab 2 Content' },
                { tab: '提名审核', content: 'Tab 3 Content' },
                { tab: '候选人列表-导师提名', content: 'Tab 4 Content' },
            ],
            formInline: {  // 输入框（用于筛选，初始值均为空）
                name: '',
                superior: '',
                city: ''
            },
            // TODO: 后端拿来的数据
            tableData: [],
            // table的列项
            colData: [
                {title: "姓名", istrue: true},
                {title: "部门", istrue: true},
                {title: "直属上级", istrue: true},
                {title: "城市", istrue: true},
                {title: "入职时间", istrue: true},
            ],
            colOptions: [],
            colSelect: [],
            columnShow: { // 因为不同的tab所需要显示的列项内容不同，因此要在表格处做一些筛选，传给子组件TutorTable其是否显示某些列这一columnShow参数
                name: true,
                currentMembers: false,
                historicalMembers: false,
                department: true, 
                superior: true, 
                city: true, 
                joinDate: true, 
                teacherDutyDate: false,
                newcomerBoard: false,
                teacherScore: false,
                operation: false,
                OKR: false,   
            },
        }
    },
    computed: {
        tables() {  // 前端筛选后的数据
            if(this.formInline.name || this.formInline.city || this.formInline.superior){
                return this.tableData.filter(data => !this.formInline.name || data.name.toLowerCase().includes(this.formInline.name.toLowerCase()))
                .filter(data => (!this.formInline.city || this.formInline.city === "全部") || data.city === this.formInline.city)
                .filter(data => (!this.formInline.superior || this.formInline.superior === "全部") || data.superior === this.formInline.superior)
            }
            else return this.tableData
        }
    },
    watch: {
        colOptions(valArr) {  // 列项选择
            var arr = this.colSelect.filter(i => valArr.indexOf(i) < 0); // 未选中
            this.colData.filter(i => {
            if (arr.indexOf(i.title) !== -1) {
                i.istrue = false;
            } else {
                i.istrue = true;
            }
            });
        },
        tab(data) {
            if(this.GLOBAL.ident === 'admin'){
            switch(data){
                case 0:{
                    // 上岗导师
                    this.columnShow = { // 因为不同的tab所需要显示的列项内容不同，因此要在表格处做一些筛选，传给子组件TutorTable其是否显示某些列这一columnShow参数
                        name: true,
                        currentMembers: true,
                        historicalMembers: true,
                        department: true, 
                        superior: true, 
                        city: true, 
                        joinDate: true, 
                        nominateDate: false,
                        trainStatus: false,
                        operation: false,
                        teacherDutyDate: true,
                        newcomerBoard: true,
                        teacherScore: true,
                        OKR: true,   
                    }
                    this.getDutyTeacherList();
                    break;
                }
                case 1:{
                    // TODO: 提名进度
                    this.columnShow = { // 因为不同的tab所需要显示的列项内容不同，因此要在表格处做一些筛选，传给子组件TutorTable其是否显示某些列这一columnShow参数
                        name: true,
                        currentMembers: false,
                        historicalMembers: false,
                        department: true, 
                        superior: true, 
                        city: true, 
                        joinDate: true,
                        nominateDate: true,  // 多了这个条目！后端需要返回：提名时间
                        trainStatus: true,  // 多了这个条目！后端需要返回：导师培训状态
                        operation: false,  // 多了这个条目！后端需要返回：操作
                        checkStatus: true, // 多了这个条目！后端需要返回：审核状态
                        teacherDutyDate: false,  
                        newcomerBoard: false,
                        teacherScore: false,
                        OKR: false,   
                    }
                    this.getNominateProcess();
                    break;
                }
                case 2:{
                    // 提名审核
                    this.columnShow = { // 因为不同的tab所需要显示的列项内容不同，因此要在表格处做一些筛选，传给子组件TutorTable其是否显示某些列这一columnShow参数
                        name: true,
                        currentMembers: false,
                        historicalMembers: false,
                        department: true, 
                        superior: true, 
                        city: true, 
                        joinDate: true, 
                        nominateDate: true,  // 多了这个条目！后端需要返回：提名时间
                        trainStatus: true,  // 多了这个条目！后端需要返回：导师培训状态
                        operation: true,  // 多了这个条目！后端需要返回：操作
                        teacherDutyDate: false,  
                        newcomerBoard: false,
                        teacherScore: false,
                        OKR: false,   
                    }
                    this.getNominatedList();
                    break;
                }
                case 3:{
                    // 候选人列表-导师提名
                    this.columnShow = { // 因为不同的tab所需要显示的列项内容不同，因此要在表格处做一些筛选，传给子组件TutorTable其是否显示某些列这一columnShow参数
                        name: true,
                        currentMembers: false,
                        historicalMembers: false,
                        department: true, 
                        superior: true, 
                        city: true, 
                        joinDate: true, 
                        newcomerBoard: false,
                        nominateDate: false, // 多了这个条目！后端需要返回：提名时间
                        trainStatus: false,  // 多了这个条目！后端需要返回：导师培训状态
                        operation: false,  // 多了这个条目！后端需要返回：操作
                        teacherDutyDate: false,  
                        teacherScore: false,
                        OKR: false,   
                    }
                    this.getTeacherWaitList();
                    break;
                }
                default:{
                    break;
                }
            }
            } else if (this.GLOBAL.ident === 'hrbp'){
                switch(data){
                case 0:{
                    // 上岗导师
                    this.columnShow = { // 因为不同的tab所需要显示的列项内容不同，因此要在表格处做一些筛选，传给子组件TutorTable其是否显示某些列这一columnShow参数
                        name: true,
                        currentMembers: true,
                        historicalMembers: true,
                        department: true, 
                        superior: true, 
                        city: true, 
                        joinDate: true, 
                        nominateDate: false,
                        trainStatus: false,
                        operation: false,
                        teacherDutyDate: true,
                        newcomerBoard: true,
                        teacherScore: true,
                        OKR: true,   
                    }
                    this.getDutyTeacherList();
                    break;
                }
                case 1:{
                    // 提名审核
                    this.columnShow = { // 因为不同的tab所需要显示的列项内容不同，因此要在表格处做一些筛选，传给子组件TutorTable其是否显示某些列这一columnShow参数
                        name: true,
                        currentMembers: false,
                        historicalMembers: false,
                        department: true, 
                        superior: true, 
                        city: true, 
                        joinDate: true, 
                        nominateDate: true,  // 多了这个条目！后端需要返回：提名时间
                        trainStatus: true,  // 多了这个条目！后端需要返回：导师培训状态
                        operation: true,  // 多了这个条目！后端需要返回：操作
                        teacherDutyDate: false,  
                        newcomerBoard: false,
                        teacherScore: false,
                        OKR: false,   
                    }
                    this.getNominatedList();
                    break;
                }
                default:{
                    break;
                }
            }
            }
        }
    },
    methods: {
        closeNewcomerBoard(){
            this.showTutorLearn = false;
        },

        nominate() {
            console.log('nominate!');
            console.log(this.$refs.waitList)
            var temp = this.$refs.waitList;
            temp[0].nominateSelectedTeacher();
            this.getTeacherWaitList();
            temp[0].$forceUpdate();
        },
        resetFilter() {  // 重置filter
            this.formInline = {}
        },
        getDutyTeacherList() {
          //  从后端获取在职老师列表的table信息，存储在this.tableData中
          COMM.get_duty_teacher_list().then(res => {
            console.log("get admin duty_teacher_list success: ", res)
            this.tableData = res.data;
            this.initializeSelectOptions();
          }, err => {console.log("get admin duty_teacher_list error: ", err)})
        },
        getNominateProcess(){
          COMM.get_nominate_process().then(res=>{
            console.log("get admin nominate process success: ", res)
            this.tableData = res.data;
            this.initializeSelectOptions();
          },err=>{console.log("get admin nominate process error: ", err)})
        },
        getTeacherWaitList(){
            COMM.get_teacher_wait_list().then(res=>{
            console.log("get admin teacher wait list success: ", res)
            this.tableData = res.data;
            this.initializeSelectOptions();
            },err=>{console.log("get admin teacher wait list error: ", err)})
        },
        getNominatedList(){
            COMM.get_nominated_list().then(res=>{
            console.log("get admin nominated list success: ", res)
            this.tableData = res.data;
            this.initializeSelectOptions();
            },err=>{console.log("get admin nominated list error: ", err)})
        },
        checkNewcomerTable(data){ // 提供给子组件TutorTable调用的回调函数
            // 子组件TutorTable点击查看新人看板 -> 改变数据值唤醒子组件NewcomerTable中的内容
            console.log('tutor data:', data)
            this.tutorIdentity = data
            this.showLeadNewcomer = true
        },
        checkLearningBoard(data){ // 同上
            this.infos = data
            this.showTutorLearn = true;
        },
        initializeSelectOptions(){
            /* 
            初始化筛选框
            是否应该优化成watch(tabledata) -> initializeSelectOptions?
             */
            var tableData = this.tableData;
            var superiorOptions = [];
            var cityOptions = [];
            for(var i = 0; i < tableData.length; i++){
                superiorOptions.push(tableData[i].superior);
                cityOptions.push(tableData[i].city);
            }
            this.superiorOptions = Array.from(new Set(superiorOptions));
            this.cityOptions = Array.from(new Set(cityOptions));
        },
    },
    created() {
        if(this.GLOBAL.ident === 'admin'){
            this.items = [  // tab栏+内容（内容暂时无用，考虑是否删掉）
                { tab: '上岗导师', content: 'Tab 1 Content' },
                { tab: '提名进度', content: 'Tab 2 Content' },
                { tab: '提名审核', content: 'Tab 3 Content' },
                { tab: '候选人列表-导师提名', content: 'Tab 4 Content' },
            ]
        }
        else if (this.GLOBAL.ident === 'hrbp'){
            this.items = [  // tab栏+内容（内容暂时无用，考虑是否删掉）
                { tab: '上岗导师', content: 'Tab 1 Content' },
                { tab: '提名审核', content: 'Tab 3 Content' },
            ]
        }

        // 初始化列项选择
        this.getDutyTeacherList();
        var _this = this;
        for (let i = 0; i < _this.colData.length; i++) {
            _this.colSelect.push(_this.colData[i].title);
            if (_this.colData[i].title === '不想展示的名字') { //初始化不想展示的列可以放在这个条件里
                continue;
            }
            _this.colOptions.push(_this.colData[i].title); 
        }
    }
})
</script>
