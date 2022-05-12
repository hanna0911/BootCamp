<template>
  <v-parallax
    dark
    src="../assets/welcomePage.png"
    height="900"
    speed="0.2"
    transparent="100"
  >
    <v-row
      align="center"
      justify="center"
    >
      <v-col
        class="text-center"
        cols="12"
      >
        <h2 class="text-h2 font-weight-thin mb-4" style="color: white">
          BootCamp
        </h2>
        <h6 class="text-h6 font-weight-thin mb-4" style="color: white">
            an optimal training platform for newcomers <br> grasping new workflow and procedures in a blink
        </h6>
       
    <!-- 注册界面 start -->
    <v-dialog
      v-model="signupDialog"
      persistent
      max-width="600px"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          color="primary"
          dark
          v-bind="attrs"
          v-on="on"
        >
          注册
        </v-btn>
      </template>
      <v-card>
        <v-card-title>
          <span class="text-h5">注册</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col
                cols="12"
                sm="6"
                md="4"
              >
                <v-text-field
                  label="姓名*"
                  required
                  :rules="rules.requiredRules"
                  v-model="signupNameInput"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  label="用户名*"
                  hint="仅允许包含英文字母、数字，长度不超过20个字符"
                  :rules="rules.usernameRules"
                  required
                  v-model="signupUsernameInput"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  label="密码*"
                  type="password"
                  hint="需要包含大小写英文字母、数字、特殊字符，长度8~20个字符"
                  :rules="rules.passwordRules"
                  required
                  v-model="signupPasswordInput"
                ></v-text-field>
              </v-col>
              <v-col
                cols="12"
                sm="6"
              >
              
                <!-- TODO: 修改部门列表items -->
                <v-autocomplete
                  :items="['管理部门', '项目部门', '策划部门', '技术部门', '财务部门']"
                  label="部门"
                  v-model="signupDeptInput"
                ></v-autocomplete>
              </v-col>
              <v-col
                cols="12"
                sm="6"
              >
                
                <!-- TODO: 修改城市列表items，考虑是否要修改为先选省、再选市 -->
                <v-autocomplete
                  :items="['北京', '上海', '广州', '深圳', '天津', '南京']"
                  label="城市"
                  v-model="signupCityInput"
                ></v-autocomplete>
              </v-col>
            </v-row>
          </v-container>
          <small>*必填</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="blue darken-1"
            text
            @click="signupDialog = false"
          >
            取消
          </v-btn>
          <v-btn
            color="blue darken-1"
            text
            @click="join"
          >
            注册
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- 注册界面 end -->

    <!-- 登录界面 start -->
    <v-dialog
      v-model="dialogLoginPanel"
      persistent
      max-width="600px"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          class="ma-2"
          outlined
          color="white"
          dark
          v-bind="attrs"
          v-on="on"
        >
          登录
        </v-btn>
      </template>
      <v-card>
        <v-card-title>
          <span class="text-h5">登录</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  label="用户名*"
                  v-model="usernameInput"
                  :rules="rules.requiredRules"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  label="密码*"
                  type="password"
                  v-model="passwordInput"
                  :rules="rules.requiredRules"
                  required
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
          <small>*必填</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="blue darken-1"
            text
            @click="dialogLoginPanel = false"
          >
            Cancel
          </v-btn>
          <v-btn
            color="blue darken-1"
            text
            @click="login"
            @keyup.enter="login"
          >
            Login
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- 登录界面 end -->

    <!-- 登录失败界面 start -->
      <v-dialog
        v-model="logindialogError"
        max-width="500px"
      >
        <v-card>
          <v-card-title>
            <span>Invalid Username or Password!</span>
            <v-spacer></v-spacer>
          </v-card-title>
          <v-card-actions>
            <v-btn
              color="primary"
              text
              @click="logindialogError = false"
            >
              Close
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <!-- 登录失败界面 end -->

      </v-col>
    </v-row>
  </v-parallax>
</template>

<script>
import COMM from "@/utils/Comm"
export default ({
    name: 'NavigationBar',
    props: {
        changeLoginStatus: {
            type: Function,
            default: () => {
                return () => {}
            }
        },
        changeRoleList: {
          type: Function,
          default: () => {
            return () => {}
          }
        },
    },
    data: () => ({
        dialogLoginPanel: false, // 登录界面显示
        logindialogError: false, // 登录错误弹框显示
        usernameInput: "", // 登录用户名input
        passwordInput: "", // 登录密码input
        signupNameInput: "", //注册姓名input
        signupUsernameInput: "", //注册用户名input
        signupPasswordInput: "", //注册密码input
        signupCityInput: "", //注册城市input
        signupDeptInput: "", //注册部门input
        signupDialog: false, // 注册界面显示
        rules: { // TODO: 后期可根据username和password特性进行修改
            requiredRules: [value => !!value || "必填项"],
            mincharRules: [value => (value && value.length >= 3) || '长度至少3位'],
            passwordRules: [(value) => (/^(?![A-z0-9]+$)(?=.[^%&',;=?$\x22])(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,20}$/).test(value) || "必填项，至少包含大小写字母、数字、特殊字符，长度8~20位"],
            usernameRules: [(value) =>  !!value && (/^[a-zA-Z0-9]{0,20}$/).test(value) || '必填项，只能包含字母、数字，长度不超过20位']
        },
    }),
    methods: {
        login() { // 登录，与后端 /login 接口进行交互
            // 在后端Models中查找用户名、密码是否匹配
            COMM.login(this.usernameInput, this.passwordInput).then(res => {
                // if passed login authentication                
                this.dialogLoginPanel = false;
                this.changeLoginStatus(true);  // --登录配置相关--：App.vue调用函数（回调函数）

                // 把用户名传递给App.vue（回调），再通过App.vue传递data给NavigationBar.vue的props
                // this.passUsername(this.usernameInput);

                this.changeRoleList(res.role_list)
                this.$router.push({ path: "/" })

                console.log("login success: ", res);
            }, (err) => {
                // didn't pass authentication
                this.logindialogError = true;
                this.changeLoginStatus(false); // App.vue调用函数（回调函数）
                console.log("login error",err);
            })
        },
        join() { // 注册，与后端 /join 接口进行交互
            // 在后端查找有没有重名的用户，如果没有则创建新用户
            const personalInfo={"name":this.signupNameInput, "dept":this.signupDeptInput, "city":this.signupCityInput}
            COMM.createAccount(this.signupUsernameInput, this.signupPasswordInput, personalInfo).then(res => {
                //注册成功（码同login）
                this.signupDialog = false
                this.changeLoginStatus(true)  // --登录配置相关--：App.vue调用函数（回调函数）

                // 把用户名传递给App.vue（回调），再通过App.vue传递data给NavigationBar.vue的props
                // this.passUsername(this.usernameInput)

                console.log("sign up success: ", res)
            }, err => {
                //注册失败
                this.logindialogError = true
                this.changeLoginStatus(false)  // App.vue调用函数（回调函数）
                console.log("sign up error: ", err)
            })
        },
    }
})
</script>