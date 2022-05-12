<template>
    <v-container>
        <v-card
            class="mx-auto"
            elevation="0"
        >
            <v-list-item three-line>
                <v-list-item-content>
                    <div class="text-overline" style="margin-bottom: -10px">
                        具有权限:&nbsp;
                        <span v-for="(identity, i) in userInfo.userPositions" :key="i">
                            {{ identity }}
                        </span>
                    </div>
                    <div class="text-overline mb-4">
                        {{ userInfo.registrationDate.replace('T', ' ').split(' ')[0] }} 加入
                    </div>
                    <v-list-item-title class="text-h5 mb-2">
                        {{ userInfo.name }}
                    </v-list-item-title>
                    <v-list-item-subtitle>
                        <strong>{{ userInfo.bio }}</strong>
                    </v-list-item-subtitle>
                    <v-list-item-subtitle>
                       详细信息：{{ userInfo.detail }}
                    </v-list-item-subtitle>
                </v-list-item-content>
                <v-list-item-avatar tile size="150">
                    <img src="/api/avatar"/>
                </v-list-item-avatar>
            </v-list-item>

            <v-card-text>
                <v-chip-group multiple>
                    <v-chip color="primary" label outlined>
                        <v-icon left>mdi-tools</v-icon>
                        {{ userInfo.department }}
                    </v-chip>
                    <v-chip color="success" label outlined>
                        <v-icon left>mdi-city</v-icon>
                        {{ userInfo.city }}
                    </v-chip>
                    <v-chip color="black" label outlined>
                        <v-icon left>mdi-nintendo-switch</v-icon>
                        {{ userInfo.employed }}</v-chip>
                </v-chip-group>
            </v-card-text>
        </v-card>

    </v-container>
</template>

<script>
import COMM from '@/utils/Comm.js'
export default ({
    name: 'PersonalProfile',
    props: {
        
    },
    data: () => ({
       userInfo: {},
    }),
    methods: {
        getUserInfo() {
            // TODO: 后端获取用户信息（没有找到后端的接口，是这个吗？感觉不是。。。先凑合）
            COMM.get_user_info().then(res => {
                // bug: 登录状态无法解决的话，会一直走err（目前选择了注释掉后端newcomer_info()中session判断相关内容）
                this.userInfo = res.data;
            }, err => {
                console.log("getUserInfo error: ", err)
            })
        },
    },
    mounted() {
        this.getUserInfo();
    },
})
</script>