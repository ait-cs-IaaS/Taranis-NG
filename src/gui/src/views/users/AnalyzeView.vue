<template>
<div>
    <DataTable
      :addButton="true"
      :items.sync="report_items"
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
          <v-icon v-on="on" color="secondary" @click.stop="createProduct(item)"> mdi-file </v-icon>
        </template>
        <span>Create Product</span>
      </v-tooltip>
    </template>
    </DataTable>
</div>
</template>

<script>
import DataTable from '@/components/common/DataTable'
import { deleteReportItem, createReportItem, updateReportItem } from '@/api/analyze'
import { mapActions, mapGetters } from 'vuex'
import { notifySuccess, emptyValues, notifyFailure } from '@/utils/helpers'

export default {
  name: 'Analyze',
  components: {
    DataTable
  },
  data: () => ({
    report_items: [],
    formData: {},
    edit: false
  }),
  methods: {
    ...mapActions('analyze', ['loadReportItems']),
    ...mapGetters('analyze', ['getReportItems']),
    ...mapActions(['updateItemCount']),
    updateData() {
      this.loadReportItems().then(() => {
        const sources = this.getReportItems()
        console.debug(sources)
        this.report_items = sources
        this.updateItemCount({
          total: sources.length,
          filtered: sources.length
        })
      })
    },
    addItem() {
      this.formData = emptyValues(this.report_items[0])
      this.edit = false
    },
    editItem(item) {
      this.$router.push('/report/' + item.id)
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
        deleteReportItem(item).then(() => {
          notifySuccess(`Successfully deleted ${item.name}`)
          this.updateData()
        }).catch(() => {
          notifyFailure(`Failed to delete ${item.name}`)
        })
      }
    },
    createItem(item) {
      createReportItem(item).then(() => {
        notifySuccess(`Successfully created ${item.name}`)
        this.updateData()
      }).catch(() => {
        notifyFailure(`Failed to create ${item.name}`)
      })
    },
    updateItem(item) {
      updateReportItem(item).then(() => {
        notifySuccess(`Successfully updated ${item.name}`)
        this.updateData()
      }).catch(() => {
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
