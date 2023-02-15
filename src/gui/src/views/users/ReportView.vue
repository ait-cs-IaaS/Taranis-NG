<template>
  <v-container fluid style="min-height: 100vh">
    <report-item :report_item_prop="report_item" :edit="true"/>
  </v-container>
</template>

<script>
import { getReportItem } from '@/api/analyze'
import ReportItem from '@/components/analyze/ReportItem'

export default {
  name: 'ReportView',
  data: () => ({
    report_item: {}
  }),
  components: {
    ReportItem
  },
  async created() {
    this.report_item = await this.loadReportItem()
    console.debug(this.report_item)
  },
  methods: {
    async loadReportItem() {
      if (this.$route.params.id) {
        return await getReportItem(this.$route.params.id).then((response) => {
          return response.data
        })
      }
    }
  }
}
</script>
