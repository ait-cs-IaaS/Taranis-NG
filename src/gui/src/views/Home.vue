<template>
  <v-container fluid>
    <v-row no-gutters>
      <dash-board-card
        v-for="cluster in clusters"
        :key="cluster.name"
        :link-to="`/assess?tags=${cluster.name}`"
        :link-text="cluster.name"
      >
        <template #content>
          <trending-card :cluster="cluster" />
        </template>
      </dash-board-card>

      <dash-board-card link-to="/assess" link-text="Assess">
        <template #content>
          <v-icon class="mr-2"> mdi-email-multiple </v-icon>
          <span class="caption">
            There are
            <strong>{{ dashboardData.total_news_items }}</strong> total Assess
            items.
          </span>
        </template>
      </dash-board-card>
      <dash-board-card link-to="/analyze" link-text="Analyze">
        <template #content>
          <v-icon class="mr-2"> mdi-account </v-icon>
          <span class="caption">
            There are <b>{{ dashboardData.report_items_completed }}</b>
            completed analyses.
          </span>
          <v-divider inset></v-divider>
          <v-icon class="mr-2" color="grey">
            mdi-account-question-outline
          </v-icon>
          <span class="caption">
            There are <b>{{ dashboardData.report_items_in_progress }}</b>
            pending analyses.
          </span>
        </template>
      </dash-board-card>
      <dash-board-card link-to="/publish" link-text="Publish">
        <template #content>
          <v-icon class="mr-2" color="orange"> mdi-email-check-outline </v-icon>
          <span class="caption">
            There are <b>{{ dashboardData.total_products }}</b> products ready
            for publications.
          </span>
        </template>
      </dash-board-card>
    </v-row>
  </v-container>
</template>

<script>
import DashBoardCard from '@/components/common/DashBoardCard.vue'
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import TrendingCard from '@/components/common/TrendingCard.vue'
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'HomeView',
  components: {
    DashBoardCard,
    TrendingCard
  },
  setup() {
    const store = useStore()
    const dashboardData = ref({})
    const clusters = ref([])

    const totalItems = () => store.getters['getItemCount'].total

    const loadDashboardData = () =>
      store.dispatch('dashboard/loadDashboardData')
    const loadClusters = () => store.dispatch('dashboard/loadClusters')
    const getDashboardData = () => store.getters['dashboard/getDashboardData']
    const getClusters = () => store.getters['dashboard/getClusters']

    onMounted(async () => {
      await loadDashboardData()
      dashboardData.value = getDashboardData()

      await loadClusters()
      clusters.value = getClusters()
    })

    return {
      dashboardData,
      clusters,
      totalItems
    }
  }
})
</script>
