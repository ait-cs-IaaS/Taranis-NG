<template>
  <v-container id="selector">
    <component
      :is="cardLayout()"
      v-for="collection in collections"
      :key="collection.id"
      :card="collection"
      :delete-permission="deletePermission"
    ></component>
  </v-container>
</template>

<script>
import CardAssess from '@/components/assess/legacy/CardAssess.vue'
import CardAnalyze from '@/components/analyze/CardAnalyze.vue'
import CardProduct from '@/components/publish/CardProduct.vue'

export default {
  name: 'ContentData',
  components: {
    CardAssess,
    CardAnalyze,
    CardProduct
  },
  props: {
    name: String,
    action: String,
    getter: String,
    cardItem: String,
    deletePermission: String
  },
  data: () => ({
    collections: [],
    filter: {
      search: ''
    }
  }),
  mounted() {
    this.updateData()
    this.$root.$on('notification', () => {
      this.updateData()
    })
    this.$root.$on('update-data', () => {
      this.updateData()
    })
    this.$root.$on('update-items-filter', (filter) => {
      this.filter = filter
      this.updateData()
    })
  },
  beforeUnmount() {
    this.$root.$off('notification')
    this.$root.$off('update-data')
    this.$root.$off('update-items-filter')
  },
  methods: {
    updateData() {
      this.$store.dispatch(this.action, this.filter).then(() => {
        this.collections = this.$store.getters[this.getter].items
      })
    },
    cardLayout: function () {
      return this.cardItem
    }
  }
}
</script>
