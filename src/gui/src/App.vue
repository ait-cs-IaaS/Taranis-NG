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
import { useStore } from 'vuex'
import { connectSSE, reconnectSSE } from '@/utils/sse'

export default defineComponent({
  name: 'App',
  components: {
    MainMenu,
    Notification
  },
  setup() {
    const store = useStore()
    const { cookies } = useCookies()

    const loadUserProfile = () => store.dispatch('settings/loadUserProfile')
    const isAuthenticated = () => store.getters['isAuthenticated']
    const needTokenRefresh = () => store.getters['needTokenRefresh']

    onMounted(() => {
      if (cookies.isKey('jwt')) {
        store.dispatch('setToken', cookies.get('jwt')).then(() => {
          cookies.remove('jwt')
        })
      }

      if (localStorage.ACCESS_TOKEN) {
        if (isAuthenticated()) {
          store.dispatch('setAuthURLs')
          loadUserProfile()
          connectSSE()
        } else {
          if (store.getters.getJWT) {
            store.dispatch('logout')
          }
        }
      }
      setInterval(
        function () {
          if (isAuthenticated()) {
            if (needTokenRefresh() === true) {
              store.dispatch('refresh').then(() => {
                console.debug('Token refreshed')
                reconnectSSE()
              })
            }
          } else {
            if (store.getters.getJWT) {
              store.dispatch('logout')
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
