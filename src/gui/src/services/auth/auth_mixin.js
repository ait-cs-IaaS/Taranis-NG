import Permissions from '@/services/auth/permissions'
import { store } from '@/store/store'
import { authStore } from '@/stores/AuthStore'

const AuthMixin = {
  data: () => ({
    permissions: Permissions
  }),
  methods: {
    isAuthenticated() {
      const authstore = authStore()
      return authstore.isAuthenticated
    },
    needTokenRefresh() {
      const authstore = authStore()
      return authstore.needTokenRefresh
    },
    checkPermission(permission) {
      return store.getters.getPermissions.includes(permission)
    }
  }
}

export default AuthMixin
