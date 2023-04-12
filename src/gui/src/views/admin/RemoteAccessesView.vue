<template>
  <div>
    <DataTable
      :addButton="true"
      :items.sync="RemoteAccess"
      :headerFilter="['tag', 'name', 'title', 'description']"
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
import {
  deleteRemoteAccess,
  createRemoteAccess,
  updateRemoteAccess
} from '@/api/config'
import { mapActions as mapActionsVuex } from 'vuex'
import { notifySuccess, notifyFailure, emptyValues } from '@/utils/helpers'
import { mapActions, mapState } from 'pinia'
import { configStore } from '@/stores/ConfigStore'

export default {
  name: 'RemoteAccess',
  components: {
    DataTable,
    EditConfig
  },
  data: () => ({
    RemoteAccess: [],
    formData: {},
    edit: false
  }),
  computed: {
    ...mapState(configStore, ['remote_access']),
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
          name: 'api_url',
          label: 'Node URL',
          type: 'text'
        },
        {
          name: 'api_key',
          label: 'API Key',
          type: 'text'
        }
      ]
    }
  },
  methods: {
    ...mapActions(configStore, ['loadRemoteAccesses']),
    ...mapActionsVuex(['updateItemCount']),
    updateData() {
      this.loadRemoteAccesses().then(() => {
        this.RemoteAccess = this.remote_access.items
        this.updateItemCount({
          total: this.remote_access.total_count,
          filtered: this.remote_access.length
        })
      })
    },
    addItem() {
      this.formData = emptyValues(this.RemoteAccess[0])
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
      console.log(item)
      deleteRemoteAccess(item)
        .then(() => {
          notifySuccess(`Successfully deleted ${item.name}`)
          this.updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to delete ${item.name}`)
        })
    },
    createItem(item) {
      createRemoteAccess(item)
        .then(() => {
          notifySuccess(`Successfully created ${item.name}`)
          this.updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to create ${item.name}`)
        })
    },
    updateItem(item) {
      updateRemoteAccess(item)
        .then(() => {
          notifySuccess(`Successfully updated ${item.name}`)
          this.updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to update ${item.name}`)
        })
    }
  },
  mounted() {
    this.updateData()
  },
  beforeDestroy() {}
}
</script>
