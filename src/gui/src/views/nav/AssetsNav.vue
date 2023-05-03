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
          <v-btn color="primary" block @click="addAsset()">
            <v-icon left dark> mdi-view-grid-plus </v-icon>
            New Asset
          </v-btn>
        </v-col>
        <v-col cols="12" align-self="center" class="py-2">
          <v-btn color="primary" block @click="addAssetGroup()">
            <v-icon left dark> mdi-folder-plus-outline </v-icon>
            New Asset Group
          </v-btn>
          {{ search }}
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
import { useAssetsStore } from '@/stores/AssetsStore'
import { useFilterStore } from '@/stores/FilterStore'

export default {
  name: 'AssetsNav',
  components: {
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
      },
      {
        label: 'vulnerability',
        icon: 'mdi-counter',
        type: 'VULNERABILITY',
        direction: 'ASC'
      }
    ]
  }),
  computed: {
    ...mapState(useFilterStore, ['assetFilter']),
    limit: {
      get() {
        return this.assetFilter.limit
      },
      set(value) {
        this.updateAssetFilter({ limit: value })
        this.updateFilteredAssets()
      }
    },
    sort: {
      get() {
        if (!this.assetFilter.order) return 'DATE_DESC'
        return this.assetFilter.order
      },
      set(value) {
        this.updateAssetFilter({ sort: value })
        this.updateFilteredAssets()
      }
    },
    offset: {
      get() {
        return this.assetFilter.offset
      },
      set(value) {
        this.updateAssetFilter({ offset: value })
        this.updateFilteredAssets()
      }
    },
    search: {
      get() {
        return this.assetFilter.search
      },
      set(value) {
        this.updateAssetFilter({ search: value })
        if (!this.awaitingSearch) {
          setTimeout(() => {
            this.updateFilteredAssets()
            this.awaitingSearch = false
          }, 500)
        }

        this.awaitingSearch = true
      }
    },
    navigation_drawer_class() {
      return this.showOmniSearch ? 'mt-12' : ''
    }
  },
  created() {
    const query = Object.fromEntries(
      Object.entries(this.$route.query).filter(([, v]) => v != null)
    )
    this.updateAssetFilter(query)
    console.debug('loaded with query', query)
  },
  methods: {
    ...mapActions(useAssetsStore, ['updateFilteredAssets']),
    ...mapActions(useFilterStore, ['updateAssetFilter']),
    addAsset() {
      this.$router.push('/asset/0')
    },
    addAssetGroup() {
      this.$router.push('/asset-group/0')
    }
  }
}
</script>
