<template>
  <v-container fluid style="min-height: 100vh">
    <card-product v-if="readyToRender" :product-prop="product" />
  </v-container>
</template>

<script>
import { ref, onBeforeMount } from 'vue'
import { getProduct } from '@/api/publish'
import CardProduct from '@/components/publish/CardProduct.vue'
import { useRoute } from 'vue-router'

export default {
  name: 'ProductView',
  components: {
    CardProduct
  },
  setup() {
    const route = useRoute()
    const defaultProduct = ref({
      id: null,
      title: '',
      product_type_id: null,
      report_items: []
    })
    const product = ref(defaultProduct.value)

    const edit = ref(true)
    const readyToRender = ref(false)

    const loadProducts = async () => {
      console.debug('Loading product', route.params.id)
      if (route.params.id && route.params.id !== '0') {
        const response = await getProduct(route.params.id)
        return response.data
      }
      edit.value = false
      return defaultProduct.value
    }

    const reportCreated = () => {
      edit.value = true
    }

    onBeforeMount(async () => {
      product.value = await loadProducts()
      readyToRender.value = true
    })

    return { product, edit, readyToRender, reportCreated }
  }
}
</script>
