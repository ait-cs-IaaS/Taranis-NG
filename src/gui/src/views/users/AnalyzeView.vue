<template>
  <DataTable
    :addButton="true"
    :items.sync="report_items.items"
    :headerFilter="['tag', 'title', 'created']"
    sortByItem="id"
    :actionColumn="true"
    @delete-item="deleteItem"
    @edit-item="editItem"
    @add-item="addItem"
    @update-items="updateData"
    @selection-change="selectionChange"
  >
    <template v-slot:actionColumn>
      <v-tooltip left>
        <template v-slot:activator="{ on }">
          <v-icon v-on="on" color="secondary" @click.stop="createProduct(item)">
            mdi-file
          </v-icon>
        </template>
        <span>Create Product</span>
      </v-tooltip>
    </template>
  </DataTable>
</template>

<script>
import DataTable from '@/components/common/DataTable'
import {
  deleteReportItem,
  createReportItem,
  updateReportItem
} from '@/api/analyze'
import { mapActions as mapActionsVuex } from 'vuex'
import { notifySuccess, notifyFailure } from '@/utils/helpers'
import { mapActions, mapState } from 'pinia'
import { analyzeStore } from '@/stores/AnalyzeStore'

export default {
  name: 'Analyze',
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
  computed: {
    ...mapState(analyzeStore, ['report_items', 'report_item_types'])
  },
  methods: {
    ...mapActions(analyzeStore, ['loadReportItems', 'loadReportTypes']),
    ...mapActionsVuex(['updateItemCount']),
    updateData() {
      this.loadReportItems().then(() => {
        this.updateItemCount({
          total: this.report_items.items.length,
          filtered: this.report_items.items.length
        })
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
  },
  mounted() {
    this.updateData()
  },
  beforeDestroy() {}
}
</script>
