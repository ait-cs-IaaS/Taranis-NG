<template>
  <v-app class="grey lighten-2">
    <MainMenu v-if="isAuthenticated" />

    <router-view name="nav"></router-view>

    <v-main>
      <router-view />
    </v-main>

    <Notification v-if="isAuthenticated" />
  </v-app>
</template>

<script>
import MainMenu from '@/components/MainMenu.vue'
import Notification from '@/components/common/Notification.vue'
import { useCookies } from 'vue3-cookies'
import { defineComponent, onMounted } from 'vue'
import { useSettingsStore } from '@/stores/SettingsStore'
import { useAuthStore } from '@/stores/AuthStore'
import { connectSSE, reconnectSSE } from '@/utils/sse'
import { storeToRefs } from 'pinia'

export default defineComponent({
  name: 'App',
  components: {
    MainMenu,
    Notification
  },
  setup() {
    const { cookies } = useCookies()
    const { isAuthenticated, needTokenRefresh, jwt } = storeToRefs(
      useAuthStore()
    )
    const { refresh, logout, setAuthURLs, setToken } = useAuthStore()
    const { loadUserProfile } = useSettingsStore()

    onMounted(() => {
      if (cookies.isKey('jwt')) {
        setToken(cookies.get('jwt')).then(() => {
          cookies.remove('jwt')
        })
      }

      if (localStorage.ACCESS_TOKEN) {
        if (isAuthenticated) {
          setAuthURLs()
          loadUserProfile()
          connectSSE()
        } else {
          if (jwt) {
            logout()
          }
        }
      }
      setInterval(
        function () {
          if (isAuthenticated) {
            if (needTokenRefresh === true) {
              refresh().then(() => {
                console.debug('Token refreshed')
                reconnectSSE()
              })
            }
          } else {
            if (jwt) {
              logout()
            }
          }
        }.bind(this),
        5000
      )
    })

    return {
      cookies,
      isAuthenticated
    }
  }
})
</script>

<style src="./assets/common.css"></style>
<style src="./assets/centralize.css"></style>

<style lang="scss">
@import '@/styles/awake.scss';
</style>
