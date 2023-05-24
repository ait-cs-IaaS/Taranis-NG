import {
  getNewsItemsAggregates,
  getOSINTSourceGroupsList,
  getOSINTSourcesList
} from '@/api/assess'
import { defineStore } from 'pinia'
import { xorConcat } from '@/utils/helpers'

import { useFilterStore } from './FilterStore'

export const useAssessStore = defineStore('assess', {
  state: () => ({
    multi_select: false,
    selection: [],
    osint_sources: [],
    osint_source_groups: [],
    default_source_group_id: '',
    newsItems: { total_count: 0, items: [] },
    newsItemsSelection: [],
    top_stories: []
  }),
  getters: {
    getMultiSelect() {
      return this.multi_select
    },
    getSelection() {
      return this.selection
    },
    getOSINTSourceGroupsList() {
      return Array.isArray(this.osint_source_groups.items)
        ? this.osint_source_groups.items.map((value) => ({
            id: value.id,
            title: value.name
          }))
        : []
    },
    getOSINTSourcesList() {
      return Array.isArray(this.osint_sources.items)
        ? this.osint_sources.items.map((value) => ({
            id: value.id,
            title: value.name
          }))
        : []
    }
  },
  actions: {
    async updateNewsItems() {
      const filter = useFilterStore()
      const response = await getNewsItemsAggregates(filter.newsItemsFilter)
      this.newsItems = response.data
    },
    async updateOSINTSources() {
      const response = await getOSINTSourcesList()
      this.osint_sources = response.data
    },
    async updateOSINTSourceGroupsList() {
      const response = await getOSINTSourceGroupsList()
      this.osint_source_groups = response.data
      this.default_source_group_id = response.data.items.filter(
        (value) => value.default
      )[0].id
    },
    selectNewsItem(id) {
      this.newsItemsSelection = xorConcat(this.newsItemsSelection, id)
    },
    clearNewsItemSelection() {
      this.newsItemsSelection = []
    },

    multiSelect(data) {
      this.multi_select = data
      this.selection = []
    },

    select(data) {
      this.selection.push(data)
    },

    deselect(data) {
      for (let i = 0; i < this.selection.length; i++) {
        if (
          this.selection[i].type === data.type &&
          this.selection[i].id === data.id
        ) {
          this.selection.splice(i, 1)
          break
        }
      }
    }
  }
})
