<template>
  <v-card>
    <v-card-title> Share Items </v-card-title>
    <v-card-text>
      Select a report to share the item with:
      {{ reportItemSelection }}
      <v-select
        v-model="reportItemSelection"
        single-line
        label="Select Report"
        no-data-text="No reports found"
        :items="reportItems"
      />
    </v-card-text>
    <v-card-actions class="mt-1">
      <v-btn
        variant="outlined"
        class="text-lowercase text-red-darken-3 ml-3"
        prepend-icon="mdi-close"
        @click="close()"
      >
        abort
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn
        variant="outlined"
        class="text-lowercase text-primary mr-3"
        prepend-icon="mdi-share-outline"
        @click="share()"
      >
        share
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { addAggregatesToReportItem } from '@/api/analyze'
import { useAnalyzeStore } from '@/stores/AnalyzeStore'
import { ref, onMounted } from 'vue'

export default {
  name: 'PopupShareItems',
  props: {
    itemIds: {
      type: Array,
      default: () => []
    },
    dialog: Boolean
  },
  emits: ['close'],
  setup(props, { emit }) {
    const reportItems = ref([])
    const reportItemSelection = ref(null)
    const store = useAnalyzeStore()

    const { loadReportItems, report_items } = store

    const share = () => {
      addAggregatesToReportItem(reportItemSelection.value, props.itemIds)
      emit('close')
    }

    const close = () => {
      emit('close')
    }

    onMounted(async () => {
      console.debug('PopupShareItems mounted')
      console.debug(props.itemIds)
      await loadReportItems()
      reportItems.value = report_items.items.map((item) => {
        return {
          title: item.title,
          value: item.id
        }
      })
    })

    return {
      reportItems,
      reportItemSelection,
      share,
      close
    }
  }
}
</script>
