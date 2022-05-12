<template>
<v-container style="margin-top: 10px">
  <v-row>
    
    <!-- 左栏：课程 -->
    <v-col cols="12" sm="6" md="7">
      <course-display :programID="programID" :showAudience="showAudience"></course-display>
    </v-col>
    
    <!-- 右栏：考试与任务 -->
    <v-col cols="6" md="5">

      <!-- 考试 -->
      <exam-display :programID="programID" :showAudience="showAudience"></exam-display>

      <!-- 任务 -->
      <task-display :programID="programID" :showAudience="showAudience"></task-display>

    </v-col>
  </v-row>
</v-container>
</template>

<script>

// import COMM from "@/utils/Comm"
import CourseDisplay from './CourseDisplay.vue'
import ExamDisplay from './ExamDisplay.vue'
import TaskDisplay from './TaskDisplay.vue'

// var testDownloadTestID = "testDownloadTestID"

export default ({
    name: 'ContentDisplay',
    inject: ['GLOBAL'],
    components: {
      CourseDisplay,
      ExamDisplay,
      TaskDisplay, 
    },
    data() { 
        return {
            // course dialog
            courseDialog: false,
            notifications: false,
            sound: true,
            widgets: false,

            /*
            // 在子组件中定义
            uploadLessonDialog: false, // 上传课程弹窗
            */

            uploadTestDialog: false, // 上传考试弹窗
            uploadTaskDialog: false, // 上传任务弹窗
            addClassDialog: false, // 添加课程弹窗

            /*
            // 在子组件中定义
            toAddClass: { // 要添加的课程的名称
              name: '线性代数',
              intro: '线性代数2022秋',
              tag: '',
              recommend_time: 64,
              audience: 'newcomer',
              cover: 'NOT_A_REAL_BMP',
              is_template: false
            },
            toAddTest: {
              name: 'TEST', 
              intro: 'hahaha', 
              tag: 'tag1 tag2 tag3', // TODO：需要改成list而不是string
              recommend_time: 120, //
              audience: 'newcomer',
              cover: 'NOT_A_REAL_BMP',
              csv: 'NOT_A_REAL_CSV',
            },
            toAddLesson: {
              name: '',
              intro: '',
              recommend_time: '',
              cover: 'NOT_A_REAL_BMP',
              resetFields() {
                this.name = ''
                this.intro = ''
                this.recommend_time = ''
                // this.cover = ''
              }
            },
            // toAddTask: {
            //   name: '',
            //   intro: '',
            //   tag: '',
            //   recommend_time: '',
            //   is_template: '',
            //   taskType: '',
            //   taskText: '',
            //   taskLink: '',
            //   taskFile: ''
            // },
            toFinishTask: {
              name: '',
              intro: '',
              tag: '',
              recommend_time: '',
              is_template: '',
              taskType: '',
              taskText: '',
              taskLink: '',
              taskFile: '',
              taskID: ''
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
            task_type_value: '',
            
            isTextTask: false,
            isFileTask: false,
            isLinkTask: false,
            isDoingTextTask: false,
            isDoingLinkTask: false,
            isDoingFileTask: false,
            doTaskDialog: false,
            ruleForm: { // 存档，后面要改成课程、考试、任务各自
              name: '',
            },
            rules: {
                name: [
                    { required: true, message: '请输入课程名称', trigger: 'blur' },
                    { min: 3, max: 20, message: '长度在3～20个字符', trigger: 'blur' }
                ],
            },
            */
            // class list: 后续需要修改变量名（毕竟后端还没有写出来接口）
            // selected: [2],

            /*
            // 在子组件中定义
            class_items: [
              {
                name: '微积分',
                intro: '小学一年级课程',
                tag: '必修',
                recommend_time: 'Day 3',
                audience: '',
                cover: '',
                content_type: '',
                is_template: '',
                csv: '',
                program_id: '',
                task_type: '',
                task_text: '',
                task_link: '',
                task_file :'',

                lessonNum: 12,
                finishLessons: 7,
                // course dialog
                courseDialog: false,
                notifications: false,
                sound: true,
                widgets: false,
                // courseLink: 'http%3a%2f%2fvideo.ch9.ms%2fbuild%2f2011%2fslides%2fTOOL-532T_Sutter.pptx'
                courseLink: 'https://backend-wewritebugs.app.secoder.net/files/lesson/7-2Fourier级数的收敛性.ppt'
              },
              {
                name: '数据结构',
                intro: '小学二年级课程',
                tag: '必修',
                recommend_time: 'Day 2',
                audience: '',
                cover: '',
                content_type: '',
                is_template: '',
                csv: '',
                program_id: '',
                task_type: '',
                task_text: '',
                task_link: '',
                task_file :'',

                lessonNum: 15,
                finishLessons: 6,
                // course dialog
                courseDialog: false,
                notifications: false,
                sound: true,
                widgets: false,
                courseLink: 'newteach.pbworks.com%2Ff%2Fele%2Bnewsletter.docx'
                // courseLink: 'https://view.xdocin.com/file_8na57uxpj5pzquob5iy5zixn2zi.htm?p=eyJfcyI6InZ1enRqeGpyb2N3ZjRiN2YiLCJfdCI6IjE2NTAzMDU4MDQifQ%3D%3D'
              },
            ],
            class_tag_items: ['必修', '限选', '任选'],
            class_recommend_time_items: [],
            classTag_selected: '',
            class_selected: [], // 选中的任务


            test_items: [
              // {
              //   name: '游泳测试',
              //   intro: '介绍',
              //   tag: '必修',
              //   recommend_time: 100,
              //   audience: '',
              //   cover: '',
              //   content_type: '',
              //   is_template: '',
              //   csv: '',
              //   program_id: '',
              //   task_type: '',
              //   task_text: '',
              //   task_link: '',
              //   task_file :'',
              // },
              // {
              //   name: '体育测试',
              //   intro: '介绍',
              //   tag: '限选',
              //   recommend_time: 200,
              //   audience: '',
              //   cover: '',
              //   content_type: '',
              //   is_template: '',
              //   csv: '',
              //   program_id: '',
              //   task_type: '',
              //   task_text: '',
              //   task_link: '',
              //   task_file :'',
              // },
            ],
            test_tag_items: ['必修', '限选', '任选'],
            testTag_selected: '', 
            test_recommend_time_items: [],


            task_items: [
              // {
              //   name: '见一次导师',
              //   intro: '与被分配到的导师见面',
              //   tag: '必修',
              //   recommend_time: 'Day 1',
              //   audience: '',
              //   cover: '',
              //   content_type: '',
              //   is_template: '',
              //   csv: '',
              //   program_id: '',
              //   task_type: '',
              //   task_text: '',
              //   task_link: '',
              //   task_file :'',
              //   isFinished: true,
              // },
              // {
              //   name: '见第二次导师',
              //   intro: '与被分配到的导师再见一次面',
              //   tag: '限选',
              //   recommend_time: 'Day 2',
              //   audience: '',
              //   cover: '',
              //   content_type: '',
              //   is_template: '',
              //   csv: '',
              //   program_id: '',
              //   task_type: '',
              //   task_text: '',
              //   task_link: '',
              //   task_file :'',
              //   isFinished: false,
              // },
            ],
            task_tag_items: ['必修', '限选', '任选'],
            task_recommend_time_items: [],
            task_selected: [], // 选中的任务
            taskTag_selected: '',
            
            lesson_file_list: [],
            lesson_items: [
              {
                index: 1,
                name: '向量及其运算',
                intro: '线性代数的基础',
                recommend_time: 3,
                audience: '',
                cover: 'NOT_A_REAL_BMP',
                content_type: '',
                coursewares: []
              },
              {
                index: 2,
                name: '矩阵及其运算',
                intro: '把向量放在一起就是矩阵',
                recommend_time: 3,
                audience: '',
                cover: 'NOT_A_REAL_BMP',
                content_type: '',
                coursewares: []
              }
            ],
            modify_item: -1
            ,
            newLessonItem : {
              index: '',
              name: '',
              intro: '',
              recommend_time: '',
              audience: '',
              cover: '',
              content_type: '',
              coursewares: []
            },
            dup_file_marker: false,
            */

            // 身份权限相关数据
            valid: {
              addContent: false,
              studyContent: true, 
            },

            /*
            // 在子组件中定义
            dayItems: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5'],
            audience_options: [{
              label: '面向新人',
              value: 'newcomer'
            }, {
              label: '导师培训',
              value: 'teacher'
            }],
            audience_value: ''
            */
        }
    },
    props: {
      programID: {
        type: String,
        default: () => {
          return ""
        }
      },
      // 回调函数，NewcomerBoardEdit -> NewcomerManage
      closeNewcomerBoard: {
        type: Function,
        default: () => {
        return () => {}
        }
      },
      showAudience: {
          type: String,
          required: true,
      }
      // 身份权限相关数据
      // identity: {
      //   type: String,
      //   default: 'newcomer' // tutor, HRBP, admin
      // }, 
    },
    watch: {
      /*
      // 在子组件中定义
      audience_value(newVal, oldVal) {
        this.toAddClass.audience = newVal
        console.log('audience' + oldVal + '->' + newVal)
      },
      */
      // identity(data) {
      //   console.log('identity:', data)
      //   if(data == 'newcomer' || data == 'tutor'){
      //       this.valid = {
      //         addContent: false,
      //         studyContent: true, 
      //       }
      //   }
      //   else if (data == 'admin'){
      //     this.valid = {
      //         addContent: true,
      //         studyContent: false, 
      //     }
      //   }
      // }
    },
    methods: {
      /*
      // 在子组件中定义
      postClassInfo() {
        // TODO: 把lesson对应的class信息发送到后台
        console.log('class', this.toAddClass.name)
      },
      */
      
      closeSelf() {
        this.closeNewcomerBoard() // 调用回调函数关闭自己
      },

      /*
      // 在子组件中定义
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
        this.resetLessonForm()
      },
      resetLessonForm(formName) {  // 取消：重置表单输入
        console.log(formName)
        this.toAddLesson.name = ''
        this.toAddLesson.intro = ''
        this.toAddLesson.recommend_time = ''
        if(this.$refs.upload_lesson != undefined)
          this.$refs.upload_lesson.clearFiles()
        this.uploadLessonDialog = false
      },
      resetClassForm(formName) {
        console.log(formName)
        this.resetLessonForm()
        if(this.$refs.upload_lesson != undefined)
          this.$refs.upload_lesson.clearFiles()
        this.toAddClass = {
            name: '',
            intro: '',
            tag: '',
            recommend_time: '',
            audience: '',
            cover: 'NOT_A_REAL_BMP',
            is_template: false
        }
        this.addClassDialog = false
      },
      uploadClass(formName) {
        console.log(formName)
        COMM.upload_course(this.toAddClass, this.lesson_items)
      },
      */

      openClassDialog() { // 提供给子组件CourseDisplay的回调函数
        this.addClassDialog = true;
      },
      closeClassDialog() { // 提供给子组件CourseDisplay的回调函数
        this.addClassDialog = false;
      },

      // uploadTestFile(item){
      //   /* 上传testfile文件（.csv） */
      //   let fileObj = item.file
      //   const form = new FormData()  // FormData 对象
      //   form.append('file', fileObj)  // 文件对象  'upload'是后台接收的参数名
      //   COMM.upload_test_file(form).then(res => {
      //     console.log('submit test file success:', res)      
      //   }, (err) => {
      //     console.log('submit test file error:', err)
      //   })
      // },
      
      /*
      // 在子组件中定义
      cacheLessonData(item){
        // 上传课件（目前只支持pptx
        if(this.modify_item == -1) {
          console.log('cache lesson data')
          console.log(item)
          let file = item.file
          console.log(file)
          if (this.toAddLesson.name == "" || this.toAddLesson.recommend_time == "" || file == null) {
            alert('课程名称、推荐时间和课件是必填项')
            this.resetLessonForm()
          }
          if (this.newLessonItem.name != this.toAddLesson.name) {
            this.newLessonItem = {
              index: this.lesson_items.length + 1,
              name: this.toAddLesson.name,
              intro: this.toAddLesson.intro,
              recommend_time: this.toAddLesson.recommend_time,
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
          if (this.toAddLesson.name == "" || this.toAddLesson.recommend_time == "" || file == null) {
            alert('课程名称、推荐时间和课件是必填项')
            this.resetLessonForm()
          }
          if (this.newLessonItem.name != this.toAddLesson.name) {
            this.newLessonItem = {
              index: this.lesson_items.length + 1,
              name: this.toAddLesson.name,
              intro: this.toAddLesson.intro,
              recommend_time: this.toAddLesson.recommend_time,
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
      async checkAddClassSetTemplateClearance() {
        console.log('check clearance')
        var res = await COMM.getCurRole()
        var role = res.role
        if (role != 'admin') {
          this.toAddClass.is_template = false
          alert('无管理员权限，不能设置模板！')
        }
      },
      */
      
      // async checkAddTaskSetTemplateClearance() {
      //   console.log('check clearance')
      //   var res = await COMM.getCurRole()
      //   var role = res.role
      //   if (role != 'admin') {
      //     this.toAddTask.is_template = false
      //     alert('无管理员权限，不能设置模板！')
      //   }
      // },

      /*
      // 在子组件中定义
      editLesson(index) {
        this.toAddLesson.name = this.lesson_items[index].name
        this.toAddLesson.intro = this.lesson_items[index].intro
        this.toAddLesson.recommend_time = this.lesson_items[index].recommend_time
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
      genName(name, index){
        return '第' + (index + 1) + '讲：' + name
      },

      uploadTest(form){
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
        uploadForm.append('recommendTime', this.toAddTest.recommend_time)
        uploadForm.append('audience', this.toAddTest.audience)
        uploadForm.append('cover', this.toAddTest.cover)
        uploadForm.append('csv', form.file)
        COMM.upload_test_template(uploadForm)
        // alert('submit!');
        this.uploadTestDialog = false
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
      testCommit(){
        this.$refs.upload_test.submit()
      },
      resetTaskForm() {
        this.toAddTask = {
          name: '',
          intro: '',
          tag: '',
          recommend_time: '',
          taskType: '',
          taskText: '',
          taskLink: '',
          taskFile: ''
        }
        this.uploadTaskDialog = false
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
      uploadTask(filehook) {
        var file
        if (filehook && this.isFileTask)
          file = filehook.file
        else
          file = null
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
        if(this.isTextTask)
          uploadForm.append('taskText', this.taskText)
        else
          uploadForm.append('taskText', '')
        if(this.isLinkTask)
          uploadForm.append('taskLink', this.taskLink)
        else
          uploadForm.append('taskLink', '')
        if(this.isFileTask)
          uploadForm.append('taskFile', file)
        else
          uploadForm.append('taskFile', '')
        console.log(uploadForm)
        COMM.upload_task(uploadForm)
      },
      taskCommit() {
        if(this.$refs.upload_task)
          this.$refs.upload_task.submit()
        else
          this.uploadTask(null)
        this.resetTaskForm()
      },
      */

      closeTaskDialog() { // 提供给子组件TaskDisplay的回调函数
        this.uploadTaskDialog = false;
      },

      /*
      // 在子组件中定义
      downloadTestByID() {
        var info = COMM.downloadTestInfoByID(testDownloadTestID)
        var paper = COMM.downloadTestPaperByID(testDownloadTestID)
        console.log(info)
        console.log(paper)
      },
      resetTestForm(formName){  // 取消：重置表单输入
        this.$refs[formName].resetFields();
        this.$refs.upload_test.clearFiles()
        this.uploadTestDialog = false
      },
      */

      closeTestDialog() { // 提供给子组件TestDisplay的回调函数
        this.uploadTestDialog = false;
      },

      /*
      saveClass(){ // 保存课程（class）
        // TODO：像后端发送课程数据
      },
      */

      /*
      // 在子组件中定义
      getTestList(){
        // TODO: 获取test_list
        console.log('获取test_list')
        if(this.valid.studyContent){
          COMM.my_test_list().then(res => {
            console.log("my_test_list success: ", res)
            this.test_items = res.tests;
            this.test_recommend_time_items = res.test_recommend_time_items;
            this.test_tag_items = res.test_tag_items;
          }, err => {
            console.log("my_test_list error: ", err)
          })
        }
        if(this.valid.addContent){
          COMM.assignable_test_list().then(res =>{
            console.log("assignable_test_list success: ", res);
            this.test_items = res.tests;
            this.test_recommend_time_items = res.test_recommend_time_items;
            this.test_tag_items = res.test_tag_items;
          }, err => {
            console.log("assignable_test_list error: ", err)
          })
        }
      },
      getTaskList(){
        console.log('get task list')
        if(this.valid.studyContent) {
          COMM.my_task_list().then(res => {
            this.task_items = res.tasks;
            this.task_recommend_time_items = res.task_recommend_time_items;
            console.log('task_recommend_time_items', this.task_recommend_time_items)
            this.task_tag_items = res.task_tag_items;
            console.log('my_task_list: ', res);
          }, err => {
            console.log('my task list error: ', err)
          })
        }
        if(this.valid.addContent){
          COMM.assignable_task_list().then(res => {
            this.task_items = res.tasks;
            this.task_recommend_time_items = res.task_recommend_time_items;
            console.log('task_recommend_time_items', this.task_recommend_time_items)
            this.task_tag_items = res.task_tag_items;
            console.log('assignable_task_list: ', res)
          }, err => {
            console.log('assignable task list error', err)
          })
        }
      },
      async handleTaskClick(task_item) {
        if(this.valid.studyContent) {
          this.toFinishTask.name = task_item.name
          this.toFinishTask.intro = task_item.intro
          this.toFinishTask.tag = task_item.tag
          this.toFinishTask.recommendTime = task_item.recommendTime
          this.toFinishTask.taskType = task_item.taskType
          this.toFinishTask.taskText = task_item.taskText
          this.toFinishTask.taskLink = task_item.taskLink
          this.toFinishTask.taskID = task_item.taskID
          if(this.toFinishTask.taskType == 'file') {
            var res = await COMM.retrieveTaskFileByID(task_item.taskID)
            console.log(res)
            // TODO
          }
          this.doTaskDialog = true
        }
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
        this.toFinishTask.taskID = ''
      },
      testTag_select(data) {  // 选择考试标签
        console.log(data)
      },
      taskTag_select() {  // 选择任务标签

      },
      */
    },
    mounted() {
      // identity（为确认当前角色的权限）
      console.log('mounted identity:', this.identity)
      
      // TODO: 后续需要增加单独的功能性判断（有的角色在不同界面有不同功能权限）
      // if(this.identity == 'newcomer' || this.identity == 'tutor'){
      //     this.valid = {
      //       addContent: false,
      //       studyContent: true, 
      //     }
      // }
      // else if (this.identity == 'admin'){
      //   this.valid = {
      //       addContent: true,
      //       studyContent: false, 
      //   }
      // }

      // console.log('valid to:', this.valid)
      // this.getTestList() // 在子组件中获取
      // this.getTaskList() // 在子组件中获取
      console.log("test for global:", this.GLOBAL.contentDisplayAddif, this.GLOBAL.contentDisplayUser)
    }
})
</script>
