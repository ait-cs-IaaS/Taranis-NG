<template>
  <v-container fluid class="ma-5 mt-5 pa-5 pt-0">
    ID: {{ user.id }}
    <v-form id="form" ref="form" validate-on="submit" @submit.prevent="add">
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
            v-model="user_roles"
            :headers="headers"
            :items="roles.items"
            show-select
          >
            <template #top>
              <v-toolbar-title class="ml-3 text-center">
                {{ $t('user.roles') }}
              </v-toolbar-title>
            </template>
            <template v-if="roles.items.length < 10" #bottom />
          </v-data-table>
        </v-col>
        <v-col cols="12" class="pt-2">
          <v-data-table
            v-model="user.permissions"
            :headers="headers"
            :items="permissions.items"
            show-select
          >
            <template #top>
              <v-toolbar-title class="ml-3 text-center">
                {{ $t('user.permissions') }}
              </v-toolbar-title>
            </template>
            <template v-if="permissions.items.length < 10" #bottom />
          </v-data-table>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script>
import { createUser, updateUser } from '@/api/config'
import { notifySuccess, notifyFailure } from '@/utils/helpers'
import { ref, computed, onMounted } from 'vue'
import { useConfigStore } from '@/stores/ConfigStore'
import { storeToRefs } from 'pinia'

export default {
  name: 'UserForm',
  props: {
    userProp: {
      type: Object,
      required: true
    },
    edit: {
      type: Boolean,
      required: true,
      default: false
    }
  },
  setup(props) {
    const store = useConfigStore()
    const { loadOrganizations, loadRoles, loadPermissions } = store
    const { roles, permissions, organizations } = storeToRefs(store)
    const form = ref(null)

    const headers = [
      {
        title: 'Name',
        align: 'start',
        key: 'name'
      },
      { title: 'Description', key: 'description' }
    ]

    const pwd = ref('')
    const repwd = ref('')
    const user = ref(props.userProp)

    const rules = {
      required: (value) => !!value || 'Required.',
      matchPassword: (value) => {
        if (!props.edit) {
          return !!value || 'Required.'
        }
        if (!value && !pwd.value) {
          return true
        }
        return value === pwd.value || 'Passwords must match.'
      }
    }
    const passwordRules = computed(() => {
      return props.edit
        ? [rules.matchPassword]
        : [rules.required, rules.matchPassword]
    })

    const user_roles = computed({
      get: () => {
        return user.value.roles.map((role) => role.id)
      },
      set: (value) => {
        user.value.roles = value
      }
    })

    const user_permissions = computed({
      get: () => {
        return user.value.permissions.map((permission) => permission.id)
      },
      set: (value) => {
        user.value.permissions = value
      }
    })

    const add = () => {
      if (props.edit === false || pwd.value !== '') {
        user.value.password = pwd.value
      }

      if (props.edit) {
        updateUser(user.value)
          .then(() => {
            form.value.reset()
            notifySuccess('user.successful_edit')
          })
          .catch(() => {
            notifyFailure('user.error')
          })
      } else {
        createUser(user.value)
          .then(() => {
            form.value.reset()
            notifySuccess('user.successful')
          })
          .catch(() => {
            notifyFailure('user.error')
          })
      }
    }

    onMounted(() => {
      console.debug('Loading User: ' + user.value.id)
      loadOrganizations()
      loadRoles()
      loadPermissions()
    })

    return {
      headers,
      rules,
      roles,
      permissions,
      form,
      organizations,
      user_roles,
      user_permissions,
      pwd,
      repwd,
      passwordRules,
      user,
      add
    }
  },
  watch: {
    userProp(u) {
      this.user = u
    }
  }
}
</script>
