<template>
    <v-card>
      <h2 class="px-4 pt-4 pb-3 font-weight-black">任务</h2>
      <div style="margin: 2%">

     <!-- 筛选栏 -->
      <el-form :inline="true" :model="formInline" class="demo-form-inline" style="margin-left: 10px">
          <el-form-item style="margin-left: 1.5%; margin-right: 1%" size="small">
              <el-select v-if="GLOBAL.contentDisplayUser" v-model="formInline.learnStatus" placeholder="学习状态" style="width:110px">
                <el-option label="全部" value="全部"></el-option>
                <el-option
                  v-for="item in learnStatusOptions"
                  :key="item"
                  :label="item"
                  :value="item">
                </el-option>
              </el-select>
          </el-form-item>
          <el-form-item style="margin-left: 1.5%; margin-right: 1%" size="small">
              <el-select v-model="formInline.recommendTime" placeholder="时间" style="width:90px">
                <el-option label="全部" value="全部"></el-option>
                <el-option
                  v-for="item in recommendTimeOptions"
                  :key="item"
                  :label="item"
                  :value="item">
                </el-option>
              </el-select>
          </el-form-item>
          <el-form-item style="margin-left: 1.5%; margin-right: 1%" size="small">
              <el-select v-model="formInline.tag" placeholder="标签" style="width:100px">
                <el-option label="全部" value="全部"></el-option>
                <el-option
                  v-for="item in tagOptions"
                  :key="item"
                  :label="item"
                  :value="item">
                </el-option>
              </el-select>
          </el-form-item>
          <!-- classType必修/选修 -->
          <el-form-item style="margin-left: 1.5%; margin-right: 1%" size="small">
              <el-select v-model="formInline.classType" placeholder="必修/选修" style="width:110px">
                <el-option label="全部" value="全部"></el-option>
                <el-option label="必修" value="必修"></el-option>
                <el-option label="选修" value="选修"></el-option>
                <!-- <el-option
                  v-for="item in classTypeOptions"
                  :key="item"
                  :label="item"
                  :value="item">
                </el-option> -->
              </el-select>
          </el-form-item>
      </el-form>

        <!-- 任务dialog弹窗 -->
        <div v-if="GLOBAL.contentDisplayAddif">
          <v-dialog
          v-model="uploadTaskDialog"
          persistent
          max-width="800px"
          >
          <template v-slot:activator="{ on, attrs }">
              <div align="center">
                <v-btn style="margin: 2px" large v-bind="attrs" v-on="on">
                  <v-icon left medium>mdi-plus</v-icon>新建任务
                </v-btn>
                &nbsp;
                <v-btn style="margin: 2px" large @click="openAddFromDialog">
                  <v-icon left medium>mdi-plus</v-icon>从任务库添加
                </v-btn>
              </div>
          </template>
          <v-card>
              <v-card-title>添加任务</v-card-title>
              <v-divider></v-divider>
              <v-card-text>
                <div style="margin-top: 35px; margin-right: 20px">
                  <el-form :model="toAddTask" :rules="rules" ref="toAddTask" label-width="100px">
                  <el-form-item label="任务名称：" prop="name">
                      <el-input v-model="toAddTask.name"></el-input>
                  </el-form-item>
                  <el-form-item label="任务简介：" prop="intro">
                      <el-input v-model="toAddTask.intro"></el-input>
                  </el-form-item>
                  <!-- 标签 -->
                  <el-form-item label="考试标签：" prop="tag">
                      <!-- <el-input v-model="to A d d.tag"></el-input> -->
                      <el-tag
                        :key="tag"
                        v-for="tag in toAddTask.tag"
                        closable
                        :disable-transitions="false"
                        @close="handleClose(tag)">
                        {{tag}}
                      </el-tag>
                      <el-input
                        class="input-new-tag"
                        v-if="inputVisible"
                        v-model="inputValue"
                        ref="saveTagInput"
                        size="small"
                        @keyup.enter.native="handleInputConfirm"
                        @blur="handleInputConfirm"
                      >
                      </el-input>
                      <el-button v-else class="button-new-tag" size="small" @click="showInput">+ 新建标签</el-button>                  
                  </el-form-item>
                  <!-- 必修选修 -->
                  <el-form-item label="课程性质：" prop="isObligatory">
                    <!-- <el-select v-model="audience_value" placeholder="请选择" v-bind="toAddTest.audience"> -->
                    <el-select v-model="toAddTask.isObligatory" placeholder="请选择">
                      <el-option label="必修" :value="true"></el-option>
                      <el-option label="选修" :value="false"></el-option>
                    </el-select>
                  </el-form-item>
                  <el-form-item label="推荐用时：" prop="recommend_time">
                      <el-input v-model="toAddTask.recommend_time"
                                type="number"
                                oninput="if(value<0)value =0"
                      ></el-input>
                  </el-form-item>
                  <el-form-item label="受众：" prop="audience">
                      <el-select v-model="toAddTask.audience" placeholder="请选择" >
                        <el-option 
                          v-for="(item, index) in audience_options" 
                          :label="item.label" 
                          :value="item.value" 
                          :key="index">
                        </el-option>
                      </el-select>
                  </el-form-item>
                  <el-form-item label="是否模板：">
                      <el-checkbox v-model="toAddTask.is_template" @change="checkAddTaskSetTemplateClearance()">*仅管理员可设置模板</el-checkbox>
                  </el-form-item>
                  <v-divider dark>
                    任务类型
                  </v-divider>
                  <el-form-item label="任务类型：" prop="taskType">
                      <el-select v-model="toAddTask.taskType" placeholder="请选择" v-bind="toAddTask.taskType" @change="renderTaskUploadWidget()">
                        <el-option 
                          v-for="(item, index) in task_type_options" 
                          :label="item.label" 
                          :value="item.value" 
                          :key="index">
                        </el-option>
                      </el-select>
                  </el-form-item>
                  <el-form-item label="任务文字：" prop="taskText" v-if="isTextTask">
                    <el-input :rows="4" type="textarea" v-model="toAddTask.taskText"></el-input>
                  </el-form-item>
                  <!-- <el-form-item label="任务文件：" prop="taskFile" v-if="isFileTask"> -->
                  <el-form-item label="任务文件：" v-if="isFileTask">
                    <!-- 这里是上传的action，不太清楚elementUI的操作，可以查一下 -->
                    <el-upload
                      ref="upload_task_file"
                      class="upload-demo"
                      drag
                      :http-request="uploadTask"
                      :show-file-list="true"
                      :auto-upload="false"
                      :action="uploadTask"
                      >
                      <i class="el-icon-upload"></i>
                      <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                      <div style="margin-top: -15px" class="el-upload__tip" slot="tip">只能上传视频（mp4/flv/mov文件）与课件（ppt/pptx/key/pdf文件）</div>
                    </el-upload>
                  </el-form-item>
                  <el-form-item label="任务链接：" prop="taskLink" v-if="isLinkTask">
                    <el-input :rows="2" type="textarea" v-model="toAddTask.taskLink"></el-input>
                  </el-form-item>
                  </el-form>
                </div>
              </v-card-text>
              <v-divider></v-divider>
              <v-card-actions>
              <v-btn
                  color="blue darken-1"
                  text
                  @click="resetTaskForm('toAddTask')"
              >
                  取消
              </v-btn>
              <v-btn
                  color="blue darken-1"
                  text
                  @click="taskCommit('toAddTask')"
              >
                  上传
              </v-btn>
              </v-card-actions>
          </v-card>
          </v-dialog>
        </div>

        <div v-if="GLOBAL.contentDisplayAddif" style="margin: 10px; margin-top: 30px; margin-bottom: 20px">
          <v-dialog
            v-model="addFromDialog"
            max-width="1000px"
          >
            <!-- 添加课程按钮 -->
            <!-- 添加课程界面 -->
            <v-card>
              <v-toolbar dark color="primary">
                <v-btn icon dark @click="addFromDialog = false">
                  <v-icon>mdi-close</v-icon>
                </v-btn>
                <v-toolbar-title>从任务库添加</v-toolbar-title>
                <v-spacer></v-spacer>
              </v-toolbar>
              <v-divider></v-divider>
              <v-card-text>
              <div style="margin-top: 30px; margin-left: 20px; margin-right: 20px">
              <el-input
                placeholder="请输入课程名称"
                prefix-icon="el-icon-search"
                clearable
                v-model="search_name">
              </el-input>
              </div>  
              <div>
              <v-list>
                <v-list-item-group>
                <template v-for="item in addFromList_modified">
                <v-list-item :key="item.name">
                  <v-list-item-content>
                      <v-list-item-title v-bind="attrs" v-on="on" class="font-weight-black" v-text="item.name"></v-list-item-title>
                      <v-row style="margin-top: -5px; margin-bottom: -15px">
                        <!-- 推荐学习时间 -->
                        <v-col>
                          <v-list-item-subtitle
                            style="margin-top: 5px; margin-bottom: 15px"
                            class="text--primary"
                          >
                            <v-chip>{{item.recommendTime + "小时"}}
                            </v-chip>
                          </v-list-item-subtitle>
                        </v-col>
                        <!-- 必修、选修tag -->
                        <v-col>
                          <v-list-item-subtitle
                              style="margin-top: 5px; margin-bottom: 15px"
                              class="text--primary"
                            >
                              <span v-for="(tag, tag_id) in item.tag" :key="tag_id">
                              <v-chip>{{tag}}</v-chip>&nbsp;</span>
                          </v-list-item-subtitle>
                        </v-col>
                        <v-col>
                          <v-btn block large @click="addFromToProgram(item.contentID)">
                          添加
                          </v-btn>
                        </v-col>
                      </v-row>
                      <v-list-item-subtitle v-bind="attrs" v-on="on" v-text="item.intro"></v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
                </template>
                </v-list-item-group>
              </v-list>
              </div>
              </v-card-text>
            </v-card>
          </v-dialog>
        </div>

        <!-- 任务清单 -->
        <div style="margin-top: -15px">
        <v-list three-line>
          <v-list-item-group
            v-model="task_selected"
            active-class=""
            multiple
          >
            <template v-for="(task_item, index) in task_items_modified">
              <v-list-item :key="task_item.name">
                <template v-slot:default="{  }">
                  <v-list-item-action @click="handleTaskClick(task_item)">
                      <v-checkbox v-if='GLOBAL.contentDisplayUser' disabled v-model="task_item.isFinished"></v-checkbox>
                  </v-list-item-action>

                  <v-list-item-content>
                    <v-list-item-title @click="handleTaskClick(task_item)" v-text="task_item.name"></v-list-item-title>

                      <v-row>
                        <!-- 推荐学习时间 -->
                        <v-col @click="handleTaskClick(task_item)">
                          <!-- 管理员权限 -->
                          <v-select
                            v-if="false"
                            v-model="task_item.recommendTime"
                            :items="task_recommend_time_items"
                            chips
                            label="建议时间"
                            placeholder="添加标签"
                            single-line
                            small-chips
                            dense
                          ></v-select>
                          <!-- 新人、导师权限 -->
                          <v-chip v-else style="margin-top: 5px; margin-bottom: 15px">{{ task_item.recommendTime }}小时</v-chip>
                        </v-col>

                        <!-- 标签tag：成列表展示 -->
                        <v-col @click="handleTaskClick(task_item)">
                          <v-list-item-subtitle
                              style="margin-top: 5px; margin-bottom: 15px"
                              class="text--primary"
                            >
                              <span v-for="(tag, tag_id) in task_item.tag" :key="tag_id">
                                <v-chip v-if="tag !== ''">{{tag}}</v-chip>&nbsp;
                              </span>
                          </v-list-item-subtitle>
                        </v-col>

                        <!-- 必修选修tag -->
                        <v-col @click="handleTaskClick(task_item)">
                          <v-list-item-subtitle
                              style="margin-top: 5px; margin-bottom: 15px"
                              class="text--primary"
                            >
                              <v-chip>{{task_item.isObligatory ? '必修' : '选修'}}</v-chip>
                          </v-list-item-subtitle>
                        </v-col>
                        
                        <v-col @click="handleTaskClick(task_item)" v-if="GLOBAL.contentDisplayUser">
                          <v-combobox
                            v-if="false"
                            v-model="task_item.tag"
                            :items="task_tag_items"
                            chips
                            label="添加标签"
                            placeholder="添加标签"
                            small-chips
                            dense
                            single-line
                          >
                            <template v-slot:selection="{ attrs, item, taskTag_select, taskTag_selected }">
                              <v-chip
                                v-bind="attrs"
                                :input-value="taskTag_selected"
                                @click="taskTag_select"
                                small
                              >{{ item }}
                              </v-chip>
                            </template>
                          </v-combobox>
                          <v-chip style="margin-top: 5px; margin-bottom: 15px" v-else>{{ task_item.isFinished ? '已完成': '未完成' }}</v-chip>
                        </v-col>
                        <v-col v-if="GLOBAL.contentDisplayAddif">
                          <v-btn @click="deleteTask(task_item.contentID)">
                            删除本任务
                          </v-btn>
                        </v-col>
                      </v-row>

                    <v-list-item-subtitle @click="handleTaskClick(task_item)" v-text="task_item.intro"></v-list-item-subtitle>
                  </v-list-item-content>
                </template>
              </v-list-item>

              <v-divider
                v-if="index < task_items_modified.length - 1"
                :key="index"
              ></v-divider>
            </template>
          </v-list-item-group>
        </v-list>
        </div>
        <v-dialog
        v-if="GLOBAL.contentDisplayUser"
        v-model="doTaskDialog"
        max-width="700px"
        >
        <v-card>
            <v-card-title>完成任务</v-card-title>
            <v-divider></v-divider>
            <v-card-text>
              <div style="margin-top: 35px; margin-right: 20px; margin-left: 20px">
                <el-form :model="toFinishTask" class="doTaskForm">
                  <el-form-item :label="renderTaskName(toFinishTask.name)">
                  </el-form-item>
                  <el-form-item :label="renderTaskIntro(toFinishTask.intro)" >
                  </el-form-item>
                  <!-- TODO: 需要改成chip -->
                  <el-form-item :label="renderTaskTag(toFinishTask.tag)" >
                  </el-form-item>
                  <el-form-item :label="renderTaskType(toFinishTask.taskType)">
                  </el-form-item>
                  <el-form-item label="任务文字：" v-if="isDoingTextTask">
                    {{toFinishTask.taskText}}
                  </el-form-item>
                  <el-form-item label="任务文件：" v-if="isDoingFileTask">
                    <v-btn @click="downloadTaskFile"> 下载文件 </v-btn>
                  </el-form-item>
                  <el-form-item label="任务链接：" v-if="isDoingLinkTask">
                    {{toFinishTask.taskLink}}
                  </el-form-item>
                </el-form>
              </div>
            </v-card-text>
            <v-divider></v-divider>
            <v-card-actions>
            <v-btn
                color="blue darken-1"
                text
                @click="resetFinishTask()"
            >
                取消
            </v-btn>
            <v-btn v-if="GLOBAL.contentDisplayUser && !GLOBAL.contentDisplayAddif"
                color="blue darken-1"
                text
                @click="handleFinishTask()"
            >
                完成
            </v-btn>
            </v-card-actions>
        </v-card>
        </v-dialog>
                
      </div>
    </v-card>
</template>

<script>
import COMM from "@/utils/Comm"

export default ({
    name: 'TaskDisplay',
    inject: ['GLOBAL'],
    data() { 
        return {
          search_name: '',

            formInline: { // 输入框（筛选）内容
                learnStatus: '',
                recommendTime: '',
                tag: '',
                classType: '',
            },
            // 筛选栏修改
            learnStatusOptions: [],
            recommendTimeOptions: [],
            tagOptions: [],
            // classTypeOptions: [],

            // tag标签新建
            inputVisible: false,
            inputValue: '',



            task_items: [],
            task_tag_items: ['必修', '限选', '任选'],
            task_recommend_time_items: [],
            task_selected: [], // 选中的任务
            addFromDialog: false,
            addFromList: [],
            taskTag_selected: '',
            toAddTask: {
                name: '',
                intro: '',
                tag: [],
                recommend_time: '',
                is_template: false,
                taskType: '',
                taskText: '',
                taskLink: '',
                taskFile: ''
            },
            audience_options: [{
                label: '面向新人',
                value: 'newcomer'
            }, {
                label: '导师培训',
                value: 'teacher'
            }],
            toFinishTask: {
                name: '',
                intro: '',
                tag: '',
                recommend_time: '',
                is_template: false,
                taskType: '',
                taskText: '',
                taskLink: '',
                taskFile: '',
                contentID: ''
            },
            task_type_options: [{
                label: '文字',
                value: 0
                }, {
                label: '链接',
                value: 1
                }, {
                label: '文件',
                value: 2
            }],
            isTextTask: false,
            isFileTask: false,
            isLinkTask: false,
            isDoingTextTask: false,
            isDoingLinkTask: false,
            isDoingFileTask: false,
            doTaskDialog: false,
            uploadTaskDialog: false,
            rules: {
                name: [
                    { required: true, message: '请输入任务名称', trigger: 'blur' },
                    { min: 3, max: 20, message: '长度在3～20个字符', trigger: 'blur' }
                ],
                recommend_time: [
                    { required: true, message: '请输入推荐用时', trigger: 'blur' },
                ],
                audience: [
                  { required: true, message: '请选择受众', trigger: 'change' }
                ],
                taskType: [
                  { required: true, message: '请选择任务类型', trigger: 'change' }
                ],
                taskText: [
                  { required: true, message: '请输入任务文字', trigger: 'change' }
                ],
                taskLink: [
                  { required: true, message: '请输入任务链接', trigger: 'change' }
                ],
                taskFile: [
                  { required: true, message: '请选择任务文件', trigger: 'change' }
                ],
                isObligatory: [
                  { required: true, message: '请选择课程性质', trigger: 'change' }
                ],    
            },
        }
    },
    props: {
        // valid: {},
        // uploadTaskDialog: {
        //     default: false,
        //     type: Boolean,
        // },
        // closeTaskDialog: {
        //     type: Function,
        //     default: () => {return () => {}}
        // },
        programID: {
            type: String,
            default: ''
        },
        showAudience: {
            type: String,
            required: true,
        },
    },
    watch: {
      programID() {
        this.getTaskList()
      },
      // Au(){
      //   return
      // },
      showAudience() {
          if(this.showAudience === 'newcomer') {
            this.audience_options = [{
              label: '面向新人',
              value: 'newcomer'
            }]
          }
          else if(this.showAudience === 'teacher') {
            this.audience_options = [{
              label: '导师培训',
              value: 'teacher'
            }]
          }
        }
    },
    computed: {
      task_items_modified() {  // 前端筛选后的数据
        if(this.formInline.learnStatus || this.formInline.recommendTime || this.formInline.tag || this.formInline.classType){
          return this.task_items.filter(data => (!this.formInline.learnStatus || this.formInline.learnStatus === "全部") || data.isFinished === (this.formInline.learnStatus === "已完成"))
          .filter(data => (!this.formInline.recommendTime || this.formInline.recommendTime === "全部") || data.recommendTime === this.formInline.recommendTime)
          .filter(data => (!this.formInline.tag || this.formInline.tag === "全部") || data.tag.includes(this.formInline.tag))
          .filter(data => (!this.formInline.classType || this.formInline.classType === "全部") || data.isObligatory === (this.formInline.classType === "必修"))
        }
        else return this.task_items
      },
      addFromList_modified() {  // 前端筛选后的数据
        if(this.search_name){
          return this.addFromList.filter(data => (!this.search_name || data.name.includes(this.search_name)))
        }
        else return this.addFromList
      }
    },
    methods: {

        // 添加标签
      handleClose(tag) {
        this.toAddTask.tag.splice(this.toAddTask.tag.indexOf(tag), 1);
      },

      showInput() {
        this.inputVisible = true;
        this.$nextTick(_ => {
          console.log(_)
          this.$refs.saveTagInput.$refs.input.focus();
        });
      },

      handleInputConfirm() {
        let inputValue = this.inputValue;
        if (inputValue) {
          this.toAddTask.tag.push(inputValue);
          console.log('output tag', this.toAddTask.tag);
        }
        this.inputVisible = false;
        this.inputValue = '';
      },


        changeSelectOptions(){
          /* 
          初始化筛选框
          是否应该优化成watch(tabledata) -> initializeSelectOptions?
          */
          var tableData = this.task_items;
          var learnStatusOptions = [];
          var recommendTimeOptions = [];
          var tagOptions = [];
          // var classTypeOptions = [];
          for(var i = 0; i < tableData.length; i++){
              learnStatusOptions.push(tableData[i].isFinished ? '已完成' : '未完成');
              recommendTimeOptions.push(tableData[i].recommendTime);
              // tagOptions.push(tableData[i].tag);
              if(tableData[i].tag.length === 1 && tableData[i].tag[0] === ''){
                console.log('skip', tableData[i].tag);
              } else {
                tagOptions = tagOptions.concat(tableData[i].tag);
              }
              // classTypeOptions.push(tableData[i].isObligatory ? '必修' : '选修');
          }
          this.learnStatusOptions = Array.from(new Set(learnStatusOptions));
          this.recommendTimeOptions = Array.from(new Set(recommendTimeOptions));
          this.tagOptions = Array.from(new Set(tagOptions));
          // this.classTypeOptions = Array.from(new Set(classTypeOptions));
        },
        isManaging() {
          return this.programID !== ''
        },
        isLearning() {
          return this.programID === ''
        },
        async getTaskList(){
          this.task_items = []
            console.log('get task list')
            // if(this.valid.studyContent) {
            // COMM.my_task_list().then(res => {
            //     this.task_items = res.tasks;
            //     this.task_recommend_time_items = res.task_recommend_time_items;
            //     console.log('task_recommend_time_items', this.task_recommend_time_items)
            //     this.task_tag_items = res.task_tag_items;
            //     console.log('my_task_list: ', res);
            // }, err => {
            //     console.log('my task list error: ', err)
            // })
            // }
            // if(this.valid.addContent){
            // COMM.assignable_task_list().then(res => {
            //     this.task_items = res.tasks;
            //     this.task_recommend_time_items = res.task_recommend_time_items;
            //     console.log('task_recommend_time_items', this.task_recommend_time_items)
            //     this.task_tag_items = res.task_tag_items;
            //     console.log('assignable_task_list: ', res)
            // }, err => {
            //     console.log('assignable task list error', err)
            // })
            // }
            if(this.programID !== '') {
              var res = await COMM.program_content_list(this.programID)
              this.task_items = res.tasks
              console.log('this.task_items', this.task_items)
              this.changeSelectOptions();
              if(this.showAudience !== '') {
                this.task_items = this.task_items.filter(dct => dct.audience === this.showAudience)
                this.changeSelectOptions();
              }
            }
            else {
              var res_else = await COMM.my_task_list()
              this.task_items = res_else.tasks
              this.changeSelectOptions();
              if(this.showAudience !== '') {
                this.task_items = this.task_items.filter(dct => dct.audience === this.showAudience)
                this.changeSelectOptions();
              }
            }
        },
        async checkAddTaskSetTemplateClearance() {
            console.log('check clearance')
            var res = await COMM.getCurRole()
            var role = res.role
            if (role != 'admin') {
            this.toAddTask.is_template = false
            alert('无管理员权限，不能设置模板！')
            }
        },
        renderTaskUploadWidget() {
            switch(this.toAddTask.taskType) {
            case 0: {
                this.isTextTask = true
                this.isLinkTask = false
                this.isFileTask = false
                break
            }
            case 1: {
                this.isTextTask = false
                this.isLinkTask = true
                this.isFileTask = false
                break
            }
            case 2: {
                this.isTextTask = false
                this.isLinkTask = false
                this.isFileTask = true
            }
            }
        },
        async uploadTask(filehook) {
            if(filehook == null && this.isFileTask)
              return
            var file
            if (filehook && this.isFileTask)
                file = filehook.file
            else
                file = null
            console.log('file:', file)
            var uploadForm = new FormData()
            console.log(this.toAddTask)
            uploadForm.append('action', 'CreateContentTemplate')
            uploadForm.append('name', this.toAddTask.name)
            uploadForm.append('intro', this.toAddTask.intro)
            uploadForm.append('tag', this.toAddTask.tag)
            uploadForm.append('recommendTime', this.toAddTask.recommend_time)
            uploadForm.append('type', 'task')
            uploadForm.append('isTemplate', this.toAddTask.is_template)
            uploadForm.append('audience', this.toAddTask.audience)
            uploadForm.append('cover', this.toAddTask.cover)
            uploadForm.append('taskType', this.toAddTask.taskType)
            uploadForm.append('taskType', this.toAddTask.taskType)
            uploadForm.append('isObligatory', this.toAddTask.isObligatory)
            if(this.isTextTask)
                uploadForm.append('taskText', this.toAddTask.taskText)
            else
                uploadForm.append('taskText', '')
            if(this.isLinkTask)
                uploadForm.append('taskLink', this.toAddTask.taskLink)
            else
                uploadForm.append('taskLink', '')
            if(this.isFileTask)
                uploadForm.append('taskFile', file)
            else
                uploadForm.append('taskFile', '')
            console.log('uploadForm:', uploadForm)
            await COMM.upload_task(this.programID, uploadForm)
            this.getTaskList()
        },
        resetTaskForm(formName) {
            this.$refs[formName].resetFields();
            this.toAddTask = {
                name: '',
                intro: '',
                tag: [],
                recommend_time: '',
                taskType: '',
                taskText: '',
                taskLink: '',
                taskFile: '',
                is_template: false
            }
            this.isTextTask = false
            this.isFileTask = false
            this.isLinkTask = false
            this.closeTaskDialog()
        },
          
        taskCommit(formName) {
          console.log('this.toAddTask', this.toAddTask)
          this.$refs[formName].validate((valid) => {
            if (valid) {
              if(this.isFileTask){
                this.$refs.upload_task_file.submit();
              } else {
                this.uploadTask(null);
              }
              this.resetTaskForm('toAddTask');
            } else {
              console.log('error submit!!');
              return false;
            }
          });
          
        },
        taskTag_select(data) {  // TODO: 选择任务标签
            console.log(data)
        },
        async handleTaskClick(task_item) {
            if(this.GLOBAL.contentDisplayUser && !task_item.isFinished) {
              this.toFinishTask.name = task_item.name
              this.toFinishTask.intro = task_item.intro
              this.toFinishTask.tag = task_item.tag
              this.toFinishTask.recommendTime = task_item.recommendTime
              this.toFinishTask.taskType = task_item.taskType
              /*
              遗留问题，到底请求后端哪个地址？
              管理员上传program时候身份的话是program_content_list，但其他身份呢？
              （有看到请求assignable_task_list、my_task_list时候字段又不一样）
              是否要统一（比如后端每个接口返回都统一成text、link、contentID）？
              或者根据父组件的行为（比如现在是新人在查看自己的面板，还是管理员在上传program）来调用不同的url接口并且选赋值字段不一样？
              */
              this.toFinishTask.taskText = task_item.taskText // 原来这里写的是taskText
              this.toFinishTask.taskLink = task_item.taskLink // link？
              this.toFinishTask.contentID = task_item.contentID // contentID？
              console.log('taskType', task_item.taskType)
              if (this.toFinishTask.taskType == 'text') {
                this.isDoingTextTask = true
                this.isDoingLinkTask = false
                this.isDoingFileTask = false
              }
              else if (this.toFinishTask.taskType == 'link') {
                this.isDoingTextTask = false
                this.isDoingLinkTask = true
                this.isDoingFileTask = false
              }
              else {
                this.isDoingTextTask = false
                this.isDoingLinkTask = false
                this.isDoingFileTask = true
              }
              this.doTaskDialog = true
            }
        },
        async downloadTaskFile() {
            var res = await COMM.retrieveTaskFileByID(this.toFinishTask.contentID)
            var filename = res.headers['content-disposition'].split('=')[1]
            res = res.data
            console.log(filename, res)
            let a = document.createElement('a')
            document.body.append(a)
            let url = window.URL.createObjectURL(new Blob([res]))
            a.href = url
            a.download = filename
            a.target = '_blank0'
            a.click()
            a.remove()
            window.URL.revokeObjectURL(url)
        },
        resetFinishTask() {
            this.doTaskDialog = false
            this.toFinishTask.name = ''
            this.toFinishTask.intro = ''
            this.toFinishTask.tag = ''
            this.toFinishTask.recommendTime = ''
            this.toFinishTask.taskType = ''
            this.toFinishTask.taskText = ''
            this.toFinishTask.taskLink = ''
            this.toFinishTask.contentID = ''
        },
        closeTaskDialog() {
          this.uploadTaskDialog = false
        },
        renderTaskName(taskName) {
          console.log("任务名称：" + taskName)
          return "任务名称：" + taskName
        },
        renderTaskIntro(taskIntro) {
          return "任务简介：" + taskIntro
        },
        renderTaskTag(taskTag) {
          return "任务标签：" + taskTag
        },
        renderTaskType(taskType) {
          return "任务类型：" + taskType
        },
        async handleFinishTask() {
          var res = await COMM.finishTask(this.toFinishTask.contentID)
          this.resetFinishTask()
          if (res.result == 'success') {
            alert('已完成任务')
            this.getTaskList()
          }
          else {
            alert('任务状态同步失败，请检查网络连接并稍后重试')
          }
        },
        openAddFromDialog() {
          // COMM.assignable_task_list().then(
          //   response => {
          //     this.addFromList = response.tasks
          //     console.log(this.addFromList)
          //     this.refreshAddFromList()
          //     this.addFromDialog = true
          //   },
          // )
          this.refreshAddFromList()
          this.addFromDialog = true
        },
        addFromToProgram(contentID) {
          COMM.assign_content_to_program(this.programID, contentID).then(
            response => {
              console.log(response)
              this.getTaskList()
              // this.refreshAddFromList()
              this.addFromDialog = false
            }
          )
        },
        async refreshAddFromList() {
          var allContents = await COMM.assignable_task_list()
          allContents = allContents.tasks
          var usedContents = this.task_items
          // usedContents = usedContents.tasks
          var used = {}
          allContents.forEach(content => {
            used[content.contentID] = false
          });
          usedContents.forEach(content => {
            used[content.contentID] = true
          });
          var deduplicatedContents = []
          allContents.forEach(content => {
            if (!used[content.contentID]) {
              deduplicatedContents.push(content)
            }
          })
          this.addFromList = deduplicatedContents
          if(this.showAudience !== '') {
            this.addFromList = this.addFromList.filter(dct => dct.audience === this.showAudience)
          }
        },
        async deleteTask(contentID) {
            await COMM.delete_content_from_program(this.programID, contentID)
            await this.getTaskList()
        },
    },
    created() {
        console.log('taskdisplay', this.valid, this.uploadTaskDialog);
        this.getTaskList();
        console.log('taskItems', this.task_items);
        if(this.showAudience === 'newcomer') {
          this.audience_options = [{
            label: '面向新人',
            value: 'newcomer'
          }]
        }
        else if(this.showAudience === 'teacher') {
          this.audience_options = [{
            label: '导师培训',
            value: 'teacher'
          }]
        }
    }
})
</script>
