import '@mdi/font/css/materialdesignicons.css'
import { createApp } from 'vue'
import App from './App.vue'
import { router } from './router'
import ApiService from '@/services/api_service'
import { createI18n } from 'vue-i18n'
import { messages } from '@/i18n/messages'
import { datetimeFormats } from '@/i18n/datetimeformat'
import DatePicker from 'vue-datepicker-next'
import { vuetify } from '@/plugins/vuetify'
import { createPinia } from 'pinia'

export const app = createApp(App)

app.use(DatePicker)

const i18n = createI18n({
  legacy: false,
  locale:
    typeof import.meta.env.VITE_TARANIS_NG_LOCALE === 'undefined'
      ? 'en'
      : import.meta.env.VITE_TARANIS_NG_LOCALE,
  fallbackLocale: 'en',
  messages,
  datetimeFormats
})

app.use(i18n)

const coreAPIURL =
  typeof import.meta.env.VITE_TARANIS_NG_CORE_API === 'undefined'
    ? '/api'
    : import.meta.env.VITE_TARANIS_NG_CORE_API

ApiService.init(coreAPIURL)
app.provide('$coreAPIURL', coreAPIURL)

const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(vuetify)
app.mount('#app')
