<template>
  <v-app>
    <!-- <WelcomePage v-if="!loginSuccessful" :changeLoginStatus="changeLoginStatus" :passUsername="passUsername" :changeRoleList="changeRoleList"/> -->
    <WelcomePage v-if="!loginSuccessful" :changeLoginStatus="changeLoginStatus" :changeRoleList="changeRoleList"/>
    <div v-else>
      <v-navigation-drawer app permanent>
        <NavigationBar :changeInterface="changeInterface" :changeUser="changeUser" :change-login-status="changeLoginStatus"
                       :userPositions="roleList" :feedback-username="getUsername" ref="navigation-bar"/>
      </v-navigation-drawer>
      <v-main>
        <!-- 路由 -->
        <!-- <router-view v-else/> -->
        <!-- <MainBoard :currentInterface="currentInterface"/> -->
        <MainBoard ref="MainBoard"/>
      </v-main>
    </div>
  </v-app>
</template>

<script>
import NavigationBar from './components/NavigationBar.vue';
import WelcomePage from './components/WelcomePage.vue';
import MainBoard from './components/MainBoard.vue'
import COMM from './utils/Comm';
import router from './router/index.js'

export default {
  name: 'App',

  components: {
    NavigationBar,
    WelcomePage,
    MainBoard,
  },

  data: () => ({
    loginSuccessful: false,  // --登录配置相关--：用来控制登录状态（是v-if显示WelcomePage欢迎页的判断条件）
    // currentInterface: "", // 传给子组件MainBoard
    // currentUser: "", // 传给子组件MainBoard
    globalVar:{
      ident:"",
      username:"",
      contentDisplayAddif: false,  // ContentDisplay是否显示添加按钮
      contentDisplayUser: false,  // ContentDisplay是否显示学习状态
    },
    currentUsername: 'username', // 传给子组件NavigationBar
    roleList: [],  // 可选角色的列表
  }),

  watch: {
    // 如果路由有变化，会再次执行该方法（试图换用其他方法来判断？）
    '$route': 'fetchData'
  },

  created: function(){
      /*
        --登录配置相关--
        TODO: 退出登录按钮（后端api/login接口还没有做好，是个假的？还是我理解错了）
      */
    // this.currentInterface = "个人信息";
    // this.$refs.MainBoard.changeInterface('个人信息');
    this.fetchData()
  },
  provide(){
    return{
      GLOBAL: this.globalVar
    }
  },

  methods: {
    fetchData () { 
      /*
        --登录配置相关--
        
        功能：当发生url变化时执行，请求后端来得知当前登录状态是否合法，不合法则登出，合法则保持登录状态

        这里不需要前端设置cookie了，cookie由后端设置，前端跳转url时候请求后端token判断是否合法即可（我自己的理解）
        下面的内容是yzt/smz写的（应该），基本没有做改动（除了一些回调的bug进行了修复）
      */
      COMM.getToken().then(res => {
        console.log("response data: ", res)
        // this.loginSuccessful = true
        this.loginSuccessful = (res.result === "login success")
        this.changeRoleList(res.role_list)
      }, err => {
        console.log("token error", err)
        // this.logindialogError = true
        // this.changeLoginStatus(false)  // bug修复：这里不能用App.vue调用函数（回调函数）！！回调函数是给子组件调用的
        // this.loginSuccessful = false  // bug修复：直接改父组件App.vue里的data就可以啦！
      })
    },

    /*
      接收NavigationBar的信息，后传给子组件MainBoard
      即 NavigationBar -> App -> MainBoard
    */
    changeUser: function(data) {
      // this.currentUser = data // 当前身份（管理员、新人、导师、HRBP）传给子组件MainBoard
      this.globalVar.ident = data
      sessionStorage.setItem('user', data)

    },
    getUsername(data){this.globalVar.username = data},

    changeInterface: function(data) {
      // this.currentInterface = data // 当前点击的主界面信息，传给子组件MainBoard
      this.$refs.MainBoard.changeInterface(data) // 直接调用子组件MainBoard信息
    },

    /*
      接收WelcomeBoard的信息，后传给子组件NavagationBar
    */
    // passUsername: function(data) {
    //   this.currentUsername = data
    // },

    /*
      改变loginSuccessful的值
    */
    changeLoginStatus: function(isLogin) {  // 提供给WelcomePage调用的回调函数
      /* 
        只有WelcomePage传来的isLogin==true时才需要执行fetchData进一步确认登录合法性
      */
      if(isLogin) this.fetchData()
      else {
        this.loginSuccessful=false;
        console.log("loginStatus: false!!!")
      }
    },
    changeRoleList: function(list) {
      this.roleList = list;
      console.log("role list is:", this.roleList)
    },
  },
};

/*
解决路由跳转拦截问题，以后有需要修改的权限组件显示，请直接在这里改！
*/
router.beforeEach(function(to, from, next){
	console.log('路由跳转之前拦截', to, from)
  var user = sessionStorage.getItem('user');
  var jumpto = to.name;
  console.log(user, jumpto)
  switch(user){
    case 'newcomer':
      if(jumpto === 'NewcomerBoard' || jumpto === 'readNotification' || jumpto === 'PersonalProfile'){
        next();
      }
      else{
        router.push({ path: "/"});
      }
      break;
    case 'admin':
      if(jumpto === 'PersonalProfile' || jumpto === 'NewcomerManage' || jumpto === 'TutorManage' || jumpto === 'TrainTemplate' || jumpto === 'DimensionAnalysis' || jumpto === 'createNotification' || jumpto === 'readNotification'){
        next();
      }
      else{
        router.push({ path: "/"});
      }
      break;
    case 'hrbp':
      if(jumpto === 'PersonalProfile' || jumpto === 'NewcomerManage' || jumpto === 'TutorManage' || jumpto === 'createNotification' || jumpto === 'readNotification'){
        next();
      }
      else{
        router.push({ path: "/"});
      }
      break;
    case 'teacher':
      if(jumpto === 'PersonalProfile' || jumpto === 'LeadNewcomer' || jumpto === 'TutorTrain' || jumpto === 'TrainTemplate' || jumpto === 'createNotification' || jumpto === 'readNotification'){
        next();
      }
      else{
        router.push({ path: "/"});
      }
      break;
    default:
      break;
  }
	
})
</script>