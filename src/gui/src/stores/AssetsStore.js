import {
  getAllAssetGroups,
  getAllAssets,
  getAllNotificationTemplates
} from '@/api/assets'
import { defineStore } from 'pinia'
import { filter } from '@/store/filter'

export const assetsStore = defineStore('assets', {
  state: () => {
    return {
      asset_groups: { total_count: 0, items: [] },
      notification_templates: { total_count: 0, items: [] },
      assets: { total_count: 0, items: [] }
    }
  },
  actions: {
    loadAssetGroups(data) {
      return getAllAssetGroups(data).then((response) => {
        this.asset_groups = response.data
      })
    },
    loadAssets(data) {
      return getAllAssets(data).then((response) => {
        this.assets = response.data
      })
    },
    loadNotificationTemplates(data) {
      return getAllNotificationTemplates(data).then((response) => {
        this.notification_templates = response.data
      })
    },
    updateFilteredAssets() {
      return getAllAssets(filter.state.assetFilter).then((response) => {
        this.assets = response.data
      })
    }
  }
})
