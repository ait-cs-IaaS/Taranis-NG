<template>
  <div>
    <ConfigTable
      :addButton="true"
      :items.sync="osint_sources"
      :headerFilter="['tag', 'name', 'description', 'FEED_URL']"
      sortByItem="id"
      :actionColumn="true"
      @delete-item="deleteItem"
      @edit-item="editItem"
      @add-item="addItem"
      @selection-change="selectionChange"
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
    unparsed_sources: [],
    osint_sources: [],
    selected: [],
    formData: {},
    edit: false
  }),
  methods: {
    ...mapActions('config', ['loadOSINTSources']),
    ...mapGetters('config', ['getOSINTSources']),
    ...mapActions(['updateItemCount']),
    updateData() {
      this.loadOSINTSources().then(() => {
        const sources = this.getOSINTSources()
        this.unparsed_sources = sources.items
        const psources = this.parseSource(sources.items)
        this.osint_sources = psources
        this.updateItemCount({
          total: sources.total_count,
          filtered: sources.length
        })
      })
    },
    parseSource(data) {
      const sources = []

      data.forEach(source => {
        const rootLevel = {
          name: source.name,
          id: source.id,
          description: source.description,
          collector_id: source.collector_id
        }

        source.parameter_values.forEach(parameter => {
          rootLevel[parameter.parameter.key] = parameter.value
        })
        sources.push(rootLevel)
      })

      return sources
    },
    parseSubmittedData(data) {
      const result = this.unparsed_sources.find(item => item.id === data.id)

      result.parameter_values.forEach(parameter => {
        parameter.value = data[parameter.parameter.key]
      })

      return result
    },
    addItem() {
      this.formData = emptyValues(this.osint_sources[0])
      this.edit = false
    },
    editItem(item) {
      this.formData = item
      this.edit = true
    },
    handleSubmit(submittedData) {
      const updateItem = this.parseSubmittedData(submittedData)
      console.log(updateItem)
      if (this.edit) {
        this.updateItem(updateItem)
      } else {
        this.createItem(updateItem)
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
