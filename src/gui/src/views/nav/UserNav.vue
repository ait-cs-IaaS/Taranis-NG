<template>
  <icon-navigation :links="links" />
</template>

<script>
import IconNavigation from '@/components/common/IconNavigation.vue'

export default {
  name: 'UserNav',
  components: {
    IconNavigation
  },
  data: () => ({
    links: [
      { icon: 'mdi-account', title: 'nav_menu.user', route: '/user' },
      {
        icon: 'mdi-cog-outline',
        title: 'user_menu.settings',
        route: '/user/settings'
      },
      {
        icon: 'mdi-email-multiple-outline',
        title: 'nav_menu.notification_templates',
        route: '/user/templates'
      },
      {
        icon: 'mdi-format-list-text',
        title: 'nav_menu.word_lists',
        route: '/user/wordlists'
      }
    ]
  })
}
</script>
