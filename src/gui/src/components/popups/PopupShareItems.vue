<template>
  <v-card>
    <v-card-title>
      <span class="headline">Share Items</span>
    </v-card-title>
    <v-card-text>
      Select a report to share the item with:
      <v-select
        v-model="reportItemSelection"
        solo
        single-line
        label="Select Report"
        no-data-text="No reports found"
        :items="reportItems"
      />
    </v-card-text>
    <v-card-actions class="mt-1">
      <v-btn
        color="awake-red-color darken-1"
        outlined
        class="text-lowercase pr-4"
        @click="close()"
      >
        <v-icon left class="red-icon">mdi-close</v-icon>
        abort
      </v-btn>

      <v-btn
        color="primary"
        dark
        depressed
        class="text-lowercase selection-toolbar-btn pr-4"
        @click="share()"
      >
        <v-icon left>mdi-share-outline</v-icon>
        share
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { addAggregatesToReportItem } from '@/api/analyze'

export default {
  name: 'PopupShareItems',
  components: {},
  props: {
    itemIds: {
      type: Array,
      default: () => []
    },
    dialog: Boolean
  },
  emits: ['close'],
  data: () => ({
    reportItems: [],
    reportItemSelection: {}
  }),
  mounted() {
    console.debug('PopupShareItems mounted')
    console.debug(this.item_ids)
    this.loadReportItems().then(() => {
      this.reportItems = this.getReportItems().map((item) => {
        return {
          text: item.title,
          value: item.id
        }
      })
    })
  },
  methods: {
    ...mapGetters('assess', ['getNewsItemById']),
    ...mapGetters('analyze', ['getReportItems']),
    ...mapActions('analyze', ['loadReportItems']),

    share() {
      addAggregatesToReportItem(this.reportItemSelection, this.item_ids)
      this.close()
    },
    close() {
      this.$emit('close')
    }
  }
}
</script>
