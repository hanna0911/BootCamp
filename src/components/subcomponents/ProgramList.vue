<template>
<v-container>
<v-col cols="12">
<v-card>
  <h2 class="px-4 pt-4 pb-3 font-weight-black" style="margin-bottom: -20px">模板列表</h2>
  <div style="margin: 2%">

    <!-- 添加模板 -->
    <div v-if="displayType === 'teacherEdit' || displayType === 'adminEdit'" style="margin: 10px; margin-top: 30px; margin-bottom: 20px">
      <v-dialog
        v-model="addNewDialog"
      >
        <!-- 添加模板按钮 -->
        <template v-slot:activator="{ on, attrs }">
          <v-btn block large v-bind="attrs" v-on="on" @click="addNewDialog = true">
            <v-icon left medium>mdi-plus</v-icon>
            添加模板
          </v-btn>
        </template>

        <!-- 添加模板界面 -->
        <v-card>
          <v-card-title>添加模板</v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <div style="margin-top: 35px; margin-right: 20px">
              <el-form :model="newProgramInput" :rules="rules" label-width="100px" class="demo-ruleForm">
              <el-form-item label="模板名称："  required>
                  <el-input v-model="newProgramInput.name"></el-input>
              </el-form-item>
              <el-form-item label="模板简介：" >
                  <el-input v-model="newProgramInput.intro"></el-input>
              </el-form-item>
              <!-- TODO: 需要改成chip -->
              <el-form-item label="模板标签：" >
                  <el-input v-model="newProgramInput.tag"></el-input>
              </el-form-item>
              <el-form-item label="推荐用时：" required>
                  <el-input v-model="newProgramInput.recommendTime"
                            type="number"
                            oninput="if(value<0)value =0"
                  ></el-input>
              </el-form-item>
              <el-form-item label="受众：" required>
                  <el-select v-model="newProgramInput.audience"  placeholder="请选择" >
                    <el-option 
                      v-for="(item, index) in audience_options" 
                      :label="item.label" 
                      :value="item.value" 
                      :key="index">
                    </el-option>
                  </el-select>
              </el-form-item>
              </el-form>
            </div>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
          <v-btn
              color="blue darken-1"
              text
              @click="addNewDialog = false"
          >
              取消
          </v-btn>
          <v-btn
              color="blue darken-1"
              text
              @click="addNewTemplate(), addNewDialog = false"
          >
              上传
          </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
    
    <!-- 模板列表 -->
    <v-dialog
      v-model="contentDialog"
      width=1500
    >
    <template v-slot:activator="{ on, attrs }">
    <v-list two-line style="margin-top: -20px">
      <v-list-item-group>
      <template v-for="templat of templates">
        <v-list-item :key="templat.name">
        <!-- 课程显示弹窗 -->
            <v-list-item-content>
              <v-row style="margin-top: -5px; margin-bottom: -15px">
                <v-col cols="8">
                <v-list-item-title v-bind="attrs" v-on="on" class="font-weight-black" v-text="templat.name"></v-list-item-title>
                <v-list-item-subtitle v-bind="attrs" v-on="on" v-text="'作者：' + templat.author"></v-list-item-subtitle>
                </v-col>
                <v-col cols="2">
                <v-btn v-if="displayType === 'assign'" style="margin-right: 5px" large @click="assignProgram(templat.programID)">
                  分配项目
                </v-btn>
                </v-col>
                <v-col cols="2">
                <v-btn style="margin-right: 5px" large v-bind="attrs" v-on="on" @click="showContentDisplay(templat)">
                  {{(displayType === 'adminEdit' || (displayType === 'teacherEdit' && templat.isTemplate === false)) ?
                  '查看/修改模板' : '查看模板'}}
                </v-btn>
                </v-col>
              </v-row>
              <!-- 管理员权限 -->
              <v-row style="margin-top: -5px; margin-bottom: -15px">
                <!-- 推荐学习时间 -->
                <v-col cols="12" lg="3" md="4" sm="6">
                  <v-list-item-subtitle
                    style="margin-top: 5px; margin-bottom: 15px"
                    class="text--primary"
                  >
                    <v-chip>{{templat.recommendTime + "小时"}}
                    </v-chip>
                  </v-list-item-subtitle>
                </v-col>
                <!-- 面向新人/导师 -->
                <v-col cols="12" lg="3" md="4" sm="6">
                  <v-list-item-subtitle
                      style="margin-top: 5px; margin-bottom: 15px"
                      class="text--primary"
                    >
                      <v-chip>{{templat.audience === "newcomer" ? "新人培训" : "导师培训"}}</v-chip>
                  </v-list-item-subtitle>
                </v-col>
                <!-- 是否是（管理员）模板 -->
                <v-col v-if="displayType !== 'adminEdit'" cols="12" lg="3" md="4" sm="6">
                  <v-list-item-subtitle
                      style="margin-top: 5px; margin-bottom: 15px"
                      class="text--primary"
                    >
                      <v-chip>{{templat.isTemplate ? "管理员模板" : "个性化模板"}}</v-chip>
                  </v-list-item-subtitle>
                </v-col>
              </v-row>
              <v-list-item-subtitle v-bind="attrs" v-on="on" v-text="templat.intro"></v-list-item-subtitle>
            </v-list-item-content>
        </v-list-item>
      </template>
      </v-list-item-group>
    </v-list>
    </template>

    <v-card>
    <v-card-actions>
      <v-btn color="blue darken-1" text @click="contentDialog = false">
        返回
      </v-btn>
    </v-card-actions>
    <ContentDisplay :programID="showProgramID" :showAudience="showAudience === ''? showProgramAudience : showAudience"/>
    </v-card>
    </v-dialog>
  </div>
</v-card>
</v-col>
</v-container>
</template>


<script>
import COMM from "@/utils/Comm"
import ContentDisplay from '../content/ContentDisplay.vue'

export default ({
    name: 'ProgramList',
    inject: ['GLOBAL'],
    components: {
        ContentDisplay,
    },
    data() {
        return {
          addNewDialog: false,
          newProgramInput: {
            name: "",
            intro: "",
            tag: "",
            recommendTime: "",
            audience: "",
            cover: "",
          },
          audience_options: [{
            label: '新人培训',
            value: 'newcomer'
          }, {
            label: '导师培训',
            value: 'teacher'
          }],
          rules: {
            name: [
                { required: true, message: '请输入课程名称', trigger: 'blur' },
                { min: 3, max: 20, message: '长度在3～20个字符', trigger: 'blur' }
            ],
          },
          templates: {},
          showProgramID: "",
          showProgramAudience: "",
          contentDialog: false,
        };
    },
    props: {
      displayType: {  // teacherEdit, adminEdit, assign
        type: String,
        required: true,
      },
      assignProgram: {
        type: Function,
        default: () => {
          return () => {}
        }
      },
      showAudience: {
          type: String,
          required: true,
      },
    },
    methods: {
      addNewTemplate() {
        COMM.create_template_program(
          this.newProgramInput.name,
          this.newProgramInput.intro,
          this.newProgramInput.tag,
          this.newProgramInput.recommendTime,
          this.newProgramInput.audience,
          this.newProgramInput.cover,
          this.displayType === "adminEdit")
        .then(
          response => {
            console.log(response.programID)
            this.getTemplateList()
          },
          error => {
            console.log(error)
          }
        )
      },
      getTemplateList() {
        if(this.displayType === "adminEdit"){
          COMM.program_template_list().then(
            response => {
              this.templates = response.program_templates
              console.log(this.templates)
              if(this.showAudience !== '') {
                this.templates = this.templates.filter(dct => dct["audience"] === this.showAudience)
              }
            },
            error => {
              console.log(error)
            }
          )
        }
        else {
          COMM.assignable_program_list().then(
            response => {
              this.templates = response.program_templates
              console.log(this.templates)
              if(this.showAudience !== '') {
                this.templates = this.templates.filter(dct => dct["audience"] === this.showAudience)
              }
            },
            error => {
              console.log(error)
            }
          )
        }
      },
      showContentDisplay(templat) {
        this.showProgramID = templat.programID
        this.showProgramAudience = templat.audience
        this.GLOBAL.contentDisplayAddif = (this.displayType === 'adminEdit' || (this.displayType === 'teacherEdit' && templat.isTemplate === false))
        this.GLOBAL.contentDisplayUser = false
        this.contentDialog = true
      },
    },
    created() {
        this.getTemplateList()
    }
})
</script>
