<template>
  <v-container fluid class="login-screen" fill-height>
    <v-row no-gutters justify="center" align-content="center">
      <img
        :width="400"
        src="@/assets/taranis-logo-login.svg"
        alt="taranis logo"
      />
    </v-row>
    <v-form @submit.prevent="authenticate" id="form" ref="form">
      <v-row no-gutters justify="center" align-content="center">
        <v-col cols="3">
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
        </v-col>
        <v-col cols="3">
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
        </v-col>
        <v-col cols="1">
          <v-btn
            icon="mdi-login-variant"
            type="submit"
            color="primary"
            @click="authenticate"
            :disabled="loginButtonDisabled"
          />
        </v-col>
      </v-row>
    </v-form>
    <v-alert v-if="login_error !== undefined" dense type="error" text>{{
      $t(login_error)
    }}</v-alert>
  </v-container>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import { defineComponent, ref, computed, inject } from 'vue'

export default defineComponent({
  name: 'LoginView',

  setup() {
    const username = ref('')
    const password = ref('')
    const login_error = ref(undefined)
    const coreAPIURL = inject('$coreAPIURL')
    console.debug('coreAPIURL', coreAPIURL)

    const acceptPassword = computed(() => password.value.length > 0)
    const acceptUser = computed(() => username.value.length > 0)
    const loginButtonDisabled = computed(
      () => !acceptPassword.value || !acceptUser.value
    )

    return {
      username,
      password,
      login_error,
      acceptPassword,
      acceptUser,
      loginButtonDisabled
    }
  },

  methods: {
    ...mapActions(['login']),
    ...mapGetters(['isAuthenticated']),
    authenticate() {
      this.login({ username: this.username, password: this.password }).then(
        (error) => {
          if (this.isAuthenticated()) {
            this.login_error = undefined
            this.$router.push('/')
            return
          }
          if (error) {
            if (error.status > 500) {
              this.login_error = 'login.backend_error'
            } else {
              this.login_error = 'login.error'
            }
          }
        }
      )
    }
  }
})
</script>
