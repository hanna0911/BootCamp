<template>
<!-- 封装好的带新看板，需要输入导师名字/id来获取该导师的带新看板 -->
<v-container>
    <!-- 第一行 -->
    <v-row style="margin: 0.5%">

        <!-- 带新概览 -->
        <v-col>
            <v-card>
                <v-card-title>带新概览</v-card-title>
                <v-card-text>
                    <v-row>
                        <v-col>
                            <v-card elevation="0">
                                <v-card-title> {{ leadNewcomerInfo.current }} </v-card-title>
                                <v-card-subtitle>当前带新</v-card-subtitle>
                            </v-card>
                        </v-col>
                        <v-col>
                            <v-card elevation="0">
                                <v-card-title> {{ leadNewcomerInfo.total }} </v-card-title>
                                <v-card-subtitle>总计带新</v-card-subtitle>
                            </v-card>
                        </v-col>
                        <v-col>
                            <v-card elevation="0">
                                <v-card-title> {{ leadNewcomerInfo.dutyDate }} </v-card-title>
                                <v-card-subtitle>上岗日期</v-card-subtitle>
                            </v-card>
                        </v-col>
                    </v-row>
                </v-card-text>
            </v-card>
        </v-col>

        <!-- 个人荣誉 -->
        <v-col>
            <v-card>
                <v-card-title>个人荣誉</v-card-title>
                <v-card-text>
                    <v-row>
                        <v-col>
                            <v-card elevation="0">
                                <v-card-title style="margin-top: -17px">
                                    <v-chip-group>
                                        <v-chip
                                            v-for="(medal, i) in achievement.medals"
                                            :key="i"
                                        >
                                            {{ medal.name }}
                                        </v-chip>
                                    </v-chip-group>
                                </v-card-title>
                                <v-card-subtitle>勋章</v-card-subtitle>
                            </v-card>
                        </v-col>
                        <v-col>
                            <v-card elevation="0">
                                <v-card-title style="margin-top: -16px">
                                    <v-chip-group>
                                        <v-chip
                                            v-for="(certificate, i) in achievement.certificates"
                                            :key="i"
                                        >
                                            {{ certificate.name }}
                                        </v-chip>
                                    </v-chip-group>
                                </v-card-title>
                                <v-card-subtitle>证书</v-card-subtitle>
                            </v-card>
                        </v-col>
                    </v-row>
                </v-card-text>
            </v-card>
        </v-col>
    </v-row>

    <!-- 第二行 -->
    <v-row style="margin: 0.5%">
        <!-- 新人管理 -->
        <v-col>
            <v-card>
                <v-card-title>新人管理</v-card-title>
                <v-card-text>
                    <div style="margin: 1.5%">
                        <!-- 新人列表 -->
                        <newcomer-table 
                            :tables="tables" 
                            :colData="colData" 
                            :formInline="formInline" 
                            :checkNewcomerBoard="checkBoard"
                            :columnShow="columnShow"
                            :tutorIdentity="tutorIdentity"
                            :AdminToTutor="AdminToTutor"
                        ></newcomer-table>
                    </div>
                </v-card-text>
            </v-card>
        </v-col>
    </v-row>
</v-container>
</template>

<script>
import COMM from "@/utils/Comm.js"
import NewcomerTable from "./NewcomerTable.vue"

export default ({
    name: "LeadNewcomerSub",
    components: {
        NewcomerTable,
    },
    inject:["GLOBAL"],
    data() {
        return {
            AdminToTutor: false, 
            leadNewcomerInfo: {
              current: '',
              total: '',
              dutyDate: '',
              historical: '',
            },
            achievement: {
                medals: [{name:'', avatar: ''}],
                certificates: [{name:'', avatar: ''}],
            },
            // 新人管理数据：
            tableData: [], // TODO: 从后端获取raw_data
            colData: [  // table的列项
                {title: "姓名",istrue: true}, // 0
                {title: "是否参与Bootcamp",istrue: true}, // 1
                {title: "直属上级",istrue: true}, // 2
                {title: "城市",istrue: true}, // 3
                {title: "入职情况",istrue: true}, // 4
                {title: "导师分配",istrue: false}, // 5
                {title: "是否毕业",istrue: true}, // 6
                {title: "新人看板",istrue: true}, // 7
                // {title: "带新记录",istrue: true}, // 8
                {title: "新人评价",istrue: true}, // 9
                {title: "部门", istrue: true}, // 10
            ],
            colOptions: [],
            colSelect: [],  
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
            formInline: [],
        }
    },
    props: {
        // 从父组件传来需要get的导师的带新数据
        tutorIdentity: {}, // TODO: 该数据发送至后端，获取对应导师的带新数据（导师旅程+新人列表）
        checkNewcomerBoard: { // 回调函数，LeadNewcomerSub -> LeadNewcomer
          type: Function,
          default: () => {return () => {}}
        },
    },
    computed: {
        tables() {  // 前端筛选后的数据
            return this.tableData
        }
    },
    methods: {
        getLeadNewcomerInfo(){
          if(this.GLOBAL.ident === "teacher"){
            COMM.teacher_summary_info().then(res=>{
              console.log("get summary success")
              this.leadNewcomerInfo = res.data;
              if(!this.leadNewcomerInfo.teacherIsDuty){
                this.leadNewcomerInfo.dutyDate="未上岗"
              }else{
                this.leadNewcomerInfo.dutyDate = this.leadNewcomerInfo.dutyDate.split("T")[0]
              }
            },err=>{
              console.log(this.tutorIdentity)
              this.leadNewcomerInfo.current = 0
              this.leadNewcomerInfo.total = 0
              this.leadNewcomerInfo.historical = 0
              this.leadNewcomerInfo.dutyDate = '未知'
              console.log("error",err)
            })
          } else if(this.GLOBAL.ident === "admin"){
            COMM.teacher_summary_info(this.tutorIdentity.username).then(res=>{
              console.log("get summary success")
              this.leadNewcomerInfo = res.data;
              if(!this.leadNewcomerInfo.teacherIsDuty){
                this.leadNewcomerInfo.dutyDate="未上岗"
              }else{
                this.leadNewcomerInfo.dutyDate = this.leadNewcomerInfo.dutyDate.split("T")[0]

              }
            },err=>{
              console.log(this.tutorIdentity)
              this.leadNewcomerInfo.current = 0
              this.leadNewcomerInfo.total = 0
              this.leadNewcomerInfo.historical = 0
              this.leadNewcomerInfo.dutyDate = '未知'
              console.log("error",err)
            })
          }
        },

        getAchievementInfo(){
          if(this.GLOBAL.ident === "teacher"){
            COMM.get_honor().then(res=>{
              console.log("get honor success")
              this.achievement = res.data;
            },err=>{
              this.achievement.medals = [
                {name: '认真', avatar: ''}, // 完善后可以显示勋章的图片，现在暂时用文字+chip显示
                {name: '负责', avatar: ''},
              ]
              this.achievement.certificates = [
                {name: '第一名', avatar: ''}, // 完善后可以显示证书的图片，现在暂时用文字+chip显示
                {name: '第二名', avatar: ''},
              ]
              console.log("error",err)
            })
          } else if(this.GLOBAL.ident === "admin"){
            COMM.get_honor(this.tutorIdentity.username).then(res=>{
              console.log("get honor success")
              this.achievement = res.data;
            },err=>{
              this.achievement.medals = [
                {name: '认真', avatar: ''}, // 完善后可以显示勋章的图片，现在暂时用文字+chip显示
                {name: '负责', avatar: ''},
              ]
              this.achievement.certificates = [
                {name: '第一名', avatar: ''}, // 完善后可以显示证书的图片，现在暂时用文字+chip显示
                {name: '第二名', avatar: ''},
              ]
              console.log("error",err)
            })
          }

        },
        get_teacher_newcomer_list(){
            console.log('导师身份信息:', this.tutorIdentity) // 导师的身份信息在这里，可以借助这个来获取特定导师的tutor_newcomer_list
            if(this.GLOBAL.ident === "teacher"){
              COMM.get_teacher_newcomer_list().then(
                  res => {
                    console.log("get teacher_newcomer_list success: ", res)
                    this.tableData = res.data;
                  },
                  err => {console.log("get teacher_newcomer_list error: ", err)}
              )
            } else if(this.GLOBAL.ident === "admin"){
              COMM.get_teacher_newcomer_list_by_name(this.tutorIdentity.username).then(
                  res => {
                    console.log("get teacher_newcomer_list success: ", res)
                    this.tableData = res.data;
                  },
                  err => {console.log("get teacher_newcomer_list error: ", err)}
              )
            }
        },
        checkBoard(data){
            this.checkNewcomerBoard(data);  // 来自子组件NewcomerTable的信息，需要传递到父组件LeadNewcomer处
        }
    },
    created() {
      this.getLeadNewcomerInfo();
      this.getAchievementInfo();
      this.get_teacher_newcomer_list();
    },
  mounted(){
      if(this.GLOBAL.ident === 'admin' || this.GLOBAL.ident === 'hrbp'){ // 关掉管理员/HRBP通过导师管理界面中的导师看板查看新人的新人看板
        this.AdminToTutor = true;
      }
      this.getLeadNewcomerInfo();
      this.getAchievementInfo();
      this.get_teacher_newcomer_list();
    }
})
</script>
