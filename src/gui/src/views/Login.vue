<template>
  <v-container fluid class="login-screen" fill-height>
      <img :width="400" src="@/assets/taranis-logo-login.svg" alt="taranis logo"/>
      <v-form @submit.prevent="authenticate" id="form" ref="form">
              <v-text-field
                :placeholder="$t('login.username')"
                name="username"
                prepend-icon="person"
                type="text"
                v-model="username"
                :rules="[acceptUser]"
                autocomplete="username"
                required
              />
              <v-text-field
                :placeholder="$t('login.password')"
                name="password"
                prepend-icon="lock"
                type="password"
                v-model="password"
                :rules="[acceptPassword]"
                autocomplete="password"
                required
              />
              <v-btn text @click="authenticate">
                <v-icon color="white" large>mdi-login-variant</v-icon>
              </v-btn>
      </v-form>
    <v-alert v-if="login_error !== undefined" dense type="error" text>{{$t(login_error)}}</v-alert>
  </v-container>
</template>

<style scoped>
  .v-container {
    background-color: #c7c7c7; text-align: center;
  }

</style>

<script>
import AuthMixin from '@/services/auth/auth_mixin'
import { mapActions } from 'vuex'
import { defineComponent } from "vue";

export default defineComponent({
  name: 'Login',
  data: () => ({
    username: '',
    password: '',
    login_error: undefined
  }),
  mixins: [AuthMixin],
  computed: {
    acceptPassword() {
      return this.password.length > 0
    },

    acceptUser() {
      return this.username.length > 0
    },
  },
  methods: {
    ...mapActions(['login']),
    authenticate () {
      this.login({ username: this.username, password: this.password })
        .then((error) => {
          if (this.isAuthenticated()) {
            this.login_error = undefined
            this.$router.push('/')
            return
          }
          if (error) {
            this.$refs.form.reset()
            this.$validator.reset()
            if (error.status > 500) {
              this.login_error = 'login.backend_error'
            } else {
              this.login_error = 'login.error'
            }
          }
        })
    }
  }
})
</script>
