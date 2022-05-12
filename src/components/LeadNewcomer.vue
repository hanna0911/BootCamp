<template>
<v-container>
    <div v-if="!newcomerBoardVisible">
        <h2 class="px-4 pt-4 pb-3 font-weight-black">带新看板</h2>
        <!-- 带新看板 -->
        <lead-newcomer-sub :tutorIdentity="tutorIdentity" :checkNewcomerBoard="checkNewcomerBoard"/>
    </div>
    <newcomer-board-edit v-else :closeNewcomerBoard="closeNewcomerBoard" :newcomerIdentity="newcomerIdentity" :showAudience="'newcomer'"></newcomer-board-edit>


</v-container>
</template>

<script>
import LeadNewcomerSub from "./subcomponents/LeadNewcomerSub.vue"
import NewcomerBoardEdit from "./subcomponents/NewcomerBoardEdit.vue"

export default ({
    name: "LeadNewcomer",
    components: {
        LeadNewcomerSub,
        NewcomerBoardEdit,
    },
    data() {
        return {
            newcomerBoardVisible: false, // 显示新人看板
            newcomerIdentity: {}, // 该新人的所有数据在此字典中，辅助用于从后端获取该新人的数据
        }
    },
    methods: {
        checkNewcomerBoard(data) {
            this.newcomerIdentity = data;
            this.newcomerBoardVisible = true;
        },
        closeNewcomerBoard() { 
            // 提供给子组件NewcomerBoardEdit的回调函数
            this.newcomerBoardVisible = false;
        },
    }
})
</script>
