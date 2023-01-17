<template>
  <div>

    <ConfigTable
      :addButton="true"
      :items.sync="osint_sources"
      :headerFilter="['tag', 'id', 'name', 'description']"
      sortByItem="id"
      :actionColumn="true"
      @delete-item="deleteItem"
      @edit-item="editItem"
      @add-item="addItem"
    >
    <template v-slot:titlebar>
      <ImportExport
        @import="importData"
        @export="exportData"
      ></ImportExport>
    </template>
    </ConfigTable>
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
import ImportExport from '../../components/config/ImportExport'
import {
  deleteOSINTSource,
  createOSINTSource,
  updateOSINTSource,
  exportOSINTSources,
  importOSINTSources
} from '@/api/config'
import { mapActions, mapGetters } from 'vuex'
import { notifySuccess, emptyValues, notifyFailure } from '@/utils/helpers'

export default {
  name: 'OSINTSources',
  components: {
    ConfigTable,
    EditConfig,
    ImportExport
  },
  data: () => ({
    osint_sources: [],
    selected: [],
    formData: {},
    showForm: false,
    edit: false
  }),
  methods: {
    ...mapActions('config', ['loadOSINTSources']),
    ...mapGetters('config', ['getOSINTSources']),
    ...mapActions(['updateItemCount']),
    updateData() {
      this.loadOSINTSources().then(() => {
        const sources = this.getOSINTSources()
        this.osint_sources = sources.items
        this.updateItemCount({
          total: sources.total_count,
          filtered: sources.length
        })
      })
    },
    addItem() {
      this.formData = emptyValues(this.osint_sources[0])
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
      deleteOSINTSource(item).then(() => {
        notifySuccess(`Successfully deleted ${item.name}`)
        this.updateData()
      }).catch(() => {
        notifyFailure(`Failed to delete ${item.name}`)
      })
    },
    createItem(item) {
      createOSINTSource(item).then(() => {
        notifySuccess(`Successfully created ${item.name}`)
        this.updateData()
      }).catch(() => {
        notifyFailure(`Failed to create ${item.name}`)
      })
    },
    updateItem(item) {
      updateOSINTSource(item).then(() => {
        notifySuccess(`Successfully updated ${item.name}`)
        this.updateData()
      }).catch(() => {
        notifyFailure(`Failed to update ${item.name}`)
      })
    },
    importData(data) {
      importOSINTSources(data)
    },
    exportData() {
      console.debug('export OSINT sources')
      exportOSINTSources(this.selected)
    }
  },
  mounted() {
    this.updateData()
  },
  beforeDestroy() {}
}
</script>
