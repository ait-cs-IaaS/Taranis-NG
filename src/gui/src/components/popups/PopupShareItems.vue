<template>
  <v-card>
    <v-card-title>
      <span class="headline">Share Items</span>
    </v-card-title>
    <v-card-text>
      Select a report to share the item with:
      <v-select
        solo
        single-line
        label="Select Report"
        v-model="reportItemSelection"
        no-data-text="No reports found"
        :items="reportItems"
      />
    </v-card-text>
    <v-card-actions class="mt-1">
      <v-btn
        color="awake-red-color darken-1"
        outlined
        @click="close()"
        class="text-lowercase pr-4"
      >
        <v-icon left class="red-icon">mdi-close</v-icon>
        abort
      </v-btn>

      <v-btn
        color="primary"
        dark
        depressed
        @click="share()"
        class="text-lowercase selection-toolbar-btn pr-4"
      >
        <v-icon left>mdi-share-outline</v-icon>
        share
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { addAggregatesToReportItem } from '@/api/analyze'
import { analyzeStore } from '@/stores/AnalyzeStore'
import { mapActions, mapState } from 'pinia'

export default {
  name: 'PopupShareItems',
  components: {},
  props: {
    item_ids: [],
    dialog: Boolean
  },
  emits: ['close'],
  data: () => ({
    reportItems: [],
    reportItemSelection: {}
  }),
  computed: {
    ...mapState(analyzeStore, ['report_items'])
  },
  methods: {
    ...mapActions(analyzeStore, ['loadReportItems']),
    share() {
      addAggregatesToReportItem(this.reportItemSelection, this.item_ids)
      this.close()
    },
    close() {
      this.$emit('close')
    }
  },
  mounted() {
    console.debug('PopupShareItems mounted')
    console.debug(this.item_ids)
    this.loadReportItems().then(() => {
      this.reportItems = this.report_items.items.map((item) => {
        return {
          text: item.title,
          value: item.id
        }
      })
    })
  }
}
</script>
