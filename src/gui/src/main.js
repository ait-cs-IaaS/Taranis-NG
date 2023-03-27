import 'material-design-icons-iconfont/dist/material-design-icons.css'
import '@mdi/font/css/materialdesignicons.css'
import { createApp } from 'vue'
import App from './App.vue'
import { router } from './router'
import { store } from '@/store/store'
import ApiService from '@/services/api_service'
import { createI18n } from 'vue-i18n'
import { messages } from '@/i18n/messages'
import { dateTimeFormats } from '@/i18n/datetimeformat'
import VueCookies from 'vue-cookies'
import DatePicker from 'vue-datepicker-next'
import { vuetify } from '@/plugins/vuetify'

export const app = createApp(App)

app.use(require('vue-cookies'))
app.use(VueCookies)
app.use(DatePicker)


const i18n = createI18n({
  locale:
    typeof process.env.VUE_APP_TARANIS_NG_LOCALE === 'undefined'
      ? 'en'
      : process.env.VUE_APP_TARANIS_NG_LOCALE,
  fallbackLocale: 'en',
  messages,
  dateTimeFormats
})

app.use(i18n)

//import VeeValidate from 'vee-validate'
// app.use(VeeValidate, {
//   i18nRootKey: 'validations',
//   i18n
// })

const coreAPIURL =
  typeof process.env.VUE_APP_TARANIS_NG_CORE_API === 'undefined'
    ? '$VUE_APP_TARANIS_NG_CORE_API'
    : process.env.VUE_APP_TARANIS_NG_CORE_API

ApiService.init(coreAPIURL)

if (localStorage.ACCESS_TOKEN) {
  store.dispatch('setToken', localStorage.ACCESS_TOKEN).then()
}

app.use(store)
app.use(router)
app.use(vuetify)
app.mount('#app')
