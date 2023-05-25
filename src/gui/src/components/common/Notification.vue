<template>
  <v-snackbar v-model="notify" dark :color="notification.type">
    <span>{{ $t(notification.loc) }}</span>
    <v-btn variant="text" color="white--text" @click="notify = false">{{
      $t('notification.close')
    }}</v-btn>
  </v-snackbar>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useMainStore } from '@/stores/MainStore'
import { storeToRefs } from 'pinia'
import { watch } from 'vue'

export default defineComponent({
  name: 'NotificationView',

  setup() {
    const notify = ref(false)
    const { notification } = storeToRefs(useMainStore())
    watch(notification, () => {
      notify.value = true
    })
    return { notify, notification }
  }
})
</script>
