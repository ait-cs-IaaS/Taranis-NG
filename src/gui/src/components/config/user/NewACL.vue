<template>
  <v-container fluid class="ma-5 mt-5 pa-5 pt-0">
    <span v-if="edit" class="caption">ID: {{ acl.id }}</span>
    <v-form id="form" ref="form" validate-on="submit" @submit.prevent="add">
      <v-row no-gutters>
        <v-btn type="submit" color="success" class="mr-4"> Submit </v-btn>
      </v-row>
      <v-row no-gutters>
        <v-col cols="12" class="pa-1">
          <v-text-field
            v-model="acl.name"
            :label="$t('acl.name')"
            name="name"
            type="text"
            :rules="[rules.required]"
          />
        </v-col>
        <v-col cols="12" class="pa-1">
          <v-textarea
            v-model="acl.description"
            :label="$t('acl.description')"
            name="description"
          />
        </v-col>
        <v-col cols="6" class="pa-1">
          <v-combobox
            v-model="selected_type"
            :items="types"
            item-title="title"
            :label="$t('acl.item_type')"
          />
        </v-col>
        <v-col cols="6" class="pa-1">
          <v-text-field
            v-model="acl.item_id"
            :label="$t('acl.item_id')"
            name="item_id"
            type="text"
          />
        </v-col>
      </v-row>
      <v-row no-gutters>
        <v-col cols="12" class="d-flex">
          <v-checkbox
            v-model="acl.see"
            class="pr-8"
            :label="$t('acl.see')"
            name="see"
          />
          <v-checkbox
            v-model="acl.access"
            class="pr-8"
            :label="$t('acl.access')"
            name="access"
          />
          <v-checkbox
            v-model="acl.modify"
            class="pr-8"
            :label="$t('acl.modify')"
            name="modify"
          />
        </v-col>
      </v-row>
      <v-row no-gutters>
        <v-col cols="12">
          <v-checkbox
            v-model="acl.everyone"
            :label="$t('acl.everyone')"
            name="everyone"
          />
        </v-col>
        <v-col cols="12">
          <v-data-table
            v-model="selected_users"
            :headers="headers_user"
            :items="users.items"
            item-key="id"
            :show-select="true"
            class="elevation-1"
          >
            <template #top>
              <v-toolbar flat color="white">
                <v-toolbar-title>{{ $t('acl.users') }}</v-toolbar-title>
              </v-toolbar>
            </template>
          </v-data-table>
        </v-col>
        <v-col cols="12" class="pt-2">
          <v-data-table
            v-model="selected_roles"
            :headers="headers_role"
            :items="roles.items"
            item-key="id"
            :show-select="true"
            class="elevation-1"
          >
            <template #top>
              <v-toolbar flat color="white">
                <v-toolbar-title>{{ $t('acl.roles') }}</v-toolbar-title>
              </v-toolbar>
            </template>
          </v-data-table>
        </v-col>
      </v-row>
      <v-row>
        <v-btn text dark type="submit" form="form">
          <v-icon left>mdi-content-save</v-icon>
          <span>{{ $t('acl.save') }}</span>
        </v-btn></v-row
      >
    </v-form>
  </v-container>
</template>

<script>
import { createACLEntry, updateACLEntry } from '@/api/config'
import { notifySuccess, notifyFailure } from '@/utils/helpers'
import { mapActions } from 'pinia'
import { useConfigStore } from '@/stores/ConfigStore'

export default {
  name: 'NewACL',
  props: {
    aclProp: {
      type: Obejct,
      required: true
    },
    edit: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    const store = useConfigStore()
    const { loadOrganizations, loadRoles, loadPermissions } = store
    const { roles, permissions, organizations } = storeToRefs(store)
    const form = ref(null)
    const rules = {
      required: (value) => !!value || 'Required.'
    }

    const headers_user = [
      {
        title: 'Username',
        key: 'username'
      },
      { title: 'Name', key: 'name' }
    ]

    const headers_role = [
      {
        title: 'Name',
        key: 'name'
      },
      { title: 'Description', key: 'description' }
    ]

    const types = [
      { id: 'COLLECTOR', title: 'Collector' },
      { id: 'DELEGATION', title: 'Delegation' },
      { id: 'OSINT_SOURCE', title: 'OSINT Source' },
      { id: 'OSINT_SOURCE_GROUP', title: 'OSINT Source Group' },
      { id: 'PRODUCT_TYPE', title: 'Product Type' },
      { id: 'REPORT_ITEM', title: 'Report Item' },
      { id: 'REPORT_ITEM_TYPE', title: 'Report Item Type' },
      { id: 'WORD_LIST', title: 'Word List' }
    ]
    const selected_type = null

    const show_validation_error = false
    const selected_users = []
    const selected_roles = []
    const acl = {
      id: -1,
      name: '',
      description: '',
      users: [],
      roles: []
    }

    return {
      form,
      rules,
      headers_user,
      headers_role,
      loadOrganizations,
      loadRoles,
      loadPermissions,
      roles,
      permissions,
      organizations
    }
  },
  mounted() {
    this.loadUsers().then(() => {
      this.users = this.getUsers().items
    })

    this.loadRoles().then(() => {
      this.roles = this.getRoles().items
    })

    if (!this.aclId || this.aclId === -1) {
      this.acl = {
        id: -1,
        name: '',
        description: '',
        users: [],
        roles: []
      }
    } else {
      // TODO: load acl
      this.acl = {
        id: -1,
        name: '',
        description: '',
        users: [],
        roles: []
      }
    }
  },
  methods: {
    ...mapActions(useConfigStore, ['loadUsers', 'loadRoles']),
    addACL() {
      this.show_error = false
      this.selected_type = null
      this.acl.id = -1
      this.acl.name = ''
      this.acl.description = ''
      this.acl.item_type = ''
      this.acl.item_id = ''
      this.acl.everyone = false
      this.acl.see = false
      this.acl.access = false
      this.acl.modify = false
      this.acl.users = []
      this.acl.roles = []
      this.selected_users = []
      this.selected_roles = []
      this.$validator.reset()
    },
    add() {
      this.$validator.validateAll().then(() => {
        if (!this.$validator.errors.any()) {
          this.show_validation_error = false
          this.show_error = false

          if (this.selected_type !== null) {
            this.acl.item_type = this.selected_type.id
          }

          this.acl.users = []
          for (let i = 0; i < this.selected_users.length; i++) {
            this.acl.users.push({
              id: this.selected_users[i].id
            })
          }

          this.acl.roles = []
          for (let i = 0; i < this.selected_roles.length; i++) {
            this.acl.roles.push({
              id: this.selected_roles[i].id
            })
          }

          if (this.edit) {
            updateACLEntry(this.acl)
              .then(() => {
                this.$validator.reset()
                notifySuccess('acl.successful_edit')
              })
              .catch(() => {
                notifyFailure('acl.error_edit')
                this.show_error = true
              })
          } else {
            createACLEntry(this.acl)
              .then(() => {
                this.$validator.reset()
                notifySuccess('acl.successful')
              })
              .catch(() => {
                notifyFailure('acl.error')
                this.show_error = true
              })
          }
        } else {
          this.show_validation_error = true
        }
      })
    }
  }
}
</script>
