<template>
  <div>
    <ConfigTable
      :addButton="true"
      :items="osint_sources"
      :headerFilter="['name', 'description', 'id']"
      groupByItem="collector_type"
      @delete-item="deleteItem"
      @edit-item="editItem"
      @add-item="addItem"
    />
  </div>
</template>

<script>
import ConfigTable from '../../components/config/ConfigTable'
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
    ConfigTable
  },
  data: () => ({
    osint_sources: [],
    selected: []
  }),
  methods: {
    ...mapActions('config', ['loadOSINTSources']),
    ...mapGetters('config', ['getOSINTSources']),
    // ...mapGetters('assess', ['getOSINTSources']),
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
    importSources() {
      importOSINTSources(this.selected).then(() => {
        this.message = `Successfully imported ${this.selected.length} sources`
        this.dialog = true
        this.updateData()
      })
    },
    exportSources() {
      exportOSINTSources(this.selected)
    },
    addItem() {
      this.formData = emptyValues(this.organizations[0])
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
        deleteOSINTSource(item).then(() => {
          notifySuccess(`Successfully deleted ${item.name}`)
          this.updateData()
        }).catch(() => {
          notifyFailure(`Failed to delete ${item.name}`)
        })
      }
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
    }
  },
  mounted() {
    this.updateData()
  },
  beforeDestroy() {
  }
}
</script>
