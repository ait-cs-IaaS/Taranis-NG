<template>
  <span :class="news_item_summary_class">
    <v-tooltip v-if="isSummarized" top>
      <template #activator="{ props }">
        <v-icon v-bind="props">mdi-text-short</v-icon>
      </template>
      <span>This text is Summarized</span>
    </v-tooltip>
    <span v-dompurify-html="highlight_text"></span>
  </span>
</template>

<script>
import { ref, computed } from 'vue'
import { useFilterStore } from '@/stores/FilterStore'
import { storeToRefs } from 'pinia'

export default {
  name: 'SummarizedContent',
  props: {
    content: {
      type: String,
      default: ''
    },
    isSummarized: {
      type: Boolean,
      default: false
    },
    open: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    const filterStore = useFilterStore()
    const { newsItemsFilter } = storeToRefs(filterStore)
    const colorStart = ref(Math.floor(Math.random() * 9))

    const news_item_summary_class = computed(() => {
      return props.open ? 'news-item-summary-no-clip' : 'news-item-summary'
    })

    function removeRegexSpecialChars(string) {
      return string.replace(/[.*+?^${}()<>|[\]\\]/g, '')
    }
    const highlight_text = computed(() => {
      const term = removeRegexSpecialChars(newsItemsFilter.value.search)
      if (!term) return props.content
      console.debug('highlight text with term: ', term)
      let results = props.content
      results = results.replace(
        new RegExp(term, 'gi'),
        (match) => `<mark>${match}</mark>`
      )
      return results
    })

    return {
      colorStart,
      news_item_summary_class,
      highlight_text
    }
  }
}
</script>

<style scoped>
.news-item-summary {
  margin-bottom: 0px !important;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 4;
  line-clamp: 4;
  -webkit-box-orient: vertical;
  height: calc(1.5em * 4);
}
.news-item-summary-no-clip {
  margin-bottom: 0px !important;
  min-height: 6em;
}
</style>
