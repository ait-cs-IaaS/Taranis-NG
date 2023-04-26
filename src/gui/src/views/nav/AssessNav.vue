<template>
  <filter-navigation
    :search="search"
    @update:search="(value) => (search = value)"
    :limit="limit"
    @update:limit="(value) => (limit = value)"
    :offsest="offset"
    @update:offset="(value) => (offset = value)"
  >
    <template #navdrawer>
      <!-- scope -->
      <v-row class="my-2 mr-0 px-2">
        <v-col cols="12" class="pb-0">
          <h4>Source</h4>
        </v-col>

        <v-col cols="12" class="pt-0">
          <v-select
            v-model="group"
            :items="getOSINTSourceGroupsList"
            prepent-icon="mdi-format-list-numbered"
            item-text="title"
            item-value="id"
            label="Source Group"
            :hide-details="true"
            solo
            clearable
            dense
          ></v-select>
        </v-col>

        <v-col cols="12" class="pt-0">
          <v-select
            v-model="source"
            :items="getOSINTSourcesList"
            prepent-icon="mdi-format-list-numbered"
            item-text="title"
            item-value="id"
            label="Source"
            :hide-details="true"
            solo
            clearable
            dense
          ></v-select>
        </v-col>
      </v-row>

      <v-divider class="mt-0 mb-0"></v-divider>

      <!-- filter results -->
      <v-row class="my-2 mr-0 px-2">
        <v-col cols="12" class="py-0">
          <h4>filter results</h4>
        </v-col>

        <!-- time tags -->
        <v-col cols="12" class="pb-0">
          <date-chips v-model="range" />
        </v-col>

        <!-- tags -->
        <v-col cols="12" class="pr-0">
          <tag-filter />
        </v-col>
      </v-row>

      <v-divider class="mt-0 mb-0"></v-divider>

      <v-row class="my-2 mr-0 px-2">
        <v-col cols="12" class="pt-1">
          <filter-select-list
            v-model="filterAttribute"
            :items="filterAttributeOptions"
          />
        </v-col>
      </v-row>

      <v-divider class="mt-2 mb-0"></v-divider>

      <v-row class="my-2 mr-0 px-2">
        <v-col cols="12" class="py-0">
          <h4>sort by</h4>
        </v-col>

        <v-col cols="12" class="pt-2">
          <filter-sort-list v-model="sort" :items="orderOptions" />
        </v-col>
      </v-row>

      <v-divider class="mt-2 mb-0"></v-divider>

      <v-row class="my-2 mr-0 px-2 pb-5">
        <v-col cols="12" class="py-0">
          <v-btn @click="updateNewsItems()" color="primary" block>
            Reload
            <v-icon right dark> mdi-reload </v-icon>
          </v-btn>
        </v-col>
      </v-row>
    </template>
  </filter-navigation>
</template>

<script>
import { mapGetters, mapState as mapStateVuex } from 'vuex'
import dateChips from '@/components/assess/filter/dateChips'
import tagFilter from '@/components/assess/filter/tagFilter'
import filterSelectList from '@/components/assess/filter/filterSelectList'
import filterSortList from '@/components/assess/filter/filterSortList'
import FilterNavigation from '@/components/common/FilterNavigation'
import { assessStore } from '@/stores/AssessStore'
import { mapActions, mapState } from 'pinia'
import { filterStore } from '@/stores/FilterStore'

export default {
  name: 'AssessNav',
  components: {
    dateChips,
    tagFilter,
    filterSelectList,
    filterSortList,
    FilterNavigation
  },
  data: () => ({
    awaitingSearch: false,
    filterAttributeSelections: [],
    filterAttributeOptions: [
      { type: 'read', label: 'read', icon: 'mdi-email-mark-as-unread' },
      {
        type: 'important',
        label: 'important',
        icon: 'mdi-exclamation'
      },
      {
        type: 'in_report',
        label: 'items in reports',
        icon: 'mdi-share-outline'
      },
      {
        type: 'relevant',
        label: 'relevant',
        icon: 'mdi-bullhorn-outline'
      }
    ],
    orderOptions: [
      {
        label: 'published date',
        icon: 'mdi-calendar-range-outline',
        type: 'DATE',
        direction: 'DESC'
      },
      {
        label: 'relevance',
        icon: 'mdi-counter',
        type: 'RELEVANCE',
        direction: 'DESC'
      }
    ]
  }),
  computed: {
    ...mapState(filterStore, ['newsItemsFilter']),
    ...mapStateVuex(['drawerVisible']),
    source: {
      get() {
        return this.newsItemsFilter.source
      },
      set(value) {
        this.updateFilter({ source: value })
        this.updateNewsItems()
      }
    },
    group: {
      get() {
        return this.newsItemsFilter.group
      },
      set(value) {
        this.updateFilter({ group: value })
        this.updateNewsItems()
      }
    },
    limit: {
      get() {
        return this.newsItemsFilter.limit
      },
      set(value) {
        this.newsItemsFilter.limit = value
        this.updateNewsItems()
      }
    },
    sort: {
      get() {
        if (!this.newsItemsFilter.order) return 'DATE_DESC'
        return this.newsItemsFilter.order
      },
      set(value) {
        this.newsItemsFilter.sort = value
        this.updateNewsItems()
      }
    },
    offset: {
      get() {
        return this.newsItemsFilter.offset
      },
      set(value) {
        this.newsItemsFilter.offset = value
        this.updateNewsItems()
      }
    },
    range: {
      get() {
        return this.newsItemsFilter.range
      },
      set(value) {
        this.updateFilter({ range: value })
        this.updateNewsItems()
      }
    },
    filterAttribute: {
      get() {
        return this.filterAttributeSelections
      },
      set(value) {
        this.filterAttributeSelections = value

        const filterUpdate = this.filterAttributeOptions.reduce((obj, item) => {
          obj[item.type] = value.includes(item.type) ? 'true' : undefined
          return obj
        }, {})

        console.debug('filterAttributeSelections', filterUpdate)
        this.updateFilter(filterUpdate)
        this.updateNewsItems()
      }
    },
    search: {
      get() {
        return this.newsItemsFilter.search
      },
      set(value) {
        this.updateFilter({ search: value })
        if (!this.awaitingSearch) {
          setTimeout(() => {
            this.updateNewsItems()
            this.awaitingSearch = false
          }, 500)
        }

        this.awaitingSearch = true
      }
    },
    ...mapState(assessStore, [
      'getOSINTSourceGroupsList',
      'getOSINTSourcesList'
    ])
  },
  methods: {
    ...mapGetters(['getItemCount']),
    ...mapActions(assessStore, ['updateNewsItems']),
    ...mapActions(filterStore, ['updateFilter'])
  },
  created() {
    const query = Object.fromEntries(
      Object.entries(this.$route.query).filter(([, v]) => v != null)
    )
    this.updateFilter(query)
    console.debug('loaded with query', query)
  }
}
</script>
