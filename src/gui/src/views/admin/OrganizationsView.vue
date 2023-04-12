<template>
  <div>
    <DataTable
      :addButton="true"
      :items.sync="organizations.items"
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
      @submit="handleSubmit"
    ></EditConfig>
  </div>
</template>

<script>
import DataTable from '@/components/common/DataTable'
import EditConfig from '../../components/config/EditConfig'
import {
  deleteOrganization,
  createOrganization,
  updateOrganization
} from '@/api/config'
import { notifySuccess, emptyValues, notifyFailure } from '@/utils/helpers'
import { mapActions, mapState } from 'pinia'
import { configStore } from '@/stores/ConfigStore'
import { mapActions as mapActionsVuex } from 'vuex'

export default {
  name: 'Organizations',
  components: {
    DataTable,
    EditConfig
  },
  data: () => ({
    formData: {},
    edit: false
  }),
  computed: {
    ...mapState(configStore, ['organizations'])
  },
  methods: {
    ...mapActions(configStore, ['loadOrganizations']),
    ...mapActionsVuex(['updateItemCount']),
    updateData() {
      this.loadOrganizations().then(() => {
        this.updateItemCount({
          total: this.organizations.total_count,
          filtered: this.organizations.length
        })
      })
    },
    addItem() {
      this.formData = emptyValues(this.organizations.items[0])
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
        deleteOrganization(item)
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
      createOrganization(item)
        .then(() => {
          notifySuccess(`Successfully created ${item.name}`)
          this.updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to create ${item.name}`)
        })
    },
    updateItem(item) {
      updateOrganization(item)
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
