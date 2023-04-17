<template>
  <div>
    <DataTable
      :addButton="true"
      :items.sync="roles.items"
      :headerFilter="['tag', 'id', 'name', 'description']"
      sortByItem="id"
      :actionColumn="true"
      @delete-item="deleteItem"
      @edit-item="editItem"
      @add-item="addItem"
      @update-items="updateData"
    />
    <EditConfig
      v-if="formData && Object.keys(formData).length > 0"
      :configData="formData"
      :formFormat="formFormat"
      @submit="handleSubmit"
    ></EditConfig>
  </div>
</template>

<script>
import DataTable from '@/components/common/DataTable'
import EditConfig from '../../components/config/EditConfig'
import { deleteRole, createRole, updateRole } from '@/api/config'
import { mapActions as mapActionsVuex } from 'vuex'
import { notifySuccess, objectFromFormat, notifyFailure } from '@/utils/helpers'

import { mapActions, mapState } from 'pinia'
import { configStore } from '@/stores/ConfigStore'

export default {
  name: 'Roles',
  components: {
    DataTable,
    EditConfig
  },
  data: () => ({
    formData: {},
    selected: [],
    edit: false
  }),
  computed: {
    ...mapState(configStore, ['roles', 'permissions']),
    formFormat() {
      return [
        {
          name: 'id',
          label: 'ID',
          type: 'text',
          disabled: true
        },
        {
          name: 'name',
          label: 'Name',
          type: 'text',
          required: true
        },
        {
          name: 'description',
          label: 'Description',
          type: 'textarea',
          required: true
        },
        {
          name: 'permissions',
          label: 'Permissions',
          type: 'table',
          headers: [
            { text: 'Name', value: 'name' },
            { text: 'Description', value: 'description' }
          ],
          items: this.permissions.items
        }
      ]
    }
  },
  methods: {
    ...mapActions(configStore, ['loadRoles', 'loadPermissions']),
    ...mapActionsVuex(['updateItemCount']),
    async updateData() {
      this.loadRoles().then(() => {
        this.updateItemCount({
          total: this.roles.total_count,
          filtered: this.roles.length
        })
      })
      await this.loadPermissions()
    },
    addItem() {
      this.formData = objectFromFormat(this.formFormat)
      this.edit = false
    },
    editItem(item) {
      this.formData = item
      this.edit = true
    },
    handleSubmit(submittedData) {
      console.log(submittedData)
      if (this.edit) {
        this.updateItem(submittedData)
      } else {
        this.createItem(submittedData)
      }
    },
    deleteItem(item) {
      if (!item.default) {
        deleteRole(item)
          .then(() => {
            notifySuccess(`Successfully deleted ${item.name}`)
            this.updateData()
          })
          .catch(() => {
            notifyFailure(`Failed to delete ${item.name}`)
          })
      }
    },
    createItem(item) {
      createRole(item)
        .then(() => {
          notifySuccess(`Successfully created ${item.name}`)
          this.updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to create ${item.name}`)
        })
    },
    updateItem(item) {
      updateRole(item)
        .then(() => {
          notifySuccess(`Successfully updated ${item.name}`)
          this.updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to update ${item.name}`)
        })
    },
    selectionChange(selected) {
      this.selected = selected.map((item) => item.id)
    }
  },
  mounted() {
    this.updateData()
  },
  beforeDestroy() {}
}
</script>
