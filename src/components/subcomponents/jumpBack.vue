<template>
<div></div>
</template>

<script>
export default {
  name: "jumpBack",
  inject: ["GLOBAL"],
  created(){
    switch (this.GLOBAL.selectedURL){
    case "/newcomer-manage": {
        this.$router.replace({
          path:"/newcomer-manage",
          name: "NewcomerManage"
        })
        break
      }
    case "/tutor-manage": {
        this.$router.replace({
          path: '/tutor-manage',
          name: 'TutorManage',
        })
        break
      }
    case "/train-template": {
        this.$router.replace({
          path: '/train-template',
          name: 'TrainTemplate',
        })
        break
      }
    case "/newcomer-board": {
        this.$router.replace({
          path: '/newcomer-board',
          name: 'NewcomerBoard',
        })
        break
      }
    case "/dimension-analysis": {
        this.$router.replace({
          path: '/dimension-analysis',
          name: 'DimensionAnalysis',
        })
        break
      }
    case "/lead-newcomer": {
        this.$router.replace({
          path: '/lead-newcomer',
          name: 'LeadNewcomer',
        })
        break
      }
    case "/tutor-train": {
        this.$router.replace({
          path: '/tutor-train',
          name: 'TutorTrain',
        })
        break
      }
    case "/": {
        this.$router.replace({
          path: '/',
          name: 'PersonalProfile',
        })
        break
      }
    case "/create-notification": {
        this.$router.replace({
          path: '/create-notification',
          name: 'createNotification',
        })
        break
      }
    case "/read-notification": {
        this.$router.replace({
          path: '/read-notification',
          name: 'readNotification',
        })
        break
      }
    default: {
        console.log("in jump back to / by default")
        this.$router.replace({
          path:"/",
          name: "PersonalProfile"
        })
      }
    }
  }
}
</script>

<style scoped>

</style>