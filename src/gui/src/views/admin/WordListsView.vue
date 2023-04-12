<template>
  <div>
    <DataTable
      :addButton="true"
      :items.sync="word_lists.items"
      :headerFilter="['tag', 'name', 'description']"
      sortByItem="id"
      :actionColumn="true"
      @delete-item="deleteItem"
      @edit-item="editItem"
      @add-item="addItem"
      @selection-change="selectionChange"
      @update-items="updateData"
    >
      <template v-slot:titlebar>
        <ImportExport @import="importData" @export="exportData"></ImportExport>
      </template>
    </DataTable>
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
import ImportExport from '../../components/config/ImportExport'
import {
  deleteWordList,
  createWordList,
  updateWordList,
  exportWordList,
  importWordList
} from '@/api/config'
import { notifySuccess, emptyValues, notifyFailure } from '@/utils/helpers'
import { mapActions, mapState } from 'pinia'
import { configStore } from '@/stores/ConfigStore'
import { mapActions as mapActionsVuex } from 'vuex'

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
  computed: {
    ...mapState(configStore, ['word_lists'])
  },
  methods: {
    ...mapActions(configStore, ['loadWordLists']),
    ...mapActionsVuex(['updateItemCount']),
    updateData() {
      this.loadWordLists().then(() => {
        this.updateItemCount({
          total: this.word_lists.total_count,
          filtered: this.word_lists.length
        })
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
  },
  mounted() {
    this.updateData()
  },
  beforeDestroy() {}
}
</script>
