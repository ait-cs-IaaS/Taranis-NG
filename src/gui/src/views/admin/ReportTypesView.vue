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
import { defineComponent, ref } from 'vue'
import DataTable from '@/components/common/DataTable.vue'
import ReportTypeForm from '@/components/config/ReportTypeForm.vue'
import { deleteReportItemType } from '@/api/config'
import { notifySuccess, notifyFailure } from '@/utils/helpers'

import { useConfigStore } from '@/stores/ConfigStore'
import { useMainStore } from '@/stores/MainStore'

export default defineComponent({
  name: 'ReportTypes',
  components: {
    DataTable,
    ReportTypeForm
  },
  setup() {
    const selected = ref([])
    const formData = ref({})
    const newItem = ref(false)

    const report_types = useConfigStore().report_item_types_config
    const mainStore = useMainStore()

    const updateData = () => {
      loadReportTypesConfig().then(() => {
        mainStore.itemCountTotal = report_types.total_count
        mainStore.itemCountFiltered = report_types.items.length
      })
    }

    const addItem = () => {
      formData.value = undefined
      newItem.value = true
    }

    const editItem = (item) => {
      newItem.value = false
      formData.value = item
    }

    const deleteItem = (item) => {
      if (!item.default) {
        deleteReportItemType(item)
          .then(() => {
            notifySuccess(`Successfully deleted ${item.name}`)
            updateData()
          })
          .catch(() => {
            notifyFailure(`Failed to delete ${item.name}`)
          })
      }
    }

    const selectionChange = (selected) => {
      selected.value = selected.map((item) => item.id)
    }

    return {
      selected,
      formData,
      newItem,
      report_types,
      addItem,
      editItem,
      deleteItem,
      selectionChange,
      updateData
    }
  }
})
</script>
