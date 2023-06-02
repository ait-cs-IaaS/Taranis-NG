<template>
  <DataTable
    :items="products.items"
    :add-button="false"
    :search-bar="false"
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
import { deleteProduct } from '@/api/publish'
import { mapActions, mapState, mapWritableState } from 'pinia'
import { notifySuccess, notifyFailure } from '@/utils/helpers'
import { usePublishStore } from '@/stores/PublishStore'
import { useMainStore } from '@/stores/MainStore'

export default {
  name: 'PruoductView',
  components: {
    DataTable
  },
  data: function () {
    return {
      selected: []
    }
  },
  computed: {
    ...mapWritableState(useMainStore, ['itemCountTotal', 'itemCountFiltered']),
    ...mapState(usePublishStore, ['products'])
  },
  methods: {
    ...mapActions(usePublishStore, ['loadProducts']),
    updateData() {
      this.loadProducts().then(() => {
        this.itemCountTotal = this.products.total_count
        this.itemCountFiltered = this.products.items.length
      })
    },
    addItem() {
      this.$router.push('/report/0')
    },
    editItem(item) {
      this.$router.push('/product/' + item.id)
    },
    deleteItem(item) {
      deleteProduct(item)
        .then(() => {
          notifySuccess(`Successfully deleted ${item.name}`)
          this.updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to delete ${item.name}`)
        })
    },
    selectionChange(selected) {
      this.selected = selected.map((item) => item.id)
    }
  }
}
</script>
