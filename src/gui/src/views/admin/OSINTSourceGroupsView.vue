<template>
  <div>
    <DataTable
      :addButton="true"
      :items.sync="osint_source_groups.items"
      :headerFilter="['tag', 'default', 'name', 'description']"
      sortByItem="id"
      :actionColumn="true"
      @delete-item="deleteItem"
      @edit-item="editItem"
      @add-item="addItem"
      @selection-change="selectionChange"
      @update-items="updateData"
    >
    </DataTable>
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
  createOSINTSourceGroup,
  deleteOSINTSourceGroup,
  updateOSINTSourceGroup
} from '@/api/config'
import { mapActions as mapActionsVuex } from 'vuex'
import { notifySuccess, objectFromFormat, notifyFailure } from '@/utils/helpers'
import { mapActions, mapState } from 'pinia'
import { configStore } from '@/stores/ConfigStore'

export default {
  name: 'OSINTSources',
  components: {
    DataTable,
    EditConfig
  },
  data: () => ({
    selected: [],
    formData: {},
    edit: false
  }),
  computed: {
    ...mapState(configStore, ['osint_source_groups', 'osint_sources']),
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
          name: 'osint_sources',
          label: 'Sources',
          type: 'table',
          headers: [
            { text: 'Name', value: 'name' },
            { text: 'Description', value: 'description' }
          ],
          items: this.osint_sources.items
        }
      ]
    }
  },
  methods: {
    ...mapActions(configStore, ['loadOSINTSourceGroups', 'loadOSINTSources']),
    ...mapActionsVuex(['updateItemCount']),
    async updateData() {
      this.loadOSINTSourceGroups().then(() => {
        this.updateItemCount({
          total: this.osint_source_groups.total_count,
          filtered: this.osint_source_groups.length
        })
      })
      await this.loadOSINTSources()
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
      if (this.edit) {
        console.debug(`Update: ${submittedData}`)
        this.updateItem(submittedData)
      } else {
        console.debug(`Create: ${submittedData}`)
        this.createItem(submittedData)
      }
    },
    deleteItem(item) {
      deleteOSINTSourceGroup(item).then(() => {
        notifySuccess(`Successfully deleted ${item.name}`)
        this.updateData()
      }).catch(() => {
        notifyFailure(`Failed to delete ${item.name}`)
      })
    },
    createItem(item) {
      createOSINTSourceGroup(item).then(() => {
        notifySuccess(`Successfully created ${item.name}`)
        this.updateData()
      }).catch(() => {
        notifyFailure(`Failed to create ${item.name}`)
      })
    },
    updateItem(item) {
      updateOSINTSourceGroup(item).then(() => {
        notifySuccess(`Successfully updated ${item.name}`)
        this.updateData()
      }).catch(() => {
        notifyFailure(`Failed to update ${item.name}`)
      })
    },
    selectionChange(selected) {
      this.selected = selected.map(item => item.id)
    }
  },
  mounted() {
    this.updateData()
  },
  beforeDestroy() {}
}
</script>
