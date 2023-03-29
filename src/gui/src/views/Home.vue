<template>
  <v-container fluid>
    <v-row no-gutters>
      <dash-board-card v-for="cluster in clusters" :key="cluster.name" :linkTo="`/assess?tags=${cluster.name}`"
        :linkText="cluster.name">
        <template v-slot:content>
          <trending-card :cluster="cluster" />
        </template>
      </dash-board-card>

      <dash-board-card linkTo="/assess" linkText="Assess">
        <template v-slot:content>
          <v-icon class="mr-2"> mdi-email-multiple </v-icon>
          <span class="caption">
            There are <strong>{{ dashboard_data.total_news_items }}</strong> total
            Assess items.
          </span>
        </template>
      </dash-board-card>
      <dash-board-card linkTo="/analyze" linkText="Analyze">
        <template v-slot:content>
          <v-icon class="mr-2"> mdi-account </v-icon>
          <span class="caption">
            There are <b>{{ dashboard_data.report_items_completed }}</b>
            completed analyses.
          </span>
          <v-divider inset></v-divider>
          <v-icon class="mr-2" color="grey">
            mdi-account-question-outline
          </v-icon>
          <span class="caption">
            There are <b>{{ dashboard_data.report_items_in_progress }}</b>
            pending analyses.
          </span>
        </template>
      </dash-board-card>
      <dash-board-card linkTo="/publish" linkText="Publish">
        <template v-slot:content>
          <v-icon class="mr-2" color="orange">
            mdi-email-check-outline
          </v-icon>
          <span class="caption">
            There are <b>{{ dashboard_data.total_products }}</b> products
            ready for publications.
          </span>
        </template>
      </dash-board-card>
    </v-row>
  </v-container>
</template>

<script>
import DashBoardCard from '@/components/common/DashBoardCard'
import { mapGetters } from 'vuex'
import TrendingCard from '@/components/common/TrendingCard'
import { mapActions, mapState } from 'pinia'
import { dashboardStore } from '../stores/DashboardStore'

export default {
  name: 'Home',
  components: {
    DashBoardCard,
    TrendingCard
  },
  data: () => ({
  }),
  computed: {
    totalItems() {
      return this.getItemCount().total
    },
    ...mapState(dashboardStore, ['dashboard_data', 'clusters'])
  },
  methods: {
    ...mapActions(dashboardStore, ['loadDashboardData', 'loadClusters']),
    ...mapGetters(['getItemCount'])
  },
  // TODO loadClusters() ?
  async mounted() {
    await this.loadDashboardData()
    await this.loadClusters()
  }
}
</script>
