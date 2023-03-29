import { defineStore } from 'pinia'
import { getDashboardData, getTrendingClusters } from '@/api/dashboard'
// import vuexStore from '@/store' // for gradual conversion, see fullUserDetails

export const dashboardStore = defineStore('DashboardStore', {
  state: () => {
    return {
      dashboard_data: {
        total_news_items: 0,
        total_products: 0,
        report_items_completed: 0,
        report_items_in_progress: 0,
        total_database_items: 0,
        latest_collected: '',
        tag_cloud: {}
      },
      clusters: []
    }
  },
  getters: {},
  actions: {
    setDashboardData(data) {
      this.dashboard_data = data
    },
    setClusters(clusters) {
      this.clusters = clusters
    },
    async loadDashboardData() {
      const response = await getDashboardData()
      this.setDashboardData(response.data)
    },
    async loadClusters() {
      // TODO error -> on getTrendingClusters
      const response = await getTrendingClusters()
      this.setClusters(response.data)
    }
  }
})
