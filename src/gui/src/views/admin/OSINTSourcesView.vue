<template>
  <div>
    <DataTable
      v-model:items="osint_sources"
      :add-button="true"
      :header-filter="['tag', 'name', 'description', 'FEED_URL']"
      sort-by-item="id"
      :action-column="true"
      @delete-item="deleteItem"
      @edit-item="editItem"
      @add-item="addItem"
      @update-items="updateData"
      @selection-change="selectionChange"
    >
      <template #titlebar>
        <ImportExport @import="importData" @export="exportData"></ImportExport>
      </template>
    </DataTable>
    <EditConfig
      v-if="formData && Object.keys(formData).length > 0"
      v-model:config-data="formData"
      v-model:form-format="formFormat"
      @submit="handleSubmit"
    ></EditConfig>
  </div>
</template>

<script>
import DataTable from '@/components/common/DataTable.vue'
import EditConfig from '@/components/config/EditConfig.vue'
import ImportExport from '@/components/config/ImportExport.vue'
import {
  deleteOSINTSource,
  createOSINTSource,
  updateOSINTSource,
  exportOSINTSources,
  importOSINTSources
} from '@/api/config'
import { mapActions as mapActionsVuex } from 'vuex'
import {
  notifySuccess,
  objectFromFormat,
  notifyFailure,
  parseParameterValues,
  createParameterValues
} from '@/utils/helpers'
import { mapActions, mapState } from 'pinia'
import { configStore } from '@/stores/ConfigStore'

export default {
  name: 'OSINTSourcesView',
  components: {
    DataTable,
    EditConfig,
    ImportExport
  },
  data: () => ({
    osint_sources: [],
    parameters: {},
    selected: [],
    formData: {},
    collectors: [],
    edit: false
  }),
  computed: {
    ...mapState(configStore, {
      store_collectors: 'collectors',
      store_osint_sources: 'osint_sources'
    }),
    formFormat() {
      const base = [
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
          name: 'collector_id',
          label: 'Collector',
          type: 'select',
          options: this.collectors
        }
      ]
      if (this.parameters[this.formData.collector_id]) {
        return base.concat(this.parameters[this.formData.collector_id])
      }
      return base
    }
  },
  mounted() {
    this.updateData()
  },
  methods: {
    ...mapActions(configStore, ['loadOSINTSources', 'loadCollectors']),
    ...mapActionsVuex(['updateItemCount']),
    updateData() {
      this.loadOSINTSources().then(() => {
        const sources = this.store_osint_sources
        this.osint_sources = parseParameterValues(sources.items)
        this.updateItemCount({
          total: sources.total_count,
          filtered: sources.length
        })
      })
      this.loadCollectors().then(() => {
        const collectors = this.store_collectors
        this.collectors = collectors.items.map((collector) => {
          this.parameters[collector.id] = collector.parameters.map(
            (parameter) => {
              return {
                name: parameter.key,
                label: parameter.name,
                type: 'text'
              }
            }
          )
          return {
            value: collector.id,
            text: collector.name
          }
        })
      })
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
      delete submittedData.parameter_values
      const parameter_list = this.parameters[this.formData.collector_id].map(
        (item) => item.name
      )
      const updateItem = createParameterValues(parameter_list, submittedData)
      if (this.edit) {
        this.updateItem(updateItem)
      } else {
        this.createItem(updateItem)
      }
    },
    deleteItem(item) {
      deleteOSINTSource(item)
        .then(() => {
          notifySuccess(`Successfully deleted ${item.name}`)
          this.updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to delete ${item.name}`)
        })
    },
    createItem(item) {
      createOSINTSource(item)
        .then(() => {
          notifySuccess(`Successfully created ${item.name}`)
          this.updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to create ${item.name}`)
        })
    },
    updateItem(item) {
      updateOSINTSource(item)
        .then(() => {
          notifySuccess(`Successfully updated ${item.name}`)
          this.updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to update ${item.name}`)
        })
    },
    importData(data) {
      importOSINTSources(data)
        .then(() => {
          notifySuccess(`Successfully imported ${data.get('file').name}`)
          setTimeout(this.updateData(), 1000)
        })
        .catch(() => {
          notifyFailure('Failed to import')
        })
    },
    exportData() {
      let queryString = ''
      if (this.selected.length > 0) {
        queryString = 'ids=' + this.selected.join('&ids=')
      }
      exportOSINTSources(queryString)
    },
    selectionChange(selected) {
      this.selected = selected.map((item) => item.id)
    }
  }
}
</script>
