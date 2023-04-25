<template>
  <v-container column class="pa-0 pb-3">
    <v-row no-gutters class="my-1">
      <v-col cols="2">
        <strong>{{ t('assess.published') }}:</strong>
      </v-col>
      <v-col>
        <span :class="published_date_outdated ? 'error--text' : ''">
          {{ getPublishedDate }}
        </span>
        <v-icon
          v-if="published_date_outdated"
          class="ml-3"
          size="small"
          color="error"
          >mdi-alert</v-icon
        >
      </v-col>
    </v-row>
    <v-row no-gutters class="my-1">
      <v-col cols="2" class="d-flex align-center">
        <strong>Tags:</strong>
      </v-col>
      <v-col cols="6">
        <tag-list
          v-if="story.tags"
          :tags="story.tags"
          :truncate="detailView"
          :limit="detailView ? 20 : 5"
          :color="detailView"
        />
      </v-col>
      <v-col :cols="detailView ? 12 : 4">
        <week-chart
          v-if="!published_date_outdated"
          :chart-height="detailView ? 300 : 200"
          :chart-width="detailView ? 800 : 600"
          :story="story"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import TagList from '@/components/assess/card/TagList.vue'
import WeekChart from '@/components/assess/card/WeekChart.vue'
import { useI18n } from 'vue-i18n'
import { computed } from 'vue'

export default {
  name: 'StoryMetaInfo',
  components: {
    TagList,
    WeekChart
  },
  props: {
    story: {
      type: Object,
      required: true
    },
    detailView: {
      type: Boolean,
      default: false
    }
  },
  emits: ['selectItem', 'deleteItem'],
  setup(props) {
    const { d, t } = useI18n()

    const published_dates = computed(() => {
      const pub_dates = props.story.news_items
        .map((item) => item.news_item_data.published)
        .sort()

      return [pub_dates[pub_dates.length - 1], pub_dates[0]]
    })

    const published_date_outdated = computed(() => {
      const pub_date = new Date(published_dates.value[0])
      if (!pub_date) {
        return false
      }
      const oneWeekAgo = new Date()
      oneWeekAgo.setDate(oneWeekAgo.getDate() - 7)
      return oneWeekAgo > pub_date
    })

    const getPublishedDate = computed(() => {
      const pubDateNew = new Date(published_dates.value[0])
      const pubDateNewStr = d(pubDateNew, 'short')
      const pubDateOld = new Date(published_dates.value[1])
      const pubDateOldStr = d(pubDateOld, 'short')
      if (pubDateNew && pubDateOld) {
        return pubDateNewStr === pubDateOldStr
          ? pubDateNewStr
          : `${pubDateOldStr} - ${pubDateNewStr}`
      }
      return ''
    })

    return {
      published_dates,
      published_date_outdated,
      getPublishedDate,
      t
    }
  }
}
</script>
