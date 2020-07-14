import Vue from 'vue'
import App from './App.vue'
import router from './router'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/antd.css'
import axios from 'axios'
import echarts from 'echarts'
import VueSocketIO from 'vue-socket.io'
import store from './store'
import { url } from './api/api'

Vue.config.productionTip = false

Vue.prototype.$echarts = echarts
Vue.prototype.$http = axios

Vue.use(Antd)

var socketio = new VueSocketIO({
  debug: true,
  connection: url + '/flask'
})
Vue.use(socketio)

new Vue({
  router,
  store,
  render: (h) => h(App)
}).$mount('#app')
