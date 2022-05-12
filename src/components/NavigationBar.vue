<template>
<v-container>
  <!-- 工具栏 -->
    <v-list>
      <v-list-item class="px-2" @click="selectMenu('个人信息')">
        <v-list-item-avatar>
          <img src="/api/avatar"/>
<!--          <img :src="userInfo.userAvatarPath"/>-->
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title class="text-h6" v-text="userInfo.name"></v-list-item-title>
          <!-- bio：签名（detail：详细情况） -->
          <v-list-item-subtitle v-text="userInfo.bio"></v-list-item-subtitle>
        </v-list-item-content>
          <!-- <v-btn v-on:click="logout">
            登出
          </v-btn> -->
      </v-list-item>

    </v-list>

    <!-- 身份下拉框 -->
    <div class="text-center">
      <v-menu offset-y>
        <template v-slot:activator="{on, attrs}">
          <v-btn
            color="primary"
            dark
            v-bind="attrs"
            v-on="on"
          >
            {{ selectedPosition }}
          </v-btn>
        </template>
        <v-list>
          <v-list-item
            v-for="(item, index) in userInfo.userPositions"
            :key="index"
            @click="selectedPosition=item"
            link
          >
            <v-list-item-subtitle>{{ item }}</v-list-item-subtitle>
          </v-list-item>
        </v-list>
      </v-menu>
    </div>

  <!-- 菜单列表项 -->        
  <div style="margin-top: 15px">
    <v-list nav dense
      v-for="(item, i) in menuList"
      :key="item.id"
    >
      
      <!-- <v-list-item link
        v-for="subItem in item.subItem"
        :key="subItem.id"
        @click="selectedMenu=subItem.title"
      > -->
      <v-list-item link
        v-for="subItem in item.subItem"
        :key="subItem.id"
        @click="selectMenu(subItem.title)"
      >
        <v-list-item-icon v-if="subItem.title=='查看公告'">
          <v-badge v-if="subItem.title=='查看公告'&&notificationCount!=0"
          :content="notificationCount"
          color="red">
            <v-icon>{{ subItem.icon }}</v-icon>
          </v-badge>
          <v-icon v-if="notificationCount==0">{{ subItem.icon }}</v-icon>
        </v-list-item-icon>
        <v-list-item-icon v-else>
          <v-icon>{{ subItem.icon }}</v-icon>
        </v-list-item-icon>
        <v-list-item-title>{{ subItem.title }}</v-list-item-title>
      </v-list-item>

      <!-- 分割线，注意最后一项不加 -->
      <v-divider v-if="i!==menuList.length-1"/>

    </v-list>
  </div>

  <!-- 退出登录按钮 -->
  <div class="pa-2" style="margin-top: 20px">
    <v-btn block v-on:click="logout">
      退出登录
    </v-btn>
  </div>
</v-container>
  <!-- </v-app> -->
</template>

<script>
import COMM from '@/utils/Comm'
  export default {
    name: 'NavigationBar',

    data: () => ({
      menuList: [], // 菜单列表
      userInfo: { // 用户信息
        name: "myName",
        details: "myDescription",
        avatar: "/api/avatar",
        userAvatarPath: require("../assets/logo.png"), // 需要加上require字段
        bio: "",
        city: "北京",
        department: "管理部门",
        joinDate: "None",
        leader:"",
        employeeType: "",
        username: "username"
      },
      selectedPosition: "身份", // 下拉框选择
      selectedMenu: "", // 导航栏界面选择,
      notificationCount: 0
    }),

    props: {
      // 回调函数，NavigationBar -> App -> MainBoard
      changeInterface: {
        type: Function,
        default: () => {return () => {}}
      },
      changeLoginStatus: {
        type: Function,
        default: () => {return () => {}}
      },
      changeUser: {
        type: Function,
        default: () => {return () => {}}
      },
      feedbackUsername: {
        type: Function,
        default: () => {return () => {}}
      },
      currentUsername: { // 来自父组件App.vue的data
        type: String,
        default: 'username'
      },
      userPositions: {
        type: Array,
        default: () => ["管理员", "新人", "导师", "HRBP"],
      },
    },

    methods: {
      getUserInfo() {
        COMM.get_user_info().then(res => {
            console.log("getUserInfo success: ", res)
            this.userInfo = res.data;
            this.selectedPosition = res.data.selectedPosition
            this.feedbackUsername(res.data.username)
            console.log("this info",this.userInfo)
            console.log("now selected position:",this.selectedPosition)
        }, err => {
            console.log("getUserInfo error: ", err)
        })
      },
      logout(){
        COMM.logout().then(
            res => {
              console.log("logout success: ", res);
              this.$router.push({ path: "/" })
              this.changeLoginStatus(false);
            },
            err => {
              console.log("logout error: ", err)
            }
        )
        // this.$router.push({ path: "/" })
        // this.changeLoginStatus(false);
      },
      getMenuList() {        
        // 后端根据用户权限，获取对应菜单项数组，这里直接赋值代替
        if(this.selectedPosition === "管理员"){
          this.menuList = [
            {
              "id": 1,
              "subItem": [  
                {
                  "id": 1,
                  "title": "新人管理",
                  "icon": "mdi-account-group-outline",
                },
                {
                  "id": 2,
                  "title": "导师管理",
                  "icon": "mdi-account-multiple",
                }
              ]
            },
            {
              "id": 2,
              "subItem": [  
                {
                  "id": 1,
                  "title": "培训模板",
                  "icon": "mdi-book-open",
                },
                // {
                //   "id": 2,
                //   "title": "导师checklist",
                //   "icon": "mdi-check-underline",
                // }
              ]
            },
            {
              "id": 3,
              "subItem": [  
                {
                  "id": 1,
                  "title": "维度分析",
                  "icon": "mdi-chart-bar",
                },
                // 暂时隐藏掉
                // {
                //   "id": 2,
                //   "title": "培训公告",
                //   "icon": "mdi-message",
                // }
              ]
            },
            {
              'id': 4,
              'subItem': [
                {
                  'id': 1,
                  'title': "发布公告",
                  'icon': 'mdi-message'
                },
                {
                  "id": 2,
                  "title": "查看公告",
                  "icon": "mdi-message",
                }
              ]
            }
            // {
            //   "id": 4,
            //   "subItem": [  
            //     {
            //       "id": 1,
            //       "title": "帮助",
            //       "icon": "mdi-help-circle",
            //     }
            //   ]
            // }
          ]
        }
        else if(this.selectedPosition === "新人"){
          this.menuList = [
            {
              "id": 1,
              "subItem": [  
                {
                  "id": 1,
                  "title": "新人看板",
                  "icon": "mdi-view-dashboard",
                }
              ]
            },
            {
              "id": 2,
              "subItem": [  
                {
                  "id": 1,
                  "title": "查看公告",
                  "icon": "mdi-message",
                }
              ]
            }
            // {
            //   "id": 2,
            //   "subItem": [  
            //     {
            //       "id": 1,
            //       "title": "帮助",
            //       "icon": "mdi-help-circle",
            //     }
            //   ]
            // }
          ]
        }
        else if(this.selectedPosition === "导师"){
          this.menuList = [
            {
              "id": 1,
              "subItem": [  
                {
                  "id": 1,
                  "title": "带新看板",
                  "icon": "mdi-account-multiple-outline",
                },
                {
                  "id": 2,
                  "title": "导师培训",
                  "icon": "mdi-book-open-variant",
                }
              ]
            },
            {
              "id": 2,
              "subItem": [  
                {
                  "id": 1,
                  "title": "培训模板",
                  "icon": "mdi-book-open",
                },
              ]
            },
            {
              'id': 3,
              'subItem': [
                {
                  'id': 1,
                  'title': "发布公告",
                  'icon': 'mdi-message'
                },
                {
                  "id": 2,
                  "title": "查看公告",
                  "icon": "mdi-message",
                }
              ]
            }
            // {
            //   "id": 2,
            //   "subItem": [  
            //     {
            //       "id": 1,
            //       "title": "帮助",
            //       "icon": "mdi-help-circle",
            //     }
            //   ]
            // }
          ]
        }
        else if(this.selectedPosition === "HRBP"){
          this.menuList = [
            {
              "id": 1,
              "subItem": [  
                {
                  "id": 1,
                  "title": "新人管理",
                  "icon": "mdi-account-group-outline",
                },
                {
                  "id": 2,
                  "title": "导师管理",
                  "icon": "mdi-account-multiple",
                }
              ]
            },
            // {
            //   "id": 2,
            //   "subItem": [  
            //     {
            //       "id": 1,
            //       "title": "维度分析",
            //       "icon": "mdi-chart-bar",
            //     }
            //   ]
            // },
            {
              'id': 2,
              'subItem': [
                {
                  'id': 1,
                  'title': "发布公告",
                  'icon': 'mdi-message'
                },
                {
                  "id": 2,
                  "title": "查看公告",
                  "icon": "mdi-message",
                }
              ]
            }
            // {
            //   "id": 3,
            //   "subItem": [  
            //     {
            //       "id": 1,
            //       "title": "帮助",
            //       "icon": "mdi-help-circle",
            //     }
            //   ]
            // }
          ]
        }
      },
      selectMenu(data) {
        this.selectedMenu = data;
        if(this.selectedMenu == '查看公告')
          this.notificationCount = 0
        this.changeInterface(this.selectedMenu)
      },
      async getNotificationCount() {
        this.notificationCount = 0
        var res = await COMM.retrieve_notifications()
        res.notifications.forEach(notification => {
          if (!notification.finished) {
            this.notificationCount++
          }
        });
        console.log(this.notificationCount)
      }
   },
    
    created() {
      this.getUserInfo();
      this.getMenuList();
      this.getNotificationCount()
    },

    watch: {
      selectedPosition(newName) {
        var switchTo
        switch(newName) {
          case "管理员": switchTo = "admin"; break
          case "导师": switchTo = "teacher"; break
          case "新人": switchTo = "newcomer"; break
          case "HRBP": switchTo = "hrbp"; break
          default: return
        }
        COMM.switchRole(switchTo).then(
            (response) => {
              console.log(response.data.data)
              this.changeUser(switchTo)
            },
            err => {console.log(err.data.data)}
        );
        this.getMenuList();
      },
      // selectedMenu() { // 发送导航栏选中界面的信息给App.vue
      //   this.changeInterface(this.selectedMenu) // 回调函数
      // },
      // App.vue传来的用户名，用于向后端获取用户信息
      currentUsername() {
        this.getUserInfo()
      },
    }

  }
</script>