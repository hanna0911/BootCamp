<template>
    <!-- 这里改用router来显示子组件，因此与NewcomerManage相关内容均被暂时注释掉了 -->
    <router-view/> 
    <!-- 如果要取消router的访问方式，需要将主界面的子组件全部罗列在此处，如下： -->
    <!-- <NewcomerManage ref="newcomer-manage" v-show="newcomermanageVisible"/> -->
</template>

<script>
// import NewcomerManage from "./NewcomerManage.vue" // 非router显示
export default ({
    name: "MainBoard",
    inject: ["GLOBAL"],
    components: {
        // NewcomerManage, // 非router显示
    },
    props: {
        // currentInterface: String, // 来自父组件App.vue的data
        // currentUser: String, // 来自父组件App.vue的data
    },
    data: () => ({
        /*
            设置组件的可显示性
            为确保无某组件权限的用户通过url直接跳转到其无权访问的组件，因此需要对组件的visibility进行严格管控
            详见currentUser()
        */
        newcomermanageVisible: false,
        tutormanageVisible: false,
        traintemplateVisible: false,
        newcomerboardVisible: false, 
        trainnoticeVisible: false,
        // helppageVisible: false,
        dimensionanalysisVisible: false,
        leadnewcomerVisible: false,
        tutortrainVisible: false,
        // TODO
    }),
    watch: {
        /*
        currentInterface() {
            switch(this.currentInterface){
                case "新人管理": {
                    this.$router.push({ path: "/newcomer-manage"})
                    break
                }
                case "导师管理": {
                    this.$router.push({ path: "/tutor-manage" })
                    break
                }
                case "培训模板": {
                    this.$router.push({ path: "/train-template" })
                    break
                }
                case "新人看板": {
                    this.$router.push({ path: "/newcomer-board" })
                    break
                }
                case "培训公告": {
                    this.$router.push({ path: "/train-notice" })
                    break
                }
                // case "帮助": {
                //      this.$router.push({ path: "/help-page" })
                //     break
                // }
                case "维度分析": {
                    this.$router.push({ path: "/dimension-analysis" })
                    break
                }
                case "带新看板": {
                    this.$router.push({ path: "/lead-newcomer" })
                    break
                }
                case "导师培训": {
                    this.$router.push({ path: "/tutor-train" })
                    break
                }
                case "个人信息": {
                    this.$router.push({ path: "/" })
                    break
                }
                // TODO
                case "发布公告": {
                    this.$router.push({ path: "/create-notification"})
                    break
                }
                case "查看公告": {
                    this.$router.push({ path: "/read-notification"})
                    break
                }
                default: {
                    console.log("interface -> default")
                    break
                }
            }
        },
        */
        /*
        currentUser() {
             
            //    当用户权限改变时，重新设置组件的可显示性
            //    为防止无某组件权限的用户通过url直接跳转到其无权访问的组件，因此需要对组件的visibility进行严格管控
            
            // 先将所有的组件显示都置成false（目前只写了这些，请写其他组件的同学进行改动）
            this.newcomermanageVisible = false
            this.tutormanageVisible = false
            this.traintemplateVisible = false
            this.newcomerboardVisible = false
            this.trainnoticeVisible = false
            this.helppageVisible = false
            this.dimensionanalysisVisible = false
            this.tutortrainVisible = false
            // TODO
            switch(this.currentUser){ // 再根据user的权限基于“访问许可”（用是否能显示组件来实现）
                case "管理员": {
                    this.newcomermanageVisible = true // 新人管理
                    this.tutormanageVisible = true // 导师管理
                    this.traintemplateVisible = true // 培训模板
                    // this.trainnoticeVisible = true // 培训公告 // 暂时隐藏掉
                    // this.helppageVisible = true //帮助
                    this.dimensionanalysisVisible = true // 维度分析
                    // TODO
                    break
                }
                case "新人": {
                    this.newcomerboardVisible = true // 新人看板
                    // this.helppageVisible = true // 帮助
                    break
                }
                case "导师": {
                    // this.helppageVisible = true //帮助
                    this.leadnewcomerVisible = true // 带新看板
                    this.tutortrainVisible = true // 导师培训
                    this.traintemplateVisible = true // 培训模板，导师给新人查看模板
                    break
                }
                case "HRBP": {
                    // this.helppageVisible = true //帮助
                    // TODO
                    break
                }
            }
        }*/
    }, 
    methods: {
        changeInterface(data){
            switch(data){
                case "新人管理": {
                    // this.$router.push({ path: "/newcomer-manage"})
                    this.GLOBAL.selectedURL = "/newcomer-manage"
                    break
                }
                case "导师管理": {
                    // this.$router.push({ path: "/tutor-manage" })
                    this.GLOBAL.selectedURL = "/tutor-manage"
                    break
                }
                case "培训模板": {
                    // this.$router.push({ path: "/train-template" })
                    this.GLOBAL.selectedURL = "/train-template"
                    break
                }
                case "新人看板": {
                    // this.$router.push({ path: "/newcomer-board" })
                    this.GLOBAL.selectedURL = "/newcomer-board"
                    break
                }
                case "培训公告": {
                    // this.$router.push({ path: "/train-notice" })
                    this.GLOBAL.selectedURL = "/train-notice"
                    break
                }
                // case "帮助": {
                //      this.$router.push({ path: "/help-page" })
                //     break
                // }
                case "维度分析": {
                    // this.$router.push({ path: "/dimension-analysis" })
                    this.GLOBAL.selectedURL = "/dimension-analysis"
                    break
                }
                case "带新看板": {
                    // this.$router.push({ path: "/lead-newcomer" })
                    this.GLOBAL.selectedURL = "/lead-newcomer"
                    break
                }
                case "导师培训": {
                    // this.$router.push({ path: "/tutor-train" })
                    this.GLOBAL.selectedURL = "/tutor-train"
                    break
                }
                case "个人信息": {
                    // this.$router.push({ path: "/" })
                    this.GLOBAL.selectedURL = "/"
                    break
                }
                // TODO
                case "发布公告": {
                    // this.$router.push({ path: "/create-notification"})
                    this.GLOBAL.selectedURL = "/create-notification"
                    break
                }
                case "查看公告": {
                    // this.$router.push({ path: "/read-notification"})
                    this.GLOBAL.selectedURL = "/read-notification"
                    break
                }
                default: {
                    console.log("interface -> default")
                    this.GLOBAL.selectedURL = "/"
                    break
                }
            }
            console.log("to jump back actual to", this.GLOBAL.selectedURL)
            this.$router.replace({
              path:"/jumpBack",
              name:"jumpBack"
            })
        },
    }
})
</script>