<template>
  <DataTable
    :items="report_items"
    :add-button="false"
    :search-bar="false"
    :header-filter="['tag', 'completed', 'title', 'created']"
    sort-by-item="id"
    :action-column="true"
    @delete-item="deleteItem"
    @edit-item="editItem"
    @add-item="addItem"
    @update-items="updateData"
    @selection-change="selectionChange"
  >
    <template #actionColumn>
      <v-tooltip left>
        <template #activator="{ props }">
          <v-icon
            v-bind="props"
            color="secondary"
            @click.stop="createProduct(item)"
          >
            mdi-file
          </v-icon>
        </template>
        <span>Create Product</span>
      </v-tooltip>
    </template>
  </DataTable>
</template>

<script>
import DataTable from '@/components/common/DataTable.vue'
import {
  deleteReportItem,
  createReportItem,
  updateReportItem
} from '@/api/analyze'
import { notifySuccess, notifyFailure } from '@/utils/helpers'
import { mapActions, mapState, mapWritableState } from 'pinia'
import { useAnalyzeStore } from '@/stores/AnalyzeStore'
import { useMainStore } from '@/stores/MainStore'

export default {
  name: 'AnalyzeView',
  components: {
    DataTable
  },
  data: () => ({
    report_types: {},
    selected: [],
    report_item: {
      report_item_type_id: null,
      title_prefix: '',
      title: ''
    }
  }),
  mounted() {
    this.updateData()
  },
  computed: {
    ...mapWritableState(useMainStore, ['itemCountTotal', 'itemCountFiltered']),
    ...mapState(useAnalyzeStore, ['report_items', 'report_item_types'])
  },
  methods: {
    ...mapActions(useAnalyzeStore, ['loadReportItems', 'loadReportTypes']),
    updateData() {
      this.loadReportItems().then(() => {
        this.itemCountTotal = this.newsItems.total_count
        this.itemCountFiltered = this.items.length
      })
      this.loadReportTypes().then(() => {
        this.report_types = this.report_item_types.items
      })
    },
    addItem() {
      this.$router.push('/report/0')
    },
    editItem(item) {
      this.$router.push('/report/' + item.id)
    },
    handleSubmit(submittedData) {
      console.log(submittedData)
    },
    deleteItem(item) {
      deleteReportItem(item)
        .then(() => {
          notifySuccess(`Successfully deleted ${item.name}`)
          this.updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to delete ${item.name}`)
        })
    },
    createItem(item) {
      createReportItem(item)
        .then(() => {
          notifySuccess(`Successfully created ${item.name}`)
          this.updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to create ${item.name}`)
        })
    },
    updateItem(item) {
      updateReportItem(item)
        .then(() => {
          notifySuccess(`Successfully updated ${item.name}`)
          this.updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to update ${item.name}`)
        })
    },
    createProduct() {
      this.$router.push({ name: 'product', params: { id: null } })
    },
    selectionChange(selected) {
      this.selected = selected.map((item) => item.id)
    }
  }
}
</script>
