<template>
  <v-container fluid>
    <v-row no-gutters>
      <dash-board-card link-to="/assess" link-text="Assess" cols="6">
        <template #content>
          <v-icon class="mr-2"> mdi-email-multiple </v-icon>
          <span class="caption">
            There are
            <strong>{{ dashboardData.total_news_items }}</strong> total Assess
            items.
          </span>
        </template>
      </dash-board-card>
      <dash-board-card link-to="/publish" link-text="Publish" cols="6">
        <template #content>
          <v-icon class="mr-2" color="orange"> mdi-email-check-outline </v-icon>
          <span class="caption">
            There are <b>{{ dashboardData.total_products }}</b> products ready
            for publications.
          </span>
        </template>
      </dash-board-card>
    </v-row>
    <v-row no-gutters>
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
      <dash-board-card link-to="/config/nodes" link-text="Nodes">
        <template #content>
          <v-icon class="mr-2" color="green">
            mdi-lightbulb-off-outline
          </v-icon>
          <span class="caption">Collectors are pending</span>
          <v-divider inset></v-divider>

          <v-icon class="mr-2"> mdi-clock-check-outline </v-icon>
          <span class="caption"
            >Last successful run ended at
            <b>{{ dashboardData.latest_collected }}</b></span
          >
        </template>
      </dash-board-card>
      <dash-board-card link-to="#" link-text="Database">
        <template #content>
          <v-icon class="mr-2" color="blue"> mdi-database </v-icon>
          <span class="caption"
            >There are <b>{{ dashboardData.total_database_items }}</b> live
            items.</span
          >
          <v-divider inset></v-divider>

          <v-icon class="mr-2"> mdi-database-check </v-icon>
          <span class="caption">There are <b>0</b> archived items.</span>
        </template>
      </dash-board-card>
    </v-row>
  </v-container>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import DashBoardCard from '@/components/common/DashBoardCard.vue'

export default {
  name: 'DashBoardConfig',
  components: { DashBoardCard },
  setup() {
    const store = useStore()
    const dashboardData = ref({})

    const loadDashboardData = () =>
      store.dispatch('dashboard/loadDashboardData')
    const getDashboardData = () => store.getters['dashboard/getDashboardData']
    const getItemCount = () => store.getters['getItemCount']

    const totalItems = ref(0)

    const updateDashboardData = () => {
      loadDashboardData().then(() => {
        dashboardData.value = getDashboardData()
        totalItems.value = getItemCount().total
      })
    }

    onMounted(updateDashboardData)

    return {
      dashboardData,
      totalItems
    }
  }
}
</script>
