<template>
  <v-container fluid style="min-height: 100vh">
    <card-product :product-prop="product" />
  </v-container>
</template>

<script>
import { getProduct } from '@/api/publish'
import CardProduct from '@/components/publish/CardProduct.vue'

export default {
  name: 'ProductView',
  components: {
    CardProduct
  },
  data: () => ({
    default_product: {
      id: null,
      uuid: null,
      title: ''
    },

    product: {},
    edit: true
  }),
  async created() {
    this.products = await this.loadProducts()
  },
  methods: {
    async loadProducts() {
      if (this.$route.params.id && this.$route.params.id !== '0') {
        return await getProduct(this.$route.params.id).then((response) => {
          return response.data
        })
      }
      this.edit = false
      return this.default_product
    }
  }
}
</script>
