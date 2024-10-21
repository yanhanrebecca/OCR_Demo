// import './assets/main.css'
// 全局样式重置
import 'reset-css/reset.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
//引入Element Plus样式
import 'element-plus/dist/index.css'
//引入Element Plus
import ElementPlus from 'element-plus'
// 引入 Element Plus 图标库
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
//引入中文语言包
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import 'virtual:svg-icons-register';
import SvgIcon from '@/components/icons/SvgIcon.vue'
const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ElementPlus)
app.use(ElementPlus, {
  locale: zhCn,
})
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
app.component('svg-icon', SvgIcon);
app.mount('#app')
