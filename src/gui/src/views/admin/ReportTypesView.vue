<template>
  <div>
    <data-table
      v-model:items="report_types.items"
      :add-button="true"
      :header-filter="['tag', 'id', 'title', 'description']"
      sort-by-item="id"
      :action-column="true"
      @delete-item="deleteItem"
      @edit-item="editItem"
      @add-item="addItem"
      @update-items="updateData"
    />
    <report-type-form
      v-if="newItem || (formData && Object.keys(formData).length > 0)"
      :report-type-data="formData"
    />
  </div>
</template>

<script>
import DataTable from '@/components/common/DataTable.vue'
import ReportTypeForm from '@/components/config/ReportTypeForm.vue'
import { deleteReportItemType } from '@/api/config'
import { notifySuccess, notifyFailure } from '@/utils/helpers'

import { mapActions, mapState, mapWritableState } from 'pinia'
import { useConfigStore } from '@/stores/ConfigStore'

export default {
  name: 'ReportTypes',
  components: {
    DataTable,
    ReportTypeForm
  },
  data: () => ({
    selected: [],
    formData: {},
    newItem: false
  }),
  mounted() {
    this.updateData()
  },
  computed: {
    ...mapWritableState(useMainStore, ['itemCountTotal', 'itemCountFiltered']),
    ...mapState(useConfigStore, { report_types: 'report_item_types_config' })
  },
  methods: {
    ...mapActions(useConfigStore, ['loadReportTypesConfig']),
    updateData() {
      this.loadReportTypesConfig().then(() => {
        this.itemCountTotal = this.report_types.total_count
        this.itemCountFiltered = this.report_types.items.length
      })
    },
    addItem() {
      this.formData = undefined
      this.newItem = true
    },
    editItem(item) {
      this.newItem = false
      this.formData = item
    },
    deleteItem(item) {
      if (!item.default) {
        deleteReportItemType(item)
          .then(() => {
            notifySuccess(`Successfully deleted ${item.name}`)
            this.updateData()
          })
          .catch(() => {
            notifyFailure(`Failed to delete ${item.name}`)
          })
      }
    },
    selectionChange(selected) {
      this.selected = selected.map((item) => item.id)
    }
  }
}
</script>
