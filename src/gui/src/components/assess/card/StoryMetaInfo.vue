<template>
  <v-container column class="pa-0 pb-1">
    <v-row>
      <v-col>
        <!-- left column -->
        <v-row>
          <v-col style="max-width: 110px" class="py-0">
            <strong>{{ t('assess.published') }}:</strong>
          </v-col>
          <v-col class="py-0">
            <span :class="published_date_outdated ? 'error--text' : ''">
              {{ getPublishedDate }}
            </span>
            <v-icon
              v-if="published_date_outdated"
              class="ml-1"
              size="small"
              color="error"
              icon="mdi-alert"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col style="max-width: 110px" class="py-0">
            <strong>Tags:</strong>
          </v-col>
          <v-col class="py-0">
            <tag-list
              v-if="story.tags"
              :tags="story.tags"
              :truncate="!detailView"
              :limit="tagLimit"
              :color="detailView"
            />
          </v-col>
        </v-row>
        <!-- /left column -->
      </v-col>
      <v-col
        :cols="detailView ? 10 : 4"
        :style="detailView ? 'margin-left: 120px' : ''"
      >
        <!-- right column -->
        <v-row>
          <v-col class="py-0 pt-2">
            <week-chart
              v-if="!published_date_outdated"
              :chart-height="detailView ? 300 : 250"
              :chart-width="detailView ? 800 : 600"
              :story="story"
            />
          </v-col>
        </v-row>
        <!-- /right column -->
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import TagList from '@/components/assess/card/TagList.vue'
import WeekChart from '@/components/assess/card/WeekChart.vue'
import { useI18n } from 'vue-i18n'
import { computed } from 'vue'
import { useDisplay } from 'vuetify'

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
    const { xlAndUp, mdAndUp, name } = useDisplay()

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

    const tagLimit = computed(() => {
      if (props.detailView) {
        return 20
      }
      return xlAndUp.value ? 5 : 3
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
      mdAndUp,
      tagLimit,
      name,
      t
    }
  }
}
</script>
