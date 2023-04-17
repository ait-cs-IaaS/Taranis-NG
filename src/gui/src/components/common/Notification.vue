<template>
  <div>
    <v-snackbar dark v-model="notification" :color="notify.type">
      <span>{{ $t(notify.loc) }}</span>
      <v-btn variant="text" color="white--text" @click="notification = false">{{
        $t('notification.close')
      }}</v-btn>
    </v-snackbar>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
// import { useNotificationStore } from '@/store/notification';

export default defineComponent({
  name: 'NotificationView',

  setup() {
    // const store = useNotificationStore();
    // const notification = computed(() => store.notification);
    // const notify = computed(() => store.notify);
    // const closeNotification = () => {
    //   store.closeNotification();
    // };
    // return { notification, notify, closeNotification };
  }
})
</script>
