<template>
  <v-menu close-on-back close-on-content-click>
    <template #activator="{ props }">
      <v-btn icon="mdi-account" v-bind="props" />
    </template>
    <v-list>
      <v-list-item prepend-icon="mdi-account" @click="userview">
        <v-list-item-title>{{ username }}</v-list-item-title>
        <v-list-item-subtitle>{{ organizationName }}</v-list-item-subtitle>
      </v-list-item>
      <v-divider></v-divider>

      <v-list-item prepend-icon="mdi-cog-outline" @click="settings">
        <v-list-item-title> {{ $t('user_menu.settings') }}</v-list-item-title>
      </v-list-item>

      <v-list-item prepend-icon="mdi-logout" @click="logout">
        <v-list-item-title> {{ $t('user_menu.logout') }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'UserMenu',
  computed: {
    username() {
      return this.$store.getters.getUserName
    },
    organizationName() {
      return this.$store.getters.getOrganizationName
    }
  },
  methods: {
    logout() {
      this.$store.dispatch('logout').then(() => {
        window.location.reload()
      })
    },
    settings() {
      this.$router.push({ path: '/user/settings' })
    },
    userview() {
      this.$router.push({ path: '/user' })
    }
  }
})
</script>
