<template>
  <div>
    <data-table
      v-model:items="report_types"
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
      v-model:report_type_data="formData"
    />
  </div>
</template>

<script>
import DataTable from '@/components/common/DataTable.vue'
import ReportTypeForm from '@/components/config/ReportTypeForm.vue'
import { deleteReportItemType } from '@/api/config'
import { mapActions, mapGetters } from 'vuex'
import { notifySuccess, notifyFailure } from '@/utils/helpers'

export default {
  name: 'ReportTypes',
  components: {
    DataTable,
    ReportTypeForm
  },
  data: () => ({
    report_types: [],
    selected: [],
    formData: {},
    newItem: false
  }),
  computed: {},
  mounted() {
    this.updateData()
  },
  methods: {
    ...mapActions('config', ['loadReportTypesConfig']),
    ...mapGetters('config', ['getReportTypesConfig']),
    ...mapActions(['updateItemCount']),
    updateData() {
      this.loadReportTypesConfig().then(() => {
        const sources = this.getReportTypesConfig()
        this.report_types = sources.items
        this.updateItemCount({
          total: sources.total_count,
          filtered: sources.length
        })
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
