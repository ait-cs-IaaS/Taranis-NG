<template>
  <v-container fluid>
    <v-card v-for="product in products.items" :key="product.id" class="mt-3">
      <v-card-title>
        {{ product }}
      </v-card-title>
    </v-card>
    <h2 v-if="!products.items">No Products found</h2>
  </v-container>
</template>

<script>
import { deleteProduct } from '@/api/publish'
import { mapActions, mapState, mapWritableState } from 'pinia'
import { notifySuccess, notifyFailure } from '@/utils/helpers'
import { usePublishStore } from '@/stores/PublishStore'
import { useMainStore } from '@/stores/MainStore'

export default {
  name: 'PruoductView',
  components: {},
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
    editProduct(item) {
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
