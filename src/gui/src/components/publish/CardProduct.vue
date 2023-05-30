<template>
  <v-card>
    <v-toolbar density="compact">
      <v-toolbar-title>{{ container_title }}</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn
        prepend-icon="mdi-content-save"
        color="success"
        variant="flat"
        @click="saveProduct"
      >
        {{ $t('button.save') }}
      </v-btn>
    </v-toolbar>
    <v-card-text>
      {{ product }}
    </v-card-text>
  </v-card>
</template>

<script>
import { ref, computed } from 'vue'
import { createProduct, updateProduct } from '@/api/publish'
import { useI18n } from 'vue-i18n'

export default {
  name: 'CardProduct',
  props: {
    productProp: {
      type: Object,
      required: true
    },
    edit: { type: Boolean, default: false }
  },
  emits: ['productcreated'],
  setup(props, { emit }) {
    const { t } = useI18n()
    const product = ref(props.productProp)
    const required = [(v) => !!v || 'Required']

    const container_title = computed(() => {
      return props.edit
        ? `${t('title.edit')} product - ${product.value.title}`
        : `${t('title.add_new')} product`
    })

    const saveProduct = () => {
      if (props.edit) {
        updateProduct(product.value.id, product.value)
      } else {
        createProduct(product.value).then((response) => {
          this.$router.push('/product/' + response.data)
          emit('productcreated', response.data)
        })
      }
    }

    return {
      product,
      required,
      container_title,
      saveProduct
    }
  }
}
</script>
