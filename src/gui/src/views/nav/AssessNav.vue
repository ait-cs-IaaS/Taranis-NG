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
      <!-- scope -->
      <v-row class="my-2 mr-0 px-2">
        <v-col cols="12" class="pb-0">
          <h4>Source</h4>
        </v-col>

        <v-col cols="12" class="pt-0">
          <v-select
            v-model="group"
            :items="getOSINTSourceGroupsList"
            item-title="title"
            item-value="id"
            label="Source Group"
            :hide-details="true"
            variant="solo"
            clearable
            density="compact"
          ></v-select>
        </v-col>

        <v-col cols="12" class="pt-0">
          <v-select
            v-model="source"
            :items="getOSINTSourcesList"
            item-title="title"
            item-value="id"
            label="Source"
            :hide-details="true"
            variant="solo"
            clearable
            density="compact"
          ></v-select>
        </v-col>
      </v-row>

      <v-divider class="mt-0 mb-0"></v-divider>

      <!-- filter results -->
      <v-row class="my-2 mr-0 px-2">
        <v-col cols="12" class="py-0">
          <h4>filter results</h4>
        </v-col>

        <!-- time range -->
        <v-col cols="12" class="pb-0">
          <date-chips v-model="range" />
        </v-col>

        <!-- tags -->
        <v-col cols="12" class="pr-0">
          <tag-filter v-model="tags" />
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
          <v-btn color="primary" block @click="updateNewsItems()">
            Reload
            <v-icon right dark> mdi-reload </v-icon>
          </v-btn>
        </v-col>
      </v-row>
    </template>
  </filter-navigation>
</template>

<script>
import dateChips from '@/components/assess/filter/dateChips.vue'
import tagFilter from '@/components/assess/filter/tagFilter.vue'
import filterSelectList from '@/components/assess/filter/filterSelectList.vue'
import filterSortList from '@/components/assess/filter/filterSortList.vue'
import FilterNavigation from '@/components/common/FilterNavigation.vue'
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useFilterStore } from '@/stores/FilterStore'
import { useAssessStore } from '@/stores/AssessStore'

export default {
  name: 'AssessNav',
  components: {
    dateChips,
    tagFilter,
    filterSelectList,
    filterSortList,
    FilterNavigation
  },
  setup() {
    const store = useFilterStore()
    const assessStore = useAssessStore()
    const route = useRoute()
    const awaitingSearch = ref(false)
    const filterAttributeSelections = ref([])
    const filterAttributeOptions = [
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
    ]
    const orderOptions = [
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

    const filter = computed(() => {
      return store.filter.newsItemsFilter
    })

    const drawerVisible = computed(() => {
      return store.drawerVisible
    })

    const source = computed({
      get() {
        return filter.value.source
      },
      set(value) {
        store.setFilter({ source: value })
        updateNewsItems()
      }
    })

    const group = computed({
      get() {
        return filter.value.group
      },
      set(value) {
        store.setFilter({ group: value })
        updateNewsItems()
      }
    })

    const limit = computed({
      get() {
        return filter.value.limit
      },
      set(value) {
        store.setLimit(value)
        updateNewsItems()
      }
    })

    const sort = computed({
      get() {
        if (!filter.value.order) return 'DATE_DESC'
        return filter.value.order
      },
      set(value) {
        store.setSort(value)
        updateNewsItems()
      }
    })

    const offset = computed({
      get() {
        return filter.value.offset
      },
      set(value) {
        store.setOffset(value)
        updateNewsItems()
      }
    })

    const tags = computed({
      get() {
        const tags = store.getFilterTags || []
        return tags.map((tag) => {
          return { name: tag }
        })
      },
      set(value) {
        store.setFilter({ tags: value })
        updateNewsItems()
      }
    })

    const range = computed({
      get() {
        return filter.value.range
      },
      set(value) {
        store.setFilter({ range: value })
        updateNewsItems()
      }
    })

    const filterAttribute = computed({
      get() {
        return filterAttributeSelections.value
      },
      set(value) {
        filterAttributeSelections.value = value

        const filterUpdate = filterAttributeOptions.reduce((obj, item) => {
          obj[item.type] = value.includes(item.type) ? 'true' : undefined
          return obj
        }, {})

        console.debug('filterAttributeSelections', filterUpdate)
        store.setFilter(filterUpdate)
        updateNewsItems()
      }
    })

    const search = computed({
      get() {
        return this.newsItemsFilter.search
      },
      set(value) {
        store.setFilter({ search: value })
        if (!awaitingSearch.value) {
          setTimeout(() => {
            updateNewsItems()
            awaitingSearch.value = false
          }, 500)
        }

        awaitingSearch.value = true
      }
    })

    const getOSINTSourceGroupsList = computed(() => {
      return assessStore.getOSINTSourceGroupsList
    })

    const getOSINTSourcesList = computed(() => {
      return assessStore.getOSINTSourcesList
    })

    const getNewsItemsFilter = computed(() => {
      return store.newsItemsFilter
    })

    const updateNewsItems = () => {
      assessStore.updateNewsItems()
    }

    onMounted(() => {
      const query = Object.fromEntries(
        Object.entries(route.query).filter(([, v]) => v != null)
      )
      updateFilter(query)
      console.debug('loaded with query', query)
    })

    return {
      awaitingSearch,
      filterAttributeSelections,
      filterAttributeOptions,
      orderOptions,
      filter,
      drawerVisible,
      source,
      group,
      limit,
      sort,
      offset,
      tags,
      range,
      filterAttribute,
      search,
      getItemCount,
      getOSINTSourceGroupsList,
      getOSINTSourcesList,
      updateFilter,
      getNewsItemsFilter,
      updateNewsItems
    }
  }
}
</script>
