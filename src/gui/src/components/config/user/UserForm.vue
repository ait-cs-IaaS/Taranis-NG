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
            :items="simple_roles"
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
import { ref, computed, onMounted } from 'vue'
import { useConfigStore } from '@/stores/ConfigStore'
import { storeToRefs } from 'pinia'

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
    const store = useConfigStore()
    const { loadOrganizations, loadRoles, loadPermissions } = store
    const { roles, permissions, organizations } = storeToRefs(store)
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
    const simple_roles = ref([])
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

    const loadUser = (user_id) => {
      if (!user_id || user_id === -1) {
        loadUsers().then(() => {
          const stored_user = getUserByID()(props.userId)
          const roles = stored_user.roles.map((role) => role.id)
          const permissions = stored_user.permissions.map(
            (permission) => permission.id
          )
          stored_user.roles = roles
          stored_user.permissions = permissions
          if (stored_user !== null) {
            user.value = stored_user
            edit.value = true
          }
        })
      } else {
        user.value = {
          id: -1,
          username: '',
          name: '',
          organization: {
            id: 0
          },
          roles: [],
          permissions: []
        }
        edit.value = false
      }
    }

    const loadUsers = mapActions(useConfigStore, ['loadUsers'])
    const getUserByID = mapActions(useConfigStore, ['getUserByID'])

    const add = () => {
      $refs.form.validateAll().then(() => {
        if (edit.value === false || pwd.value !== '') {
          user.value.password = pwd.value
        }

        if (edit.value) {
          updateUser(user.value)
            .then(() => {
              $refs.form.reset()
              notifySuccess('user.successful_edit')
            })
            .catch(() => {
              notifyFailure('user.error')
            })
        } else {
          createUser(user.value)
            .then(() => {
              $refs.form.reset()
              notifySuccess('user.successful')
            })
            .catch(() => {
              notifyFailure('user.error')
            })
        }
      })
    }

    onMounted(() => {
      if (props.userId > 0) {
        edit.value = true
      }
      loadOrganizations()
      loadRoles().then(() => {
        simple_roles.value = roles.items.map((role) => {
          return {
            id: role.id,
            name: role.name,
            description: role.description
          }
        })
      })
      loadPermissions()
      console.debug('Loading User: ' + this.userId)
      this.loadUser(this.userId)
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
      passwordRules,
      loadUser,
      add
    }
  },
  watch: {
    user_id(uid) {
      this.loadUser(uid)
    }
  }
}
</script>
