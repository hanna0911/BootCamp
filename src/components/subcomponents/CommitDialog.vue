<template>
  <el-dialog
      style="text-align: center"
      title="反馈评价"
      :visible="dialogVisible"
      @close="this.Close"
      width="80%">
    <el-form label-width="80px">
      <el-form-item label="分数">
        <el-input :placeholder="oldScore"
                  type="number"
                  oninput="if(value>10)value=10;if(value<0)value =0"
                  v-model="score"></el-input>
      </el-form-item>
      <el-form-item label="评价">
        <el-input type="textarea" :placeholder="this.oldCommit" v-model="commits"></el-input>
      </el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
      <el-button v-on:click="Close">取 消</el-button>
      <el-button type="primary"
                 v-on:click="commit"
      >确 定</el-button>
    </span>
  </el-dialog>
</template>

<script>


export default {
  name: "CommitDialog",
  props: {
    dialogVisible: {type: Boolean, default: () => true},
    Close: {type: Function, default: () => {return () => {}},},
    send:{type: Function, default: () => {return () => {}},},
    oldCommit:{type:String, default:() => ""},
    oldScore: {type:Number, default: () => 0}
  },
  data() {
    return {
      score: "",
      commits: ""
    }
  },
  methods: {
    commit(){
      this.send(this.score, this.commits);
      this.Close();
      this.commits = ""
    }
  },
  mounted() {

  }
}
</script>