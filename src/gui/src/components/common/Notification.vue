<template>
  <v-snackbar v-model="notification" dark :color="notify.type">
    <span>{{ $t(notify.loc) }}</span>
    <v-btn variant="text" color="white--text" @click="notification = false">{{
      $t('notification.close')
    }}</v-btn>
  </v-snackbar>
</template>

<script>
import { defineComponent, ref } from 'vue'
// import { useNotificationStore } from '@/store/notification';

export default defineComponent({
  name: 'NotificationView',

  setup() {
    const notify = {
      loc: 'notification.test',
      type: 'success'
    }
    const notification = ref(false)
    // const store = useNotificationStore();
    // const notification = computed(() => store.notification);
    // const notify = computed(() => store.notify);
    // const closeNotification = () => {
    //   store.closeNotification();
    // };
    // return { notification, notify, closeNotification };
    return { notify, notification }
  }
})
</script>
