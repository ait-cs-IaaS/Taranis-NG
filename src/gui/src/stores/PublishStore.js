import { getAllProducts } from '@/api/publish'
import { getAllUserPublishersPresets } from '@/api/user'
import { filter } from '@/store/filter'
import { defineStore } from 'pinia'

export const publishStore = defineStore('publish', {
  state: () => ({
    products: { total_count: 0, items: [] },
    products_publisher_presets: { total_count: 0, items: [] }
  }),
  actions: {
    async loadProducts(data) {
      const response = await getAllProducts(data)
      this.products = response.data
    },
    async updateProducts() {
      const response = await getAllProducts(filter.state.productFilter)
      this.products = response.data
    },
    async loadUserPublishersPresets(context, data) {
      const response = await getAllUserPublishersPresets(data)
      this.products_publisher_presets = response.data
    }
  }
})
