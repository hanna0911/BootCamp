import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import router from './router'
import ElementUI from 'element-ui';
import VueMeta from "vue-meta";
import 'element-ui/lib/theme-chalk/index.css';
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css';
import * as echarts from 'echarts'; // 引入echarts

Vue.config.productionTip = false
Vue.use(ElementUI);
Vue.use(Antd);
Vue.use(VueMeta)
Vue.prototype.$echarts = echarts // 设置全局变量


new Vue({
  vuetify,
  router,
  metaInfo(){
    return {
      title: 'bootcamp',
      meta: [
        { "http-equiv":"Content-Security-Policy", content:"upgrade-insecure-requests"}
      ],
    };
  },
  render: h => h(App)
}).$mount('#app')