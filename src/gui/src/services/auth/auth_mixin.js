import { store } from '@/store/store'

const AuthMixin = {
  methods: {
    isAuthenticated() {
      return store.getters.isAuthenticated
    },
    needTokenRefresh() {
      return store.getters.needTokenRefresh
    },
    checkPermission(permission) {
      return store.getters.getPermissions.includes(permission)
    }
  }
}

export default AuthMixin
