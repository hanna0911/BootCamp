<template>
  <el-dialog
      style="text-align: center"
      title="写带新记录"
      :visible="dialogVisible"
      @close="this.Close"
      width="70%"
  >
    <el-table
        :data="tableData"
        height="250"
        border
        style="width: 100%">
      <el-table-column
          label="记录时间"
          width="180">
        <template slot-scope="scope">
          {{scope.row.commitTime.split('T')[0]}} {{scope.row.commitTime.split('T')[1].split('!')[0]}}
        </template>
      </el-table-column>
      <el-table-column
          prop="content"
          label="记录内容">
      </el-table-column>
    </el-table>

    <el-form label-width="80px" v-if="this.GLOBAL.ident==='teacher'">
      <el-form-item label="写记录">
        <el-input type="textarea" placeholder="recode" v-model="content" :span="8"></el-input>
      </el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
      <el-button v-on:click="Close">取 消</el-button>
      <el-button type="primary"
                 v-on:click="submit"
      >确 定</el-button>
    </span>
  </el-dialog>
</template>

<script>

export default {
  name: "RecodeDialog",
  props: {
    dialogVisible: {type: Boolean, default: () => true},
    Close: {type: Function, default: () => {return () => {}},},
    send:{type: Function, default: () => {return () => {}},},
    tableData:[]
  },
  data() {
    return {
      content: "",
    }
  },
  inject: ["GLOBAL"],
  methods: {
    submit(){
      this.send(this.content);
      this.Close();
      this.content = ""
    },
  },
  created() {
  },
  mounted() {

  }
}
</script>