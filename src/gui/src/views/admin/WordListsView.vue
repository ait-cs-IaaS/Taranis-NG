<template>
  <div>
    <DataTable
      v-model:items="word_lists"
      :add-button="true"
      :header-filter="['tag', 'name', 'description']"
      sort-by-item="id"
      :action-column="true"
      @delete-item="deleteItem"
      @edit-item="editItem"
      @add-item="addItem"
      @selection-change="selectionChange"
      @update-items="updateData"
    >
      <template #titlebar>
        <ImportExport @import="importData" @export="exportData"></ImportExport>
      </template>
    </DataTable>
    <EditConfig
      v-if="formData && Object.keys(formData).length > 0"
      :config-data="formData"
      @submit="handleSubmit"
    ></EditConfig>
  </div>
</template>

<script>
import DataTable from '@/components/common/DataTable.vue'
import EditConfig from '@/components/config/EditConfig.vue'
import ImportExport from '@/components/config/ImportExport.vue'
import {
  deleteWordList,
  createWordList,
  updateWordList,
  exportWordList,
  importWordList
} from '@/api/config'
import { notifySuccess, emptyValues, notifyFailure } from '@/utils/helpers'
import { mapActions, mapState, mapWritableState } from 'pinia'
import { useConfigStore } from '@/stores/ConfigStore'

export default {
  name: 'WordLists',
  components: {
    DataTable,
    EditConfig,
    ImportExport
  },
  data: () => ({
    selected: [],
    formData: {},
    edit: false
  }),
  mounted() {
    this.updateData()
  },
  computed: {
    ...mapState(useConfigStore, ['word_lists'])
  },
  methods: {
    ...mapActions(useConfigStore, ['loadWordLists']),
    ...mapWritableState(useMainStore, ['itemCountTotal', 'itemCountFiltered']),
    updateData() {
      this.loadWordLists().then(() => {
        this.itemCountTotal = this.word_lists.total_count
        this.itemCountFiltered = this.word_lists.items.length
      })
    },
    addItem() {
      this.formData = emptyValues(this.word_lists.items[0])
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
      deleteWordList(item)
        .then(() => {
          notifySuccess(`Successfully deleted ${item.name}`)
          this.updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to delete ${item.name}`)
        })
    },
    createItem(item) {
      createWordList(item)
        .then(() => {
          notifySuccess(`Successfully created ${item.name}`)
          this.updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to create ${item.name}`)
        })
    },
    updateItem(item) {
      updateWordList(item)
        .then(() => {
          notifySuccess(`Successfully updated ${item.name}`)
          this.updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to update ${item.name}`)
        })
    },
    importData(data) {
      importWordList(data)
    },
    exportData() {
      exportWordList(this.selected)
    },
    selectionChange(selected) {
      this.selected = selected.map((item) => item.id)
    }
  }
}
</script>
