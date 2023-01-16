<template>
  <div>
    <ConfigTable
      :addButton="true"
      :items.sync="roles"
      :headerFilter="['tag', 'id', 'name', 'description']"
      sortByItem="id"
      :actionColumn="true"
      @delete-item="deleteItem"
      @edit-item="editItem"
      @add-item="addItem"
    />
    <EditConfig
      v-if="formData && Object.keys(formData).length > 0"
      :configData="formData"
      @submit="handleSubmit"
    ></EditConfig>
  </div>
</template>

<script>
import ConfigTable from '../../components/config/ConfigTable'
import EditConfig from '../../components/config/EditConfig'
import {
  deleteOrganization,
  createOrganization,
  updateOrganization
} from '@/api/config'
import { mapActions, mapGetters } from 'vuex'
import { notifySuccess, emptyValues, notifyFailure } from '@/utils/helpers'

export default {
  name: 'Roles',
  components: {
    ConfigTable,
    EditConfig
  },
  data: () => ({
    roles: [],
    formData: {},
    showForm: false,
    edit: false
  }),
  methods: {
    ...mapActions('config', ['loadRoles']),
    ...mapGetters('config', ['getRoles']),
    ...mapActions(['updateItemCount']),
    updateData() {
      this.loadRoles().then(() => {
        const sources = this.getRoles()
        this.roles = sources.items
        this.updateItemCount({
          total: sources.total_count,
          filtered: sources.length
        })
      })
    },
    addItem() {
      this.formData = emptyValues(this.roles[0])
      this.showForm = true
      this.edit = false
    },
    editItem(item) {
      this.formData = item
      this.showForm = true
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
        deleteOrganization(item).then(() => {
          notifySuccess(`Successfully deleted ${item.name}`)
          this.updateData()
        }).catch(() => {
          notifyFailure(`Failed to delete ${item.name}`)
        })
      }
    },
    createItem(item) {
      createOrganization(item).then(() => {
        notifySuccess(`Successfully created ${item.name}`)
        this.updateData()
      }).catch(() => {
        notifyFailure(`Failed to create ${item.name}`)
      })
    },
    updateItem(item) {
      updateOrganization(item).then(() => {
        notifySuccess(`Successfully updated ${item.name}`)
        this.updateData()
      }).catch(() => {
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
