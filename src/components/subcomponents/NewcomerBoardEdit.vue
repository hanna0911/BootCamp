<template>
  <v-container>
    <!-- 返回按钮与新人姓名 -->
    <div style="margin-left: 10px; margin-top: 5px; margin-bottom: -10px">
        <v-btn @click="closeSelf">返回</v-btn>
        <h2 v-if="assignedProgramID === ''" class="px-4 pt-4 pb-3 font-weight-black">为 {{ newcomerIdentity.name }} 分配学习模板</h2>
        <h2 v-else class="px-4 pt-4 pb-3 font-weight-black"> {{ newcomerIdentity.name }} 的培训界面</h2>
    </div>
    <NewcomerSummary
        v-if="assignedProgramID !== '' && showAudience === 'newcomer'"
        :newcomerInfo="this.newcomerInfo"
        :newcomer="this.newcomerIdentity.name"
    ></NewcomerSummary>
    <TutorSummary
        v-if="assignedProgramID !== '' && showAudience === 'teacher'"
        :tutorInfo="this.tutorInfo"
        :tutor="this.newcomerIdentity.name"
    ></TutorSummary>
    <!-- 如果未被分配program，那么显示program列表以供分配 -->
    <ProgramList v-if="assignedProgramID === ''" :displayType="'assign'" :assignProgram="assignProgram" :showAudience="showAudience"/>
    <!-- 如果已被分配，则显示这个program -->
    <content-display v-else :programID="assignedProgramID" :showAudience="showAudience"/>
  </v-container>
</template>


<script>
import COMM from "@/utils/Comm"
import ContentDisplay from '../content/ContentDisplay.vue'
import ProgramList from '../subcomponents/ProgramList.vue'
import NewcomerSummary from "@/components/subcomponents/NewcomerSummary";
import TutorSummary from "@/components/subcomponents/TutorSummary";

export default ({
    name: "NewcomerBoardEdit",
    inject: ['GLOBAL'],
    components: {
        ContentDisplay, 
        ProgramList,
        NewcomerSummary,
        TutorSummary
    },
    data() {
        return {
            uploadDialog: false,
            newcomerInfo: {  // 新人旅程相关数据，从后端获取！
              startDate: '',
              isGraduate: "",
              tutor: '',
              teacherUsername: "100",
              courseProgress: '100',
              examProgress: '100',
              taskProgress: '',
              evaluateProgress: '',
              graduateDate: '',
            },
            tutorInfo:{
              startDate: '',
              courseProgress: '100',
              examProgress: '100',
              taskProgress: '100',
              isGraduate: "",
              graduateDate: '',
            },
            ruleForm: {
                name: '',
                region: '',
                date1: '',
                date2: '',
                delivery: false,
                type: [],
                resource: '',
                desc: ''
            },
            rules: {
                name: [
                    { required: true, message: '请输入活动名称', trigger: 'blur' },
                    { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }
                ],
                region: [
                    { required: true, message: '请选择活动区域', trigger: 'change' }
                ],
                date1: [
                    { type: 'date', required: true, message: '请选择日期', trigger: 'change' }
                ],
                date2: [
                    { type: 'date', required: true, message: '请选择时间', trigger: 'change' }
                ],
                type: [
                    { type: 'array', required: true, message: '请至少选择一个活动性质', trigger: 'change' }
                ],
                resource: [
                    { required: true, message: '请选择活动资源', trigger: 'change' }
                ],
                desc: [
                    { required: true, message: '请填写活动形式', trigger: 'blur' }
                ]
            },
            assignedProgramID: '',
        };
    },
    props: {
        // 回调函数，NewcomerBoardEdit -> NewcomerManage
        closeNewcomerBoard: {
            type: Function,
            default: () => {
                return () => {}
            }
        },
        newcomerIdentity: {},
        showAudience: {
            type: String,
            required: true,
        }
    },
    methods: {
        closeSelf() {
            this.closeNewcomerBoard() // 调用回调函数关闭自己
        },
        // getNewcomerBoard() {
        //     // TODO: 向后端请求该新人的所有课程、考试、任务信息
        //     console.log('getNewcomerBoard', this.newcomerIdentity) // 该新人的所有数据在此字典中，辅助用于从后端获取该新人的数据
        // },
        assignProgram(programID) {
            COMM.copy_program_template(programID).then(
                response => {
                    COMM.assign_program(this.newcomerIdentity.username, response.programID).then(
                        response => {console.log(response); this.has_program()},
                        error => {console.log(error)}
                    )
                },
                error => {
                    console.log(error)
                }
            )
        },
        getSummary(newcomer){
          if(this.showAudience === 'newcomer'){
            COMM.newcomer_summary_info_by_name(newcomer).then(
                response => {console.log(response); this.newcomerInfo = response.data},
                error => {console.log(error)}
            )
          }else {
            COMM.teacher_board_summary_by_name(newcomer).then(
                response => {console.log(response); this.tutorInfo = response.data},
                error => {console.log(error)}
            )
          }
        },

        has_program() {
            COMM.has_program(this.newcomerIdentity.username, this.showAudience).then(
                response => {
                    var programID = response.programID
                    if(programID !== '') {
                        this.GLOBAL.contentDisplayAddif = true
                        this.GLOBAL.contentDisplayUser = true
                    }
                    this.assignedProgramID = programID
                },
                error => {console.log(error)}
            )
        }
    },
    created() {
        this.has_program()
        this.getSummary(this.newcomerIdentity.username)
    },
})
</script>
