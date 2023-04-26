<template>
  <v-app class="grey lighten-2">
    <MainMenu v-if="isAuthenticated()" />

    <router-view name="nav"></router-view>

    <v-main>
      <router-view />
    </v-main>

    <Notification v-if="isAuthenticated()" />
  </v-app>
</template>

<script>
import MainMenu from './components/MainMenu'
import AuthMixin from './services/auth/auth_mixin'
import Notification from './components/common/Notification'
import { mapActions, mapState } from 'pinia'
import { settingsStore } from '@/stores/SettingsStore'
import { authStore } from './stores/AuthStore'

export default {
  name: 'App',
  components: {
    MainMenu,
    Notification
  },
  computed: {
    ...mapState(settingsStore, ['dark_theme']),
    ...mapState(authStore, ['jwt'])
  },
  mixins: [AuthMixin],
  methods: {
    ...mapActions(settingsStore, ['loadUserProfile']),
    ...mapActions(authStore, ['setToken', 'setAuthURLs', 'refresh', 'logout']),
    connectSSE() {
      // TODO: unsubscribe
      if (process.env.VUE_APP_TARANIS_NG_CORE_SSE === undefined) {
        return
      }
      this.$sse(`${process.env.VUE_APP_TARANIS_NG_CORE_SSE}?jwt=${this.jwt}`, {
        format: 'json'
      }).then((sse) => {
        sse.subscribe('news-items-updated', (data) => {
          this.$root.$emit('news-items-updated', data)
        })
        sse.subscribe('report-items-updated', (data) => {
          this.$root.$emit('report-items-updated', data)
        })
        sse.subscribe('report-item-updated', (data) => {
          this.$root.$emit('report-item-updated', data)
        })
        sse.subscribe('report-item-locked', (data) => {
          this.$root.$emit('report-item-locked', data)
        })
        sse.subscribe('report-item-unlocked', (data) => {
          this.$root.$emit('report-item-unlocked', data)
        })
      })
    },

    reconnectSSE() {
      if (this.sseConnection !== null) {
        this.sseConnection.close()
        this.sseConnection = null
      }
      this.connectSSE()
    }
  },
  updated() {
    this.$root.$emit('app-updated')
  },
  async mounted() {
    if (this.$cookies.isKey('jwt')) {
      this.setToken(this.$cookies.get('jwt'))
      this.$cookies.remove('jwt')
      this.connectSSE()
    }

    if (localStorage.ACCESS_TOKEN) {
      if (this.isAuthenticated()) {
        await this.loadUserProfile()
        this.$vuetify.theme.dark = this.dark_theme

        this.connectSSE()
      } else {
        if (this.jwt) {
          this.logout()
        }
      }
    }
    setInterval(
      function () {
        if (this.isAuthenticated()) {
          if (this.needTokenRefresh() === true) {
            this.refresh()
            console.debug('Token refreshed')
            // this.reconnectSSE()
          }
        } else {
          if (this.jwt) {
            this.logout()
          }
        }
      }.bind(this),
      5000
    )
  },
  created() {}
}
</script>

<style src="./assets/common.css"></style>
<style src="./assets/centralize.css"></style>

<style lang="scss">
@import '@/styles/awake.scss';
</style>
