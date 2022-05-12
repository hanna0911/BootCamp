<template>
<v-container>
  <ProgramList :displayType="GLOBAL.ident === 'admin' ? 'adminEdit' : 'teacherEdit'" :showAudience="''"/>
</v-container>
</template>


<script>
// import ContentDisplay from './content/ContentDisplay.vue';
import ProgramList from './subcomponents/ProgramList.vue';

export default ({
    name: 'TrainTemplate',
    inject: ['GLOBAL'],
    components: {
      // ContentDisplay
      ProgramList,
    },
    data() {
        return {
            // identity: 'admin', // tutor, HRBP, admin
            // uploadClassDialog: false,
            // ruleForm: {
            //     name: '',
            // },
            // rules: {
            //     name: [
            //         { required: true, message: '请输入课程名称', trigger: 'blur' },
            //         { min: 3, max: 5, message: '长度在3～5个字符', trigger: 'blur' }
            //     ],
            // },
            // // class list: 后续需要修改变量名（毕竟后端还没有写出来接口）
            // // selected: [2],
            // class_items: [
            //   {
            //     name: '课程1',
            //     intro: '介绍',
            //     tag: '必修',
            //     recommend_time: '',
            //     audience: '',
            //     cover: '',
            //     content_type: '',
            //     is_template: '',
            //     csv: '',
            //     program_id: '',
            //     task_type: '',
            //     task_text: '',
            //     task_link: '',
            //     task_file :'',
            //     lessonCount: '5/8 讲',
            //   },
            //   {
            //     name: '课程2',
            //     intro: '介绍',
            //     tag: '必修',
            //     recommend_time: '',
            //     audience: '',
            //     cover: '',
            //     content_type: '',
            //     is_template: '',
            //     csv: '',
            //     program_id: '',
            //     task_type: '',
            //     task_text: '',
            //     task_link: '',
            //     task_file :'',
            //     lessonCount: '5/8 讲',
            //   },
            //   {
            //     name: '课程3',
            //     intro: '介绍',
            //     tag: '必修',
            //     recommend_time: '',
            //     audience: '',
            //     cover: '',
            //     content_type: '',
            //     is_template: '',
            //     csv: '',
            //     program_id: '',
            //     task_type: '',
            //     task_text: '',
            //     task_link: '',
            //     task_file :'',
            //     lessonCount: '5/8 讲',
            //   },
            // ],
            // class_tag_items: ['必修', '限选', '任选'],
            // class_tag_value: ['必修', '限选', '任选'],
            // test_items: [
            //   {
            //     name: '课程1',
            //     intro: '介绍',
            //     tag: '必修',
            //     recommend_time: '',
            //     audience: '',
            //     cover: '',
            //     content_type: '',
            //     is_template: '',
            //     csv: '',
            //     program_id: '',
            //     task_type: '',
            //     task_text: '',
            //     task_link: '',
            //     task_file :'',
            //     recommendedTime: 0,
            //   },
            // ],
            // test_tag_items: ['必修', '限选', '任选'],
            // test_tag_value: ['必修', '限选', '任选'],
        };
    },
    props: {
        // // 回调函数，NewcomerBoardEdit -> NewcomerManage
        // closeNewcomerBoard: {
        //     type: Function,
        //     default: () => {
        //     return () => {}
        //     }
        // },
    },
    methods: {
        // closeSelf() {
        //     this.closeNewcomerBoard() // 调用回调函数关闭自己
        // },
        // uploadClass(formName) {
        //     this.$refs[formName].validate((valid) => {
        //     if (valid) {
        //         console.log(this.$refs[formName])
        //         // COMM.admin_create_content_template()
        //         alert('submit!');
        //         this.uploadClassDialog = false
        //     } else {
        //         console.log('error submit!!');
        //         return false;
        //     }
        //     });
        // },
        // resetClassForm(formName) {
        //     this.$refs[formName].resetFields();
        //     this.uploadClassDialog = false
        // }
    },
    mounted() {
      // this.identity = 'admin';
    },
    created() {
      this.GLOBAL.contentDisplayAddif = false
      this.GLOBAL.contentDisplayUser = false
    }
})
</script>
