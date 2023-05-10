<template>
  <v-container fluid class="ma-5 mt-5 pa-5 pt-0">
    <v-form id="form" ref="form" @submit.prevent="add">
      <v-row no-gutters>
        <v-btn type="submit" color="success" class="mr-4"> Submit </v-btn>
      </v-row>
      <v-row no-gutters>
        <v-col cols="6" class="pa-1">
          <v-text-field
            v-model="user.username"
            :label="$t('user.username')"
            name="username"
            type="text"
            autocomplete="username"
            :rules="[rules.required]"
          />
        </v-col>
        <v-col cols="6" class="pa-1">
          <v-text-field
            v-model="user.name"
            :label="$t('user.name')"
            name="name"
          />
        </v-col>
        <v-col cols="6" class="pa-1">
          <v-text-field
            ref="password"
            v-model="pwd"
            type="password"
            :rules="passwordRules"
            autocomplete="new-password"
            :label="$t('user.password')"
          />
        </v-col>
        <v-col cols="6" class="pa-1">
          <v-text-field
            v-model="repwd"
            type="password"
            :rules="passwordRules"
            autocomplete="new-password"
            :label="$t('user.password_check')"
          />
        </v-col>
      </v-row>

      <v-row no-gutters>
        <v-col cols="6" class="pr-1">
          <v-select
            v-model="user.organization.id"
            item-title="name"
            item-value="id"
            :hint="$t('user.organization')"
            :label="$t('user.organization')"
            :items="organizations.items"
          >
          </v-select>
        </v-col>
        <v-col cols="12" class="pl-1">
          <v-data-table
            v-model="user.roles"
            :headers="headers"
            :items="roles"
            item-value="id"
            :show-select="true"
            class="elevation-1"
          >
            <template #top>
              <v-toolbar flat color="white">
                <v-toolbar-title>{{ $t('user.roles') }}</v-toolbar-title>
              </v-toolbar>
            </template>
            <template v-if="roles.length < 10" #bottom />
          </v-data-table>
        </v-col>
        <v-col cols="12" class="pt-2">
          <v-data-table
            v-model="user.permissions"
            :headers="headers"
            :items="permissions"
            item-value="id"
            :show-select="true"
            class="elevation-1"
          >
            <template #top>
              <v-toolbar flat color="white">
                <v-toolbar-title>{{ $t('user.permissions') }}</v-toolbar-title>
              </v-toolbar>
            </template>
            <template v-if="permissions.length < 10" #bottom />
          </v-data-table>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script>
import { createUser, updateUser } from '@/api/config'
import { mapActions } from 'pinia'
import { notifySuccess, notifyFailure } from '@/utils/helpers'
import { ref, computed } from 'vue'
import { useConfigStore } from '@/stores/ConfigStore'

export default {
  name: 'UserForm',
  props: {
    userId: {
      type: Number,
      required: false,
      default: -1
    }
  },
  setup() {
    const headers = [
      {
        text: 'Name',
        align: 'start',
        value: 'name'
      },
      { text: 'Description', value: 'description' }
    ]

    const edit = ref(false)
    const pwd = ref('')
    const repwd = ref('')
    const organizations = ref([])
    const roles = ref([])
    const permissions = ref([])
    const user = ref({
      id: -1,
      username: '',
      name: '',
      organization: {
        id: 0
      },
      roles: [],
      permissions: []
    })

    const rules = {
      required: (value) => !!value || 'Required.',
      matchPassword: (value) => {
        if (!edit.value) {
          return !!value || 'Required.'
        }
        if (!value && !pwd.value) {
          return true
        }
        return value === pwd.value || 'Passwords must match.'
      }
    }
    const passwordRules = computed(() => {
      return edit.value
        ? [rules.matchPassword]
        : [rules.required, rules.matchPassword]
    })

    return {
      headers,
      rules,
      edit,
      roles,
      permissions,
      organizations,
      pwd,
      repwd,
      user,
      passwordRules
    }
  },
  watch: {
    user_id(uid) {
      this.loadUser(uid)
    }
  },
  created() {
    this.loadOrganizations().then(() => {
      this.organizations = this.store_organizations
    })
    this.loadRoles().then(() => {
      this.roles = this.store_roles.items.map((role) => {
        return {
          id: role.id,
          name: role.name,
          description: role.description
        }
      })
    })
    this.loadPermissions().then(() => {
      this.permissions = this.store_permissions.items
    })

    console.debug('Loading User: ' + this.userId)
    this.loadUser(this.userId)
    console.debug(this.user)
  },
  methods: {
    ...mapActions(useConfigStore, [
      'loadOrganizations',
      'loadRoles',
      'loadPermissions',
      'loadUsers'
    ]),
    add() {
      this.$validator.validateAll().then(() => {
        if (this.edit === false || this.pwd !== '') {
          this.user.password = this.pwd
        }

        if (this.edit) {
          updateUser(this.user)
            .then(() => {
              this.$validator.reset()
              notifySuccess('user.successful_edit')
            })
            .catch(() => {
              notifyFailure('user.error')
            })
        } else {
          createUser(this.user)
            .then(() => {
              this.$validator.reset()
              notifySuccess('user.successful')
            })
            .catch(() => {
              notifyFailure('user.error')
            })
        }
      })
    },
    loadUser(user_id) {
      if (!user_id || user_id === -1) {
        this.loadUsers().then(() => {
          const stored_user = this.getUserByID()(this.userId)
          const roles = stored_user.roles.map((role) => role.id)
          const permissions = stored_user.permissions.map(
            (permission) => permission.id
          )
          stored_user.roles = roles
          stored_user.permissions = permissions
          if (stored_user !== null) {
            this.user = stored_user
            this.edit = true
          }
        })
      } else {
        this.user = {
          id: -1,
          username: '',
          name: '',
          organization: {
            id: 0
          },
          roles: [],
          permissions: []
        }
        this.edit = false
      }
    }
  }
}
</script>
