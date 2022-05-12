<template>
<v-container>
    <!--选择推送对象管理或推送内容管理-->
    <v-btn-toggle v-model="showView" group tile color="gray">
        <v-btn value="groupManage">推动对象管理</v-btn>
        <v-btn value="messageManage">推送内容管理</v-btn>
    </v-btn-toggle>
    <!-- 显示推送内容管理 -->
    <v-row v-if="messageVisible">
        <v-col v-for="message in messageInfo" :key="message.content" cols="12">
            <v-card>
            <v-card-text>
                 <div style="display:flex; margin-top: 3px; font-size: small;color: grey">
                    <span class="messageInfo-sender" style="padding: 4px;">{{message.sender}}</span>
                    <span class="messageInfo-datatime" style="padding: 4px;">{{datetime(message.timestamp)}}</span>
                    <v-btn color="grey">撤回</v-btn>
                    <v-btn color="grey">阅读详情</v-btn>
                </div>
                <div class="text-h4">{{message.title}}</div>
                <div class="text-h6">{{message.content}}</div>
                <div class="text-h12">发送至：{{message.receiver}}</div>
            </v-card-text>
            </v-card>
        </v-col>
    </v-row>
    <!--显示推送对象管理视图-->
    <v-row v-if="groupVisible">   
        <v-col v-for="group in groupInfo" :key="group.name" clos="16">
            <v-card>
            <v-card-text>
                <div style="diplay:flex; marign-top: 2px font-size: large">
                    <span class="groupInfo-name" style="padding: 6px">{{group.name}}</span>
                    <span class="groupInfo-creator" style="padding: 6px">{{group.creator}}</span>
                    <span class="groupInfo-type" style="padding: 6px">{{group.receiverType}}</span>
                    <v-btn color="grey">查看</v-btn>
                    <v-btn color="grey">复制</v-btn>
                </div>
            </v-card-text>
            </v-card>
        </v-col>
    </v-row>
</v-container>    
</template>

<script>

export default ({
    name: "TrainNotice",
    data() {
        return {
            name:"",
            showView: "contentManage",//为内容管理和对象管理
            messageVisible: false,
            groupVisible: true,
            messageInfo:[
                {
                    sender: 'Programmer',
                    title: '第一条推送',
                    content: '这是对推送显示的测试',
                    timestamp: new Date().getTime(),
                    receiver: '全员'
                },
                {
                    sender: 'Programmer',
                    title: '第二条推送',
                    content: '这仍然是对推送显示的测试',
                    timestamp: new Date().getTime(),
                    receiver: '全员'
                }
            ],
            groupInfo:[
                {
                    name: '群组1',
                    creator: 'Programmar',
                    receiverType: '研发部门-导师'
                },
                {
                    name: '群组2',
                    creator: 'Programmar',
                    receiverType: '研发部门-所有新人' 
                }
            ]
        }
    },
    methods: {
        datetime: function(timestamp) {
            var d = new Date()
            d.setTime(timestamp > 1e10 ? timestamp : timestamp * 1000)
            return d.toLocaleString()
        }
    },
    watch: {
        "showView": {
            handler(newName) {
                this.messageVisible = (newName === "messageManage")
                this.groupVisible = (newName === "groupManage")
            }
        }
    }
})
</script>
