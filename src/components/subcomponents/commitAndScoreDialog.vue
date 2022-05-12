<template>
  <el-dialog
      style="text-align: center"
      title="反馈评价"
      :visible="dialogVisible"
      @close="this.Close"
      width="80%">
    <el-form label-width="80px">
      <el-form-item label="导师分数:">
        <p align="left">{{this.commitAndScoreData.teacherScore}}</p>
      </el-form-item>
      <el-form-item label="导师评价:">
        <p align="left">{{this.commitAndScoreData.newcomerToTeacher}}</p>
      </el-form-item>

      <el-form-item label="新人分数:">
        <p align="left">{{this.commitAndScoreData.newcomerScore}}</p>
      </el-form-item>
      <el-form-item label="新人评价:">
        <p align="left">{{this.commitAndScoreData.teacherToNewcomer}}</p>
      </el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
      <el-button v-on:click="Close">关闭</el-button>
    </span>
  </el-dialog>
</template>

<script>
export default {
  name: "commitAndScoreDialog",
  props: {
    dialogVisible: {type: Boolean, default: () => true},
    Close: {type: Function, default: () => {return () => {}},},
    commitAndScoreData:{
      teacherScore: 2,
      newcomerScore: 2,
      newcomerToTeacher: "nice",
      teacherToNewcomer: "nice"
    }
  },
  data() {
    return {
      teacher:{},
      newcoemr:{},
    }
  },

}
</script>

<style scoped>

</style>