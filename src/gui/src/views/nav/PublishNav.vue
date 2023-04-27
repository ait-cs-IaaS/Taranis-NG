<template>
  <filter-navigation
    :search="filter.search"
    :limit="limit"
    :offsest="offset"
    @update:search="(value) => (search = value)"
    @update:limit="(value) => (limit = value)"
    @update:offset="(value) => (offset = value)"
  >
    <template #navdrawer>
      <v-row class="my-2 mr-0 px-2 pb-5">
        <v-col cols="12" align-self="center" class="py-1">
          <v-btn color="primary" block @click="addReport()">
            <v-icon left dark> mdi-chart-box-plus-outline </v-icon>
            New Product
          </v-btn>
        </v-col>
      </v-row>

      <v-divider class="mt-0 mb-0"></v-divider>
      <v-row class="my-2 mr-0 px-2">
        <v-col cols="12" class="py-0">
          <h4>filter</h4>
        </v-col>

        <!-- time tags -->
        <v-col cols="12" class="pb-0">
          <date-chips v-model="range" />
        </v-col>
      </v-row>

      <v-divider class="mt-0 mb-0"></v-divider>
      <v-row class="my-2 mr-0 px-2">
        <v-col cols="12" class="py-0">
          <h4>sort by</h4>
        </v-col>

        <v-col cols="12" class="pt-2">
          <filter-sort-list v-model="sort" :items="orderOptions" />
        </v-col>
      </v-row>
    </template>
  </filter-navigation>
</template>

<script>
import { mapActions, mapState } from 'pinia'
import FilterNavigation from '@/components/common/FilterNavigation.vue'
import filterSortList from '@/components/assess/filter/filterSortList.vue'
import dateChips from '@/components/assess/filter/dateChips.vue'
import { usePublishStore } from '@/stores/PublishStore'
import { useFilterStore } from '@/stores/FilterStore'

export default {
  name: 'PublishNav',
  components: {
    dateChips,
    filterSortList,
    FilterNavigation
  },
  data: () => ({
    awaitingSearch: false,
    orderOptions: [
      {
        label: 'date',
        icon: 'mdi-calendar-range-outline',
        type: 'DATE',
        direction: 'DESC'
      }
    ]
  }),
  computed: {
    ...mapState(useFilterStore, ['productFilter']),
    limit: {
      get() {
        return this.productFilter.limit
      },
      set(value) {
        this.updateProductFilter({ limit: value })
        this.updateProducts()
      }
    },
    sort: {
      get() {
        if (!this.productFilter.order) return 'DATE_DESC'
        return this.productFilter.order
      },
      set(value) {
        this.updateProductFilter({ sort: value })
        this.updateProducts()
      }
    },
    offset: {
      get() {
        return this.productFilter.offset
      },
      set(value) {
        this.updateProductFilter({ offset: value })
        this.updateProducts()
      }
    },
    range: {
      get() {
        return this.productFilter.range
      },
      set(value) {
        this.updateProductFilter({ range: value })
        this.updateProducts()
      }
    },
    search: {
      get() {
        return this.productFilter.search
      },
      set(value) {
        this.updateProductFilter({ search: value })
        if (!this.awaitingSearch) {
          setTimeout(() => {
            this.updateProducts()
            this.awaitingSearch = false
          }, 500)
        }

        this.awaitingSearch = true
      }
    }
  },
  created() {
    const query = Object.fromEntries(
      Object.entries(this.$route.query).filter(([, v]) => v != null)
    )
    this.updateProductFilter(query)
    console.debug('loaded with query', query)
  },
  methods: {
    ...mapActions(usePublishStore, ['updateProducts']),
    ...mapActions(useFilterStore, ['updateProductFilter']),
    addReport() {
      this.$router.push('/product/0')
    }
  }
}
</script>
