<template>
    <v-card>
      <h2 class="px-4 pt-4 pb-3 font-weight-black">课程清单</h2>
<!--      临时添加  -->
<!--      <v-btn @click="this.finish_all"></v-btn>-->
      <v-spacer></v-spacer>

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

      <div style="margin: 2%">
        <v-row v-if="GLOBAL.contentDisplayAddif">
          <v-col>
            <v-btn block large @click="openClassDialog()">
              <v-icon left medium>mdi-plus</v-icon>
              新建课程添加
            </v-btn>
          </v-col>
          <v-col>
            <v-btn block large @click="openAddFromDialog()" style="margin-bottom: 5px" >
              <v-icon left medium>mdi-plus</v-icon>
              从课程库添加
            </v-btn>
          </v-col>
        </v-row>
        <!-- 添加课程弹窗 -->
        <div v-if="GLOBAL.contentDisplayAddif" style="margin: 10px; margin-top: 30px; margin-bottom: 20px">
          <v-dialog
            v-model="courseDialog"
            max-width="800px"
            min-width="600px"
          >
            <!-- 添加课程按钮 -->
            <!-- 添加课程界面 -->
            <v-card>
              <!-- <v-toolbar dark color="primary">
                <v-btn icon dark @click="closeClassDialog()">
                  <v-icon>mdi-close</v-icon>
                </v-btn>
                <v-toolbar-title>新建课程添加</v-toolbar-title>
                <v-spacer></v-spacer>
              </v-toolbar> -->
              <v-card-title>新建课程添加</v-card-title>
              <v-divider></v-divider>

              <!-- 添加课程内置界面 -->
              <v-card-text>
                <div style="margin-top: 35px; margin-right: 20px">
                  <el-form :model="toAddClass" :rules="rules" ref="toAddClass" label-width="100px">
                  <el-form-item label="课程名称：" prop="name">
                      <el-input v-model="toAddClass.name"></el-input>
                  </el-form-item>
                  <el-form-item label="课程简介：" prop="info">
                      <el-input v-model="toAddClass.intro"></el-input>
                  </el-form-item>
                  <!-- TODO: 需要改成chip -->
                  <el-form-item label="课程标签：" prop="tag">
                      <!-- <el-input v-model="toAddClass.tag"></el-input> -->
                      <el-tag
                        :key="tag"
                        v-for="tag in toAddClass.tag"
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
                    <!-- <el-select v-model="audience_value" placeholder="请选择" v-bind="toAddClass.audience"> -->
                    <el-select v-model="toAddClass.isObligatory" placeholder="请选择">
                      <el-option label="必修" :value="true"></el-option>
                      <el-option label="选修" :value="false"></el-option>
                    </el-select>
                  </el-form-item>
                  <el-form-item label="推荐用时：" prop="recommendTime">
                      <el-input v-model="toAddClass.recommendTime"
                                type="number"
                                oninput="if(value<0)value =0"
                      ></el-input>
                  </el-form-item>
                  <el-form-item label="受众：" prop="audience">
                    <!-- <el-select v-model="audience_value" placeholder="请选择" v-bind="toAddClass.audience"> -->
                    <el-select v-model="toAddClass.audience" placeholder="请选择">
                      <el-option 
                        v-for="(item, index) in audience_options" 
                        :label="item.label" 
                        :value="item.value" 
                        :key="index"
                      >
                      </el-option>
                    </el-select>
                  </el-form-item>
                  <el-form-item label="是否模板：" prop="info" v-if="this.GLOBAL.ident==='admin'">
                      <el-checkbox v-model="toAddClass.isTemplate" @change="checkSetAddClassTemplateClearance()">*仅管理员可设置模板</el-checkbox>
                  </el-form-item>
                  </el-form>
                </div>
                <v-list three-line>
                  <template v-for="(item, index) in lesson_items">
                    <v-subheader
                      v-if="item.header"
                      :key="item.header"
                      v-text="item.header"
                    ></v-subheader>

                    <v-divider
                      v-else-if="item.divider"
                      :key="index"
                      :inset="item.inset"
                    ></v-divider>

                    <v-list-item
                      v-else
                      :key="item.title"
                    >
                      <v-list-item-content>
                          <v-list-item-title v-html="genName(item.name, index)"></v-list-item-title>
                          <v-list-item-subtitle v-html="item.intro"></v-list-item-subtitle>
                      </v-list-item-content>
                      <v-list-item-action>
                          <v-toolbar dark color="primary">
                            <v-btn icon dark @click="editLesson(index)">
                              <v-icon medium>mdi-wrench</v-icon>
                                
                            </v-btn>
                            <v-btn icon dark @click="deleteLesson(index)">
                              <v-icon medium>mdi-close</v-icon>
                                
                            </v-btn>
                          </v-toolbar>
                      </v-list-item-action>
                    </v-list-item>
                  </template>
                </v-list>
                <!-- 上传每一讲的课件弹窗，TODO（现在只有一讲） -->
                <div v-if="GLOBAL.contentDisplayAddif" style="margin: 10px; margin-top: 30px; margin-bottom: 20px">
                  <v-row
                    align="center"
                    justify="space-around"
                  >
                    <v-btn large @click="postClassInfo('toAddClass')">
                      <v-icon left medium>mdi-plus</v-icon>
                      上传下一讲
                    </v-btn>
                  </v-row>
                  <v-dialog
                    v-model="uploadLessonDialog"
                    persistent
                    max-width="700px"
                  >
                  <!-- <template v-slot:activator="{ on, attrs }">
                      <v-btn large v-bind="attrs" v-on="on" @click="postClassInfo('toAddClass')">
                        <v-icon left medium>mdi-plus</v-icon>
                        上传下一讲
                      </v-btn>
                  </template> -->

                  <!-- 添加lesson -->
                  <v-card>
                      <v-card-title>本讲内容</v-card-title>
                      <v-divider></v-divider>
                      <v-card-text style="height: 500px;">
                        <div style="margin-top: 25px; margin-right: 20px">
                          <el-form :model="toAddLesson" :rules="lesson_rules" ref="toAddLesson" label-width="100px">
                            <el-form-item label="本讲标题：" prop="name">
                                <el-input v-model="toAddLesson.name"></el-input>
                            </el-form-item>
                            <el-form-item label="内容简介：" prop="info">
                                <el-input v-model="toAddLesson.intro"></el-input>
                            </el-form-item>
                            <el-form-item label="推荐用时：" prop="recommendTime">
                                <el-input v-model="toAddLesson.recommendTime"
                                          type="number"
                                          oninput="if(value<0)value =0"
                                ></el-input>
                            </el-form-item>
                            <el-form-item>
                              <!-- 这里是上传的action，不太清楚elementUI的操作，可以查一下 -->
                              <el-upload
                                ref="upload_lesson"
                                class="upload-demo"
                                drag
                                multiple
                                :http-request="cacheLessonData"
                                :auto-upload="false"
                                :file-list="lesson_file_list"
                                action=""
                                >
                                <i class="el-icon-upload"></i>
                                <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                                <div style="margin-top: -15px" class="el-upload__tip" slot="tip">只能上传视频（mp4/flv/mov文件）与课件（ppt/pptx/key/pdf文件）</div>
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
                          @click="resetLessonForm('ruleForm')"
                      >
                          取消
                      </v-btn>
                      <v-btn
                          color="blue darken-1"
                          text
                          @click="cacheLesson('ruleForm')"
                      >
                          上传
                      </v-btn>
                      </v-card-actions>
                  </v-card>
                  </v-dialog>
                </div>
              </v-card-text>
              <v-divider></v-divider>
              <v-card-actions>
              <v-btn
                  color="blue darken-1"
                  text
                  @click="closeClassDialog()"
              >
                  取消
              </v-btn>
              <v-btn
                  :disabled="lesson_items.length === 0"
                  color="blue darken-1"
                  text
                  @click="uploadClass('ruleForm')"
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
                <v-toolbar-title>从课程库添加</v-toolbar-title>
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
                <!-- <template v-for="item in addFromList"> -->
                <template v-for="item in addFromList_modified">
                <v-list-item :key="item.name">
                  <v-list-item-content>
                      <v-list-item-title class="font-weight-black" v-text="item.name"></v-list-item-title>
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
                      <v-list-item-subtitle v-text="item.intro"></v-list-item-subtitle>
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
        
        <!-- 课程清单 -->
        <v-list two-line style="margin-top: -15px">
          <v-list-item-group>
            <!-- <template v-for="class_item in class_items"> -->
            <template v-for="class_item in class_items_modified">
              <v-list-item :key="class_item.name">
  
                <!-- 课程显示弹窗 -->
                <v-dialog
                  v-model="class_item.courseDialog"
                  fullscreen
                  hide-overlay
                  transition="dialog-bottom-transition"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-list-item-content>
                      <v-list-item-title v-bind="attrs" v-on="on" class="font-weight-black" v-text="class_item.name"></v-list-item-title>
                      <!-- <v-select
                        v-model="class_tag_value"
                        :items="class_tag_items"
                        chips
                        label="请选择"
                        solo
                        dense
                        width="10"
                      ></v-select> -->

                      <!-- 管理员权限 -->
                      <v-row style="margin-top: -5px; margin-bottom: -15px">
                        <!-- 推荐学习时间 -->
                        <v-col v-bind="attrs" v-on="on">
                          <v-list-item-subtitle
                            v-if="true"
                            style="margin-top: 5px; margin-bottom: 15px"
                            class="text--primary"
                          >
                            <v-chip>{{class_item.recommendTime}}小时
                            </v-chip>
                          </v-list-item-subtitle>
                          <v-select
                            v-else-if="GLOBAL.contentDisplayAddif"
                            v-model="class_item.recommendTime"
                            :items="dayItems"
                            chips
                            label="标签"
                            placeholder="添加标签"
                            single-line
                            small-chips
                            dense
                          ></v-select>
                        </v-col>

                        <!-- 标签tag：成列表展示 -->
                        <v-col v-bind="attrs" v-on="on">
                          <v-list-item-subtitle
                              style="margin-top: 5px; margin-bottom: 15px"
                              class="text--primary"
                            >
                              <span v-for="(tag, tag_id) in class_item.tag" :key="tag_id">
                              <v-chip v-if="tag !== ''">{{tag}}</v-chip>&nbsp;</span>
                          </v-list-item-subtitle>
                        </v-col>
                        <!-- 必修选修tag -->
                        <v-col v-bind="attrs" v-on="on">
                          <v-list-item-subtitle
                              style="margin-top: 5px; margin-bottom: 15px"
                              class="text--primary"
                            >
                              <v-chip>{{class_item.isObligatory ? '必修' : '选修'}}</v-chip>
                          </v-list-item-subtitle>
                        </v-col>
                        <!-- 学习状态tag -->
                        <v-col v-bind="attrs" v-on="on" v-if="GLOBAL.contentDisplayUser">
                          <v-list-item-subtitle
                              style="margin-top: 5px; margin-bottom: 15px"
                              class="text--primary"
                            >
                              <v-chip>{{class_item.isFinished ? '已完成': '未完成'}}</v-chip>
                          </v-list-item-subtitle>
                          <!-- <v-select
                            v-else-if="GLOBAL.contentDisplayAddif"
                            v-model="class_item.tag"
                            :items="class_tag_items"
                            chips
                            label="标签"
                            placeholder="添加标签"
                            single-line
                            small-chips
                            dense
                          ></v-select> -->
                        </v-col>
                        <v-col v-if="GLOBAL.contentDisplayAddif">
                          <v-btn @click="deleteCourse(class_item.contentID)">
                            删除本课
                          </v-btn>
                        </v-col>
                      </v-row>

                      <v-list-item-subtitle v-bind="attrs" v-on="on" v-text="class_item.intro"></v-list-item-subtitle>
                      
                      <!-- 进度条 -->
                      <v-row v-bind="attrs" v-on="on">
                        <v-col cols=10>
                          <v-progress-linear v-if="GLOBAL.contentDisplayUser" style="margin-top: 10px" :value="class_item.finishedLessonCount/class_item.lessonCount*100"></v-progress-linear>
                        </v-col>
                        <v-col cosl=2>
                          <v-list-item-action v-if="GLOBAL.contentDisplayUser" style="margin-top: 5px">
                            <v-list-item-action-text>{{class_item.finishedLessonCount}}/{{class_item.lessonCount}} 讲</v-list-item-action-text>
                          </v-list-item-action>
                        </v-col>
                      </v-row>
                    </v-list-item-content>
                  </template>

                  <v-card>
                    <v-toolbar
                      dark
                      color="primary"
                    >
                      <v-btn
                        icon
                        dark
                        @click="class_item.courseDialog = false"
                      >
                        <v-icon>mdi-close</v-icon>
                      </v-btn>
                      <v-toolbar-title> {{class_item.name}} </v-toolbar-title>
                      <v-spacer></v-spacer>
                      <!--<v-toolbar-items>
                        <v-btn
                          dark
                          text
                          @click="class_item.courseDialog = false"
                        >
                          存档
                        </v-btn>
                      </v-toolbar-items>-->
                    </v-toolbar>
                    <!--<div style="margin-left: 17%">
                        <iframe id="iframe1" width="960" height="720" frameborder='no' border='0' marginwidth='0' marginheight='0' scrolling='no' allowtransparency='yes'
                        :src="'https://view.officeapps.live.com/op/view.aspx?src=' + class_item.courseLink"></iframe>
                    </div>-->
                    <CourseStudy :contentID="class_item.contentID"/>
                  </v-card>
                </v-dialog>
              </v-list-item>
              
              <!-- <v-list-item style="margin: -20px" :key="class_item.name">
                  <v-progress-linear value="15"></v-progress-linear>
              </v-list-item> -->

            </template>
          </v-list-item-group>
        </v-list>
                
      </div>
    </v-card>
</template>

<script>
import COMM from "@/utils/Comm"
import CourseStudy from "./CourseStudy.vue"

export default ({
    name: 'CourseDisplay',
    inject: ['GLOBAL'],
    components: {
      CourseStudy,
    },
    data() { 
        return {
            search_name: '', //搜索

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


            // 显示课程清单
            class_items: [
              // {
              //   name: '微积分',
              //   intro: '小学一年级课程',
              //   tag: '必修',
              //   recommendTime: 'Day 3',
              //   audience: '',
              //   cover: '',
              //   content_type: '',
              //   isTemplate: '',
              //   csv: '',
              //   programID: '',
              //   task_type: '',
              //   task_text: '',
              //   task_link: '',
              //   task_file :'',

              //   lessonCount: 12,
              //   finishedLessonCount: 7,
              //   // course dialog
              //   notifications: false,
              //   sound: true,
              //   widgets: false,
              //   // courseLink: 'http%3a%2f%2fvideo.ch9.ms%2fbuild%2f2011%2fslides%2fTOOL-532T_Sutter.pptx'
              //   courseLink: 'https://backend-wewritebugs.app.secoder.net/files/lesson/7-2Fourier级数的收敛性.ppt'
              // },
              // {
              //   name: '数据结构',
              //   intro: '小学二年级课程',
              //   tag: '必修',
              //   recommendTime: 'Day 2',
              //   audience: '',
              //   cover: '',
              //   content_type: '',
              //   isTemplate: '',
              //   csv: '',
              //   programID: '',
              //   task_type: '',
              //   task_text: '',
              //   task_link: '',
              //   task_file :'',

              //   lessonCount: 15,
              //   finishedLessonCount: 6,
              //   // course dialog
              //   notifications: false,
              //   sound: true,
              //   widgets: false,
              //   courseLink: 'newteach.pbworks.com%2Ff%2Fele%2Bnewsletter.docx'
              //   // courseLink: 'https://view.xdocin.com/file_8na57uxpj5pzquob5iy5zixn2zi.htm?p=eyJfcyI6InZ1enRqeGpyb2N3ZjRiN2YiLCJfdCI6IjE2NTAzMDU4MDQifQ%3D%3D'
              // },
            ],
            class_tag_items: ['必修', '限选', '任选'],
            class_recommendTime_items: [],
            classTag_selected: '',
            courseDialog: false,
            class_selected: [], // 选中的课程
            addFromDialog: false,
            addFromList: [],

            // 添加课程
            uploadLessonDialog: false, // 上传课程弹窗
            toAddClass: { // 要添加的课程的名称
            /*
              name: '线性代数',
              intro: '线性代数2022秋',
              tag: '',
              recommendTime: 64,
              audience: 'newcomer',
              cover: 'NOT_A_REAL_BMP',
              isTemplate: false
              */
              name: '',
              intro: '',
              tag: [],
              recommendTime: '',
              audience: '',
              isTemplate: false,
              resetFields() {
                this.name = ''
                this.intro = ''
                this.tag = []
                this.recommendTime = ''
                this.audience = ''
                this.isTemplate = false
                // this.cover = ''
              }
            },
            toAddLesson: {
              name: '',
              intro: '',
              recommendTime: '',
              cover: 'NOT_A_REAL_BMP',
              resetFields() {
                this.name = ''
                this.intro = ''
                this.recommendTime = ''
                // this.cover = ''
              }
            },

            // lesson清单
            lesson_file_list: [],
            lesson_items: [
              /*
              {
                index: 1,
                name: '向量及其运算',
                intro: '线性代数的基础',
                recommendTime: 3,
                audience: '',
                cover: 'NOT_A_REAL_BMP',
                content_type: '',
                coursewares: []
              },
              {
                index: 2,
                name: '矩阵及其运算',
                intro: '把向量放在一起就是矩阵',
                recommendTime: 3,
                audience: '',
                cover: 'NOT_A_REAL_BMP',
                content_type: '',
                coursewares: []
              }
              */
            ],
            modify_item: -1,
            newLessonItem : {
              index: '',
              name: '',
              intro: '',
              recommendTime: '',
              audience: '',
              cover: '',
              content_type: '',
              coursewares: []
            },

            audience_options: [{
              label: '面向新人',
              value: 'newcomer'
            }, {
              label: '导师培训',
              value: 'teacher'
            }],
            // audience_value: '',

            // 其他
            // ruleForm: { // 存档，后面要改成课程、考试、任务各自
            //     name: '',
            //     time: '',
            // },
            rules: {
                name: [
                    { required: true, message: '请输入课程名称', trigger: 'blur' },
                    { min: 3, max: 20, message: '长度在3～20个字符', trigger: 'blur' }
                ],
                recommendTime: [
                    { required: true, message: '请输入推荐用时', trigger: 'blur' },
                ],
                audience: [
                  { required: true, message: '请选择受众', trigger: 'change' }
                ],
                isObligatory: [
                  { required: true, message: '请选择课程性质', trigger: 'change' }
                ],
            },
            lesson_rules: {
                name: [
                    { required: true, message: '请输入本讲名称', trigger: 'blur' },
                    { min: 3, max: 20, message: '长度在3～20个字符', trigger: 'blur' }
                ],
                recommendTime: [
                    { required: true, message: '请输入推荐用时', trigger: 'blur' },
                ],
            },
        }
    },
    computed: {
      class_items_modified() {  // 前端筛选后的数据
        if(this.formInline.learnStatus || this.formInline.recommendTime || this.formInline.tag || this.formInline.classType){
          return this.class_items.filter(data => (!this.formInline.learnStatus || this.formInline.learnStatus === "全部") || data.isFinished === (this.formInline.learnStatus === "已完成"))
          .filter(data => (!this.formInline.recommendTime || this.formInline.recommendTime === "全部") || data.recommendTime === this.formInline.recommendTime)
          .filter(data => (!this.formInline.tag || this.formInline.tag === "全部") || data.tag.includes(this.formInline.tag))
          .filter(data => (!this.formInline.classType || this.formInline.classType === "全部") || data.isObligatory === (this.formInline.classType === "必修"))
        }
        else return this.class_items
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
            default: '',
        },
        showAudience: {
            type: String,
            required: true,
        },
    },
    watch: {
        // 搜索
        // search_name() {
        //   console.log('search_name', this.search_name)
        //   console.log(this.addFromList)
        // },

        audience_value(newVal, oldVal) {
            this.toAddClass.audience = newVal
            console.log('audience' + oldVal + '->' + newVal)
        },
        programID() {
          this.getCourseList()
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
        this.toAddClass.tag.splice(this.toAddClass.tag.indexOf(tag), 1);
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
          this.toAddClass.tag.push(inputValue);
          console.log('output tag', this.toAddClass.tag);
        }
        this.inputVisible = false;
        this.inputValue = '';
      },


        changeSelectOptions(){
          /* 
          初始化筛选框
          是否应该优化成watch(tabledata) -> initializeSelectOptions?
          */
          var tableData = this.class_items;
          console.log(this.class_items);
          var learnStatusOptions = [];
          var recommendTimeOptions = [];
          var tagOptions = [];
          // var classTypeOptions = [];
          for(var i = 0; i < tableData.length; i++){
              learnStatusOptions.push(tableData[i].isFinished ? '已完成' : '未完成');
              recommendTimeOptions.push(tableData[i].recommendTime);
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
        finish_all(){
          alert("finish all!")
          COMM.finish_all_lesson(this.GLOBAL.username);
        },
        async getCourseList(){
            // TODO: 获取course_list
            console.log('获取course_list')
            // if(this.valid.studyContent){
            //     COMM.my_course_list().then(res => {
            //         console.log("my_course_list success: ", res)
            //         this.class_items = res.courses;
            //         this.class_recommendTime_items = res.class_recommendTime_items;
            //         this.class_tag_items = res.class_tag_items;
            //     }, err => {
            //         console.log("my_course_list error: ", err)
            //     })
            // }
            // if(this.valid.addContent){
            //     COMM.assignable_course_list().then(res =>{
            //         console.log("assignable_course_list success: ", res);
            //         this.class_items = res.courses;
            //         this.class_recommendTime_items = res.class_recommendTime_items;
            //         this.class_tag_items = res.class_tag_items;
            //     }, err => {
            //         console.log("assignable_course_list error: ", err)
            //     })
            // }
            if(this.programID != '') {
              var res = await COMM.program_content_list(this.programID)
              // var courses = res.courses
              // courses.forEach(course => {
              //   this.class_items.push({
              //     name: course.name,
              //     intro: course.intro,
              //     tag: course.tag,
              //     recommendTime: course.recommendTime,
              //     audience: course.audience,
              //     cover: '',
              //     content_type: course.content_type,
              //     isTemplate: course.isTemplate,
              //     csv: '',
              //     programID: course.programID,
              //     task_type: '',
              //     task_text: '',
              //     task_link: '',
              //     lessonCount: course.lessonCount,
              //     lessonFinished: 0, // TODO: modify API to add lesson finished data
              //     notifications: false,
              //     sound: true,
              //     widgets: false,
              //     courseLink: ''
              //   })
              // });
              this.class_items = res.courses
              console.log('this.class_items', this.class_items);
              this.changeSelectOptions();
              if(this.showAudience !== '') {
                this.class_items = this.class_items.filter(dct => dct.audience === this.showAudience)
                this.changeSelectOptions();
              }
            }
            else {
              var res_else = await COMM.my_course_list()
              // var courses_else = res_else.courses
              // courses_else.forEach(course => {
              //   this.class_items.push({
              //     name: course.name,
              //     intro: course.intro,
              //     tag: course.tag,
              //     recommendTime: course.recommendTime,
              //     audience: course.audience,
              //     cover: '',
              //     content_type: 'course',
              //     isTemplate: course.isTemplate,
              //     csv: '',
              //     programID: course.programID,
              //     task_type: '',
              //     task_text: '',
              //     task_link: '',
              //     lessonCount: course.lessonCount,
              //     lessonFinished: 0, // TODO: modify API to add lesson finished data
              //     notifications: false,
              //     sound: true,
              //     widgets: false,
              //     courseLink: ''
              //   })
              // })
              this.class_items = res_else.courses
              this.changeSelectOptions();
              if(this.showAudience !== '') {
                this.class_items = this.class_items.filter(dct => dct.audience === this.showAudience)
                this.changeSelectOptions();
              }
            }
        },

        postClassInfo(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.uploadLessonDialog = true;
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
        cacheLesson(formName) {
            // 判断课件/讲/lesson是否合法
            // this.$refs[formName].validate((valid) => {
            //   if (valid) {
            //     console.log(this.$refs[formName])

            //   } else {
            //     console.log('error submit!!');
            //     return false;
            //   } 
            // });
            // TODO：向后端发送lesson数据
            console.log(formName)
            this.$refs.upload_lesson.submit()
            //alert('submit!');
            this.uploadLessonDialog = false
            console.log('find class', this.toAddClass);
            this.resetLessonForm()
        },
        resetLessonForm(formName) {  // 取消：重置表单输入
            console.log(formName)
            this.toAddLesson.name = ''
            this.toAddLesson.intro = ''
            this.toAddLesson.recommendTime = ''
            if(this.$refs.upload_lesson != undefined)
            this.$refs.upload_lesson.clearFiles()
            this.uploadLessonDialog = false
        },
        resetClassForm(formName) {
            console.log(formName)
            this.$refs[formName].resetFields();
            this.lesson_items = [];
            
            this.resetLessonForm()
            if(this.$refs.upload_lesson != undefined)
            this.$refs.upload_lesson.clearFiles()
            this.toAddClass = {
                name: '',
                intro: '',
                tag: [],
                recommendTime: '',
                audience: '',
                cover: 'NOT_A_REAL_BMP',
                isTemplate: false
            }
            
            // this.closeClassDialog();
        },
        async uploadClass(formName) {
            console.log(formName)
            console.log('this.toAddClass', this.toAddClass);
            await COMM.upload_course(this.programID, this.toAddClass, this.lesson_items)
            this.closeClassDialog()
            this.getCourseList()
        },
        cacheLessonData(item){
            /* 上传课件（目前只支持pptx）*/
            if(this.modify_item == -1) {
            console.log('cache lesson data')
            console.log(item)
            let file = item.file
            console.log(file)
            if (this.toAddLesson.name == "" || this.toAddLesson.recommendTime == "" || file == null) {
                alert('课程名称、推荐时间和课件是必填项')
                this.resetLessonForm()
            }
            if (this.newLessonItem.name != this.toAddLesson.name) {
                this.newLessonItem = {
                index: this.lesson_items.length + 1,
                name: this.toAddLesson.name,
                intro: this.toAddLesson.intro,
                recommendTime: this.toAddLesson.recommendTime,
                audience: this.toAddClass.audience,
                cover: this.toAddLesson.cover,
                content_type: '',
                coursewares: [file]
                }
                this.lesson_items.push(this.newLessonItem)
            } else {
                this.newLessonItem.coursewares.push(file)
                this.lesson_items = this.lesson_items.slice(0, -1)
                this.lesson_items.push(this.newLessonItem)
            }
            return
            } else {
            console.log('cache lesson data')
            console.log(item)
            let file = item.file
            console.log(file)
            if (this.toAddLesson.name == "" || this.toAddLesson.recommendTime == "" || file == null) {
                alert('课程名称、推荐时间和课件是必填项')
                this.resetLessonForm()
            }
            if (this.newLessonItem.name != this.toAddLesson.name) {
                this.newLessonItem = {
                index: this.lesson_items.length + 1,
                name: this.toAddLesson.name,
                intro: this.toAddLesson.intro,
                recommendTime: this.toAddLesson.recommendTime,
                audience: this.toAddClass.audience,
                cover: this.toAddLesson.cover,
                content_type: '',
                coursewares: [file]
                }
                this.lesson_items[this.modify_item] = this.newLessonItem
            } else {
                this.newLessonItem.coursewares.push(file)
                this.lesson_items[this.modify_item] = this.newLessonItem
            }
            this.modify_item = -1
            }
            this.lesson_file_list = []
            // const form = new FormData()  // FormData 对象
            // form.append('file', fileObj)  // 文件对象  'upload'是后台接收的参数名
            // COMM.upload_lesson_file(form).then(res => {
            //   console.log('submit test file success:', res)      
            // }, (err) => {
            //   console.log('submit test file error:', err)
            // })
        },
        // async checkAddClassSetTemplateClearance() {
        //     console.log('check clearance')
        //     var res = await COMM.getCurRole()
        //     var role = res.role
        //     if (role != 'admin') {
        //     this.toAddClass.isTemplate = false
        //     alert('无管理员权限，不能设置模板！')
        //     }
        // },

        editLesson(index) {
            this.toAddLesson.name = this.lesson_items[index].name
            this.toAddLesson.intro = this.lesson_items[index].intro
            this.toAddLesson.recommendTime = this.lesson_items[index].recommendTime
            this.toAddLesson.cover = this.lesson_items[index].cover
            this.lesson_file_list = this.lesson_items[index].coursewares
            this.uploadLessonDialog = true
            this.modify_item = index
        },
        deleteLesson(index) {
            var tmp_lesson_list = []
            this.lesson_items.forEach((lesson, i, array) => {
            console.log(array)
            if (i != index)
                tmp_lesson_list.push(lesson)
            });
            this.lesson_items = tmp_lesson_list
        },
        async deleteCourse(contentID) {
            // var tmp_course_list = []
            // this.class_items.forEach((course, i, array) => {
            //   console.log(array[i])
            //   if (i != index)
            //     tmp_course_list.push(course)
            // });
            // this.class_items = tmp_course_list
            // this.changeSelectOptions();
            await COMM.delete_content_from_program(this.programID, contentID)
            await this.getCourseList()
        },
        genName(name, index){
            return '第' + (index + 1) + '讲：' + name
        },
        openClassDialog() {
          this.courseDialog = true
        },
        closeClassDialog() {
          this.courseDialog = false
          this.resetClassForm('toAddClass')
        },
        openAddFromDialog() {
          // COMM.assignable_course_list().then(
          //   response => {
          //     this.addFromList = response.courses
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
              this.getCourseList()
              this.addFromDialog = false
              // this.refreshAddFromList()
            }
          )
        },
        async refreshAddFromList() {
          var allContents = await COMM.assignable_course_list()
          allContents = allContents.courses
          var usedContents = this.class_items
          // usedContents = usedContents.courses
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
          console.log(used)
          console.log(allContents)
          console.log(usedContents)
          this.addFromList = deduplicatedContents
          if(this.showAudience !== '') {
            this.addFromList = this.addFromList.filter(dct => dct.audience === this.showAudience)
          }
        }
    },
    created() {
        // DONE: 现在后端没有造课程的数据，所以先用default数据代替，不从后端get
        this.getCourseList();
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
