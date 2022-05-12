<template>
  <v-container>
    <h2 class="px-4 pt-4 pb-3 font-weight-black">我的公告</h2>
      <v-dialog v-model="readNotificationDialog" >
        <v-card>
          <v-card-title>公告内容</v-card-title>
          <v-divider></v-divider>
          <v-card-text style="height: 500px;">
            <h2 class="px-4 pt-4 pb-3 font-weight-black">{{toReadNotification.title}}</h2>
            <h3 class="px-4 pt-4 pb-3 font-weight-black">发布者：{{renderAuthorRole(toReadNotification.authorRole)}} {{toReadNotification.author}}</h3>
            <h3 class="px-4 pt-4 pb-3 font-weight-black">发布时间：{{renderTimestamp(toReadNotification.releaseTime)}}</h3>
            <h3 class="px-4 pt-4 pb-3 font-weight-black">内容</h3>
            <div style="margin-left: 50px">
              {{toReadNotification.content}}
            </div>
          </v-card-text>
        </v-card>
        <v-btn @click="finishReading(toReadNotification.notificationID)">
          返回
        </v-btn>
      </v-dialog>
    <v-spacer></v-spacer>
    <v-btn @click="getNotifications">
      <v-icon>
        mdi-refresh
      </v-icon>
    </v-btn>
    <h3 class="px-4 pt-4 pb-3 font-weight-black">未读</h3>
    <v-list>
      <template v-for="(item, index) in unreadNotifications">
        <v-list-item :key="item.notificationID">
          <template>
            <v-list-item-content>
              <v-list-item-title v-text="item.title"></v-list-item-title>
              <v-list-item-subtitle
                class="text--primary"
                v-text="genSubtitle(item.author, item.authorRole, item.releaseTime)"
              ></v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-action>
                <v-toolbar dark color="primary">
                  <v-btn icon dark @click="readNotification(index, 'unread')" min-width="100">
                    点击阅读
                  </v-btn>
                </v-toolbar>
            </v-list-item-action>
          </template>
        </v-list-item>
      </template>
    </v-list>
    <h3 class="px-4 pt-4 pb-3 font-weight-black">已读</h3>
    <v-list>
      <template v-for="(item, index) in finishedNotifications">
        <v-list-item :key="item.notificationID">
          <template>
            <v-list-item-content>
              <v-list-item-title v-text="item.title"></v-list-item-title>
              <v-list-item-subtitle
                class="text--primary"
                v-text="genSubtitle(item.author, item.authorRole, item.releaseTime)"
              ></v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-action>
                <v-toolbar dark color="primary">
                  <v-btn icon dark @click="readNotification(index, 'finished')" min-width="100">
                    点击阅读
                  </v-btn>
                </v-toolbar>
            </v-list-item-action>
          </template>
        </v-list-item>
      </template>
    </v-list>
    <template v-if="isManager">
      <h3 class="px-4 pt-4 pb-3 font-weight-black">已发送</h3>
      <v-list>
        <template v-for="(item, index) in authoredNotifications">
          <v-list-item :key="item.notificationID">
            <template>
              <v-list-item-content>
                <v-list-item-title v-text="item.title"></v-list-item-title>
                <v-list-item-subtitle
                  class="text--primary"
                  v-text="genSubtitle(item.author, item.authorRole, item.releaseTime)"
                ></v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                  <v-toolbar dark color="primary">
                    <v-btn icon dark @click="deleteNotification(index)" min-width="100">
                      删除这条公告
                    </v-btn>
                  </v-toolbar>
              </v-list-item-action>
            </template>
          </v-list-item>
        </template>
      </v-list>
    </template>
  </v-container>
</template>
<script>

import COMM from "@/utils/Comm";
export default ({
    name: 'AssigneeTable',
    inject: ['GLOBAL'],
    components: {
    //   CommitDialog
    },
    data() {
      return {
        unreadNotifications: [],
        finishedNotifications: [],
        authoredNotifications: [],
        readNotificationDialog: false,
        toReadNotification: {
          title: "",
          author: "",
          authorRole: "",
          releaseTime: "",
          content: "",
          notificationID: "",
          finished: "", 
        },
        readingUnread: false,
        isManager: false
      }
    },
    props: {
    },
    methods: {
      genSubtitle(author, authorRole, releaseTime) {
        return "发布者：" + this.renderAuthorRole(authorRole) + " " + author + "  发布时间：" + this.renderTimestamp(releaseTime)
      },
      readNotification(index, type) {
        var dataset = []
        if (type == 'unread') {
          dataset = this.unreadNotifications
          this.readingUnread = true
        }
        else {
          dataset = this.finishedNotifications
          this.readingUnread = false
        }
        console.log(dataset)
        this.toReadNotification = dataset[index]
        this.readNotificationDialog = true
      },
      async getNotifications() {
        this.unreadNotifications = []
        this.finishedNotifications = []
        this.authoredNotifications = []
        var res = await COMM.retrieve_notifications()
        res.notifications.forEach(notification => {
          if (!notification.finished) {
            this.unreadNotifications.push(notification)
          }
          else {
            this.finishedNotifications.push(notification)
          }
        });
        console.log(this.unreadNotifications)
        console.log(this.finishedNotifications)
        res = await COMM.getCurRole()
        var role = res.role
        if (role != 'newcomer') {
          this.isManager = true
          res = await COMM.retrieve_authored_notification()
          this.authoredNotifications = res.notifications
        }
      },
      async finishReading(notificationID) {
        this.readNotificationDialog = false
        if (!this.readingUnread) {
          return
        }
        var res = await COMM.finish_notification(notificationID)
        if (res.result == 'success') {
          this.getNotifications()
        }
      },
      async deleteNotification(index) {
        var targetNotification = this.authoredNotifications[index]
        var postData = {
          'action': 'delete notification',
          'notificationID': targetNotification.notificationID
        }
        var res = await COMM.delete_notification(postData)
        if (res.result == 'success')
          alert('删除成功')
        this.getNotifications()
      },
      renderAuthorRole(role) {
        if(role === 'admin')
          return '管理员'
        else if (role === 'HRBP')
          return 'HRBP'
        else if (role ==='teacher')
          return '导师'
        else
          return 'BOOTCAMP'
      },
      renderTimestamp(timestamp) {
        if (timestamp[timestamp.length - 4] == '.')
          return timestamp.replace('T', ' ').slice(0, -4)
        else
          return timestamp.replace('T', ' ')
      }
    },
    mounted() {
      this.getNotifications()
    },
})
</script>
