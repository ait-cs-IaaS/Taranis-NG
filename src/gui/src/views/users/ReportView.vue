<template>
  <v-container fluid style="min-height: 100vh">
    <report-item :report_item_prop="report_item" :edit="edit" />
  </v-container>
</template>

<script>
import { getReportItem } from '@/api/analyze'
import ReportItem from '@/components/analyze/ReportItem'

export default {
  name: 'ReportView',
  data: () => ({
    report_item: {},
    default_report_item: {
      id: null,
      uuid: null,
      title: '',
      title_prefix: '',
      completed: false,
      report_item_type_id: null,
      news_item_aggregates: [],
      remote_report_items: [],
      attributes: []
    },
    edit: true
  }),
  components: {
    ReportItem
  },
  async created() {
    this.report_item = await this.loadReportItem()
    if (this.report_item === undefined) {
      this.report_item = this.default_report_item
      this.edit = false
    }
  },
  methods: {
    async loadReportItem() {
      if (this.$route.params.id && this.$route.params.id !== '0') {
        return await getReportItem(this.$route.params.id).then((response) => {
          return response.data
        })
      }
    }
  }
}
</script>
