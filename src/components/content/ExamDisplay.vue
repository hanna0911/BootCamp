<template>
    <v-card>
      <h2 class="px-4 pt-4 pb-3 font-weight-black" style="margin-bottom: 5px">考试</h2>
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

        <!-- 添加考试弹窗 -->
        <div v-if="GLOBAL.contentDisplayAddif" style="margin: 10px; margin-top: 10px; margin-bottom: 20px">
          <v-dialog
          v-model="uploadTestDialog"
          persistent
          max-width="700px"
          >
          <template v-slot:activator="{ on, attrs }">
              <div align="center">
                <v-btn style="margin: 2px" large v-bind="attrs" v-on="on">
                  <v-icon left medium>mdi-plus</v-icon>新建考试添加
                </v-btn>
                &nbsp;
                <v-btn style="margin: 2px" large @click="openAddFromDialog">
                  <v-icon left medium>mdi-plus</v-icon>从考试库添加
                </v-btn>
                &nbsp;
                <v-btn hidden
                    color="blue darken-1"
                    text
                    @click="downloadTestByID()"
                >
                    下载测试
                </v-btn>
              </div>
          </template>
          <v-card>
              <v-card-title>添加考试</v-card-title>
              <v-divider></v-divider>
              <v-card-text>
                <div style="margin-top: 25px; margin-right: 20px">
                  <el-form :model="toAddTest" :rules="rules" ref="toAddTest" label-width="100px" class="demo-ruleForm">
                  <el-form-item label="考试名称：" prop="name">
                      <el-input v-model="toAddTest.name"></el-input>
                  </el-form-item>
                  <el-form-item label="考试简介：" prop="info">
                      <el-input v-model="toAddTest.intro"></el-input>
                  </el-form-item>
                  <!-- 改成chip -->
                  <el-form-item label="考试标签：" prop="tag">
                      <!-- <el-input v-model="toAddTest.tag"></el-input> -->
                      <el-tag
                        :key="tag"
                        v-for="tag in toAddTest.tag"
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
                    <el-select v-model="toAddTest.isObligatory" placeholder="请选择">
                      <el-option label="必修" :value="true"></el-option>
                      <el-option label="选修" :value="false"></el-option>
                    </el-select>
                  </el-form-item>
                  <el-form-item label="考试时间：" prop="recommend_time">
                      <el-input v-model="toAddTest.recommend_time"
                                type="number"
                                oninput="if(value<0)value =0"
                      ></el-input>
                  </el-form-item>
                  <el-form-item label="受众：" prop="audience">
                    <el-select v-model="toAddTest.audience"  placeholder="请选择">
                      <el-option 
                        v-for="(item, index) in audience_options" 
                        :label="item.label" 
                        :value="item.value" 
                        :key="index"
                      >
                      </el-option>
                    </el-select>
                  </el-form-item>
                  <el-form-item label="是否模板：" prop="info">
                      <el-checkbox v-model="toAddTest.is_template" @change="checkAddTestSetTemplateClearance()">*仅管理员可设置模板</el-checkbox>
                  </el-form-item>
                  <el-form-item prop="test">
                    <el-upload
                      ref="upload_test"
                      class="upload-demo"
                      drag
                      :http-request="uploadTest"
                      accept=".csv"
                      action=""
                      :auto-upload="false"
                      :show-file-list="true"
                      :on-success="handleTestFileSuccess"
                    >
                      <i class="el-icon-upload"></i>
                      <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                      <div style="margin-top: -15px; margin-bottom: -35px;" class="el-upload__tip" slot="tip">只能上传csv文件</div>
                    </el-upload>
                  </el-form-item>
                  </el-form>
                </div>
              </v-card-text>
              <v-divider></v-divider>
              <v-card-actions>
              <v-btn
                  color="blue darken-1"
                  text
                  @click="resetTestForm('toAddTest')"
              >
                  取消
              </v-btn>
              <v-btn
                  color="blue darken-1"
                  text
                  @click="testCommit('toAddTest')"
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
                <v-toolbar-title>从考试库添加</v-toolbar-title>
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

        <!-- 考试清单 -->
        <v-dialog
          v-model="showExamDialog"
          fullscreen
          hide-overlay
          transition="dialog-bottom-transition"
        >
        <template v-slot:activator="{ on, attrs }">
          <v-list two-line style="margin-top: -20px">
            <v-list-item-group v-bind="attrs" v-on="on">
              <template v-for="(test_item, index) in test_items_modified">
                <v-list-item :key="test_item.contentID">
                  <!-- 考试内容 -->
                  <v-list-item-content>
                    <v-list-item-title
                      class="font-weight-black" 
                      v-text="test_item.name"/>

                    <v-row>
                      <!-- 建议时间 -->
                      <v-col>
                        <!-- 管理员权限 -->
                        <v-select
                          v-if="false"
                          v-model="test_item.recommendTime"
                          :items="test_recommend_time_items"
                          chips
                          label="建议时间"
                          placeholder="添加标签"
                          single-line
                          small-chips
                          dense
                        ></v-select>
                        <!-- 新人、导师权限 -->
                        <v-chip v-else style="margin-top: 5px; margin-bottom: 15px">{{ test_item.recommendTime + "分钟" }}</v-chip>
                      </v-col>

                      <!-- 标签tag：成列表展示 -->
                      <v-col>
                        <v-list-item-subtitle
                            style="margin-top: 5px; margin-bottom: 15px"
                            class="text--primary"
                          >
                            <span v-for="(tag, tag_id) in test_item.tag" :key="tag_id">
                            <v-chip v-if="tag !== ''">{{tag}}</v-chip>&nbsp;</span>
                        </v-list-item-subtitle>
                      </v-col>

                      <!-- 必修选修tag -->
                      <v-col>
                        <v-list-item-subtitle
                            style="margin-top: 5px; margin-bottom: 15px"
                            class="text--primary"
                          >
                            <v-chip>{{test_item.isObligatory ? '必修' : '选修'}}</v-chip>
                        </v-list-item-subtitle>
                      </v-col>
                      <!-- 学习状态tag -->
                      <v-col v-if="GLOBAL.contentDisplayUser">
                        <v-combobox
                          v-if="false"
                          v-model="test_item.tag"
                          :items="test_tag_items"
                          chips
                          label="添加标签"
                          placeholder="添加标签"
                          small-chips
                          dense
                          single-line
                        >
                          <template v-slot:selection="{ attrs, item, testTag_select, testTag_selected }">
                            <v-chip
                              v-bind="attrs"
                              :input-value="testTag_selected"
                              @click="testTag_select"
                              small
                            >{{ item }}
                            </v-chip>
                          </template>
                        </v-combobox>
                        <v-chip style="margin-top: 5px; margin-bottom: 15px" v-else>{{ test_item.isFinished ? '已完成':'未完成' }}</v-chip>
                      </v-col>

                      <v-col>
                        <v-chip v-if='GLOBAL.contentDisplayUser && test_item.isFinished' style="margin-top: 10px; margin-bottom: 5px">{{ test_item.score + '分 / 100 分' }}</v-chip>
                      </v-col>

                      <v-col v-if="GLOBAL.contentDisplayAddif">
                        <v-btn @click="deleteTest(test_item.contentID)">
                          删除本考试
                        </v-btn>
                      </v-col>
                    </v-row>

                    <v-list-item-subtitle
                      class="font-weight-black" 
                      v-text="test_item.intro">
                    </v-list-item-subtitle>
                    <!-- 临时按钮 -->
                    <v-btn v-if='GLOBAL.contentDisplayUser && !GLOBAL.contentDisplayAddif && !test_item.isFinished' large v-bind="attrs" v-on="on" @click="showExamFunc(test_item.contentID)">
                      显示考试
                    </v-btn>
              <v-divider
                v-if="index < test_items_modified.length - 1"
                :key="index"
              ></v-divider>
                  </v-list-item-content>
                </v-list-item>
              </template>
            </v-list-item-group>
          </v-list>

        </template>
        <!-- 答题界面 -->
        <v-card>
          <v-toolbar
            dark
            color="primary"
          >
            <v-btn
              icon
              dark
              @click="showExamDialog = false"
            >
              <v-icon>mdi-close</v-icon>
            </v-btn>
            <v-toolbar-title>  </v-toolbar-title>
            <v-spacer></v-spacer>
            <v-toolbar-items v-if='false'>
              <v-btn
                dark
                text
                @click="showExamDialog = false"
              >
                存档
              </v-btn>
            </v-toolbar-items>
          </v-toolbar>
          <test-list :testItem="test_item" :contentID="showExamContentID"/>
        </v-card>
        </v-dialog>
      </div>
    </v-card>
</template>

<script>
import TestList from '../subcomponents/TestList.vue'
import COMM from "@/utils/Comm"
var testDownloadTestID = "testDownloadTestID"

export default ({
    name: 'ExamDisplay',
    inject: ['GLOBAL'],
    components: {
        TestList,
    },
    data() { 
        return {
            search_name: '', 

            // tag标签新建
            inputVisible: false,
            inputValue: '',
          
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


            // 输入框规则
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
                isObligatory: [
                  { required: true, message: '请选择课程性质', trigger: 'change' }
                ],            
              },

            // 显示考试列表
            test_items: [],
            test_tag_items: ['必修', '限选', '任选'],
            testTag_selected: '', 
            test_recommend_time_items: [],
            addFromDialog: false,
            addFromList: [],

            // 添加考试
            toAddTest: {
              /*
                name: 'TEST', 
                intro: 'hahaha', 
                tag: 'tag1 tag2 tag3', // TODO：需要改成list而不是string
                recommend_time: 120, //
                is_template: false,
                audience: 'newcomer',
                cover: 'NOT_A_REAL_BMP',
                csv: 'NOT_A_REAL_CSV',
              */
                name: '', 
                intro: '', 
                tag: [], // TODO：需要改成list而不是string
                recommend_time: '', //
                is_template: false,
                audience: '',
                cover: 'NOT_A_REAL_BMP',
                csv: 'NOT_A_REAL_CSV',

            },
            audience_options: [{
              label: '面向新人',
              value: 'newcomer'
            }, {
              label: '导师培训',
              value: 'teacher'
            }],
            uploadTestDialog: false,
            // 用来显示TestList的
            showExamDialog: false,
            showExamContentID: "",
        }
    },
    computed: {
      test_items_modified() {  // 前端筛选后的数据
        if(this.formInline.learnStatus || this.formInline.recommendTime || this.formInline.tag || this.formInline.classType){
          return this.test_items.filter(data => (!this.formInline.learnStatus || this.formInline.learnStatus === "全部") || data.isFinished === (this.formInline.learnStatus === "已完成"))
          .filter(data => (!this.formInline.recommendTime || this.formInline.recommendTime === "全部") || data.recommendTime === this.formInline.recommendTime)
          .filter(data => (!this.formInline.tag || this.formInline.tag === "全部") || data.tag.includes(this.formInline.tag))
          .filter(data => (!this.formInline.classType || this.formInline.classType === "全部") || data.isObligatory === (this.formInline.classType === "必修"))
        }
        else return this.test_items
      },
      addFromList_modified() {  // 前端筛选后的数据
        if(this.search_name){
          return this.addFromList.filter(data => (!this.search_name || data.name.includes(this.search_name)))
        }
        else return this.addFromList
      }
    },
    props: {
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
        this.getTestList()
      },
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
    methods: {
  // 添加标签
      handleClose(tag) {
        this.toAddTest.tag.splice(this.toAddTest.tag.indexOf(tag), 1);
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
          this.toAddTest.tag.push(inputValue);
          console.log('output tag', this.toAddTest.tag);
        }
        this.inputVisible = false;
        this.inputValue = '';
      },

        changeSelectOptions(){
          /* 
          初始化筛选框
          是否应该优化成watch(tabledata) -> initializeSelectOptions?
          */
          var tableData = this.test_items;
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
        async getTestList(){
            console.log('获取test_list')
            // if(this.valid.studyContent){
            // COMM.my_test_list().then(res => {
            //     console.log("my_test_list success: ", res)
            //     this.test_items = res.tests;
            //     this.test_recommend_time_items = res.test_recommend_time_items;
            //     this.test_tag_items = res.test_tag_items;
            // }, err => {
            //     console.log("my_test_list error: ", err)
            // })
            // }
            // if(this.valid.addContent){
            // COMM.assignable_test_list().then(res =>{
            //     console.log("assignable_test_list success: ", res);
            //     this.test_items = res.tests;
            //     this.test_recommend_time_items = res.test_recommend_time_items;
            //     this.test_tag_items = res.test_tag_items;
            // }, err => {
            //     console.log("assignable_test_list error: ", err)
            // })
            // }
            if(this.programID !== '') {
              var res = await COMM.program_content_list(this.programID)
              this.test_items = res.tests
              this.changeSelectOptions();
              if(this.showAudience !== '') {
                this.test_items = this.test_items.filter(dct => dct.audience === this.showAudience)
                this.changeSelectOptions();
              }
            }
            else {
              var res_else = await COMM.my_test_list()
              this.test_items = res_else.tests
              this.changeSelectOptions();
              if(this.showAudience !== '') {
                this.test_items = this.test_items.filter(dct => dct.audience === this.showAudience)
                this.changeSelectOptions();
              }
            }
            console.log("get exams:", this.test_items)
        },
        downloadTestByID() {
            var info = COMM.downloadTestInfoByID(testDownloadTestID)
            var paper = COMM.downloadTestPaperByID(testDownloadTestID)
            console.log(info)
            console.log(paper)
        },
        resetTestForm(formName){  // 取消：重置表单输入
            this.$refs[formName].resetFields();
            console.log('reset', formName)
            this.toAddTest = {
                name: '', 
                intro: '', 
                tag: [], // TODO：需要改成list而不是string
                recommend_time: '', //
                is_template: false,
                audience: '',
                cover: 'NOT_A_REAL_BMP',
                csv: 'NOT_A_REAL_CSV',
            }
            this.$refs.upload_test.clearFiles()
            this.closeTestDialog();
        },
        async uploadTest(form){
            // 判断考试名字是否合法
            // formName.validate((valid) => {
            //   if (valid) {
            console.log(this.$refs[form])
            // TODO: COMM.admin_create_content_template()
            if (this.toAddTest.name == "" || this.toAddTest.audience == "" || form.file == null) {
                alert("考试名称、考试受众和考题文件是必填项！")
                this.$refs.upload_test.clearFiles()
                return
            }
            var uploadForm = new FormData()
            uploadForm.append('action', 'CreateContentTemplate')
            uploadForm.append('name', this.toAddTest.name)
            uploadForm.append('intro', this.toAddTest.intro)
            uploadForm.append('tag', this.toAddTest.tag)
            // uploadForm.append('tag', [])
            uploadForm.append('recommendTime', this.toAddTest.recommend_time)
            uploadForm.append('audience', this.toAddTest.audience)
            uploadForm.append('cover', this.toAddTest.cover)
            uploadForm.append('csv', form.file)
            uploadForm.append('isTemplate', this.toAddTest.is_template)
            uploadForm.append('isObligatory', this.toAddTest.isObligatory)
            await COMM.upload_test(this.programID, uploadForm)
            // alert('submit!');
            this.getTestList()
            this.closeTestDialog(); // 回调函数
            //   } else {
            //     console.log('error submit!!');
            //     return false;
            //   } 
            // });
        },
        handleTestFileSuccess(response, file, fileList) {
            this.$refs.upload_test.clearFiles()
            console.log(response)
            console.log(file)
            console.log(fileList)
        },
        testCommit(formName){
          this.$refs[formName].validate((valid) => {
            if (valid) {
              this.$refs.upload_test.submit();
              this.resetTestForm('toAddTest');
              this.closeTestDialog();
              this.getTestList();
            } else {
              console.log('error submit!!');
              return false;
            }
          });
        },
        testTag_select(data) {  // TODO: 选择考试标签
            console.log(data)
        },
        async checkAddTestSetTemplateClearance() {
            console.log('check clearance')
            var res = await COMM.getCurRole()
            var role = res.role
            if (role != 'admin') {
            this.toAddTest.is_template = false
            alert('无管理员权限，不能设置模板！')
            }
        },
        closeTestDialog() {
          this.uploadTestDialog = false
        },
        showExamFunc(contentID) {
          this.showExamContentID = contentID
          this.showExamDialog = true
        },
        openAddFromDialog() {
          // COMM.assignable_test_list().then(
          //   response => {
          //     this.addFromList = response.tests
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
              this.getTestList()
              this.addFromDialog = false
              // this.refreshAddFromList()
            }
          )
        },
        async refreshAddFromList() {
          var allContents = await COMM.assignable_test_list()
          allContents = allContents.tests
          var usedContents = this.test_items
          // usedContents = usedContents.tests
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
        async deleteTest(contentID) {
            await COMM.delete_content_from_program(this.programID, contentID)
            await this.getTestList()
        },
    },
    created() {
        this.getTestList();
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
