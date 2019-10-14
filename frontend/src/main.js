import Vue from 'vue'

import Cookies from 'js-cookie'

import App from './App.vue'
import router from './router'
import store from './store'

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import './styles/element-variables.scss'

import 'normalize.css/normalize.css'
import './icons' // icon
import './permission' // permission control
import './styles/element-variables.scss'
import '@/styles/index.scss' // global css

import './utils/error-log' // error log
import * as filters from './filters' // global filters


Vue.use(ElementUI)
Vue.config.devtools = true
Vue.config.productionTip = false

// register global utility filters
Object.keys(filters).forEach(key => {
  Vue.filter(key, filters[key])
})

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
