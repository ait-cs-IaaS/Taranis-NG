<template>
  <v-row dense class="ma-0 pa-0">
    <v-row dense class="mx-0 mb-0 mt-2 py-0 px-5">
      <!-- DIALOGS -->
      <v-dialog :value="deleteDialog" width="auto">
        <popup-delete-item
          :news-item="story"
          @delete-item="deleteNewsItem()"
          @close="deleteDialog = false"
        />
      </v-dialog>
      <v-dialog :value="sharingDialog" width="auto">
        <popup-share-items
          :item-ids="[story.id]"
          @close="sharingDialog = false"
        />
      </v-dialog>

      <v-col cols="12" class="pb-0">
        <v-card
          v-ripple="false"
          tile
          elevation="3"
          rounded="0"
          class="no-gutters align-self-stretch pl-5 pb-5 pr-3 pt-3"
          :class="[
            {
              selected: selected
            }
          ]"
          @click="toggleSelection"
        >
          <v-row>
            <!-- STORY TITLE -->
            <v-col
              cols="12"
              sm="12"
              lg="6"
              class="d-flex flex-grow-1 mt-3 px-5 py-3 order-1"
              align-self="center"
            >
              <v-icon v-if="story_in_report" class="mr-2 my-auto">
                mdi-share
              </v-icon>
              <h2 class="news-item-title">
                {{ story.title }}
              </h2>
            </v-col>

            <!-- STORY ACTIONS -->
            <v-col
              cols="12"
              sm="12"
              lg="6"
              class="d-flex flex-row flex-grow-1 mt-3 px-5 py-2 order-md-2 order-sm-3"
              style="justify-content: space-evenly"
            >
              <v-btn
                v-if="!detailView"
                v-ripple="false"
                size="small"
                class="item-action-btn"
                variant="tonal"
                :to="'/story/' + story.id"
                @click.stop
              >
                <span>Details</span>
                <v-icon right class="ml-2">mdi-text-box-search-outline</v-icon>
              </v-btn>

              <v-btn
                v-ripple="false"
                size="small"
                class="item-action-btn"
                variant="tonal"
                @click.stop="sharingDialog = true"
              >
                <span>Add to Report</span>
                <v-icon right class="ml-2"
                  >mdi-google-circles-communities</v-icon
                >
              </v-btn>

              <v-btn
                v-if="!detailView"
                v-ripple="false"
                size="small"
                class="item-action-btn open-close-btn"
                :class="openSummary ? 'opened' : 'closed'"
                variant="tonal"
                :style="{ minWidth: minButtonWidth }"
                @click.stop="openSummary = !openSummary"
              >
                <span>{{ news_item_summary_text }}</span>
                <span v-if="news_item_length > 1" class="primary--text"
                  >&nbsp;[{{ news_item_length }}]</span
                >
                <v-icon right class="ml-2">mdi-chevron-down</v-icon>
              </v-btn>

              <v-btn
                v-ripple="false"
                size="small"
                class="item-action-btn"
                variant="tonal"
                @click.stop="markAsRead()"
              >
                <span>mark as read</span>
                <v-icon right class="ml-2" c>mdi-eye-outline</v-icon>
              </v-btn>

              <votes v-if="detailView" :story="story" />

              <v-menu bottom offset-y>
                <template #activator="{ props }">
                  <v-btn
                    v-ripple="false"
                    size="small"
                    class="item-action-btn expandable"
                    variant="tonal"
                    v-bind="props"
                  >
                    <v-icon>mdi-dots-vertical</v-icon>
                  </v-btn>
                </template>

                <v-list class="extraActionsList" dense>
                  <v-list-item
                    class="hidden-xl-only"
                    @click.stop="markAsRead()"
                  >
                    <v-icon left size="small" class="mr-2"
                      >mdi-eye-outline</v-icon
                    >mark as read
                  </v-list-item>
                  <v-list-item @click.stop="markAsImportant()">
                    <v-icon left size="small" class="mr-2"
                      >mdi-star-outline</v-icon
                    >mark as important
                  </v-list-item>
                  <v-list-item @click.stop>
                    <v-icon left size="small" class="mr-2"
                      >mdi-bookmark-outline</v-icon
                    >mark as trusted author
                  </v-list-item>
                  <v-list-item @click.stop="deleteDialog = true">
                    <v-icon left size="small" class="mr-2"
                      >mdi-delete-outline</v-icon
                    >delete
                  </v-list-item>
                </v-list>
              </v-menu>
            </v-col>
            <!-- DESCRIPTION -->
            <v-col
              cols="12"
              sm="12"
              lg="6"
              class="px-5 order-md-3 order-sm-2"
              align-self="stretch"
            >
              <summarized-content
                :open="openSummary"
                :is_summarized="is_summarized"
                :content="getDescription()"
              />
            </v-col>
            <!-- META INFO -->
            <v-col class="px-5 pt-2 pb-3 order-4" cols="12" sm="12" lg="6">
              <v-container column class="pa-0 pb-3">
                <v-row no-gutters class="my-1">
                  <v-col cols="2">
                    <strong>{{ $t('assess.published') }}:</strong>
                  </v-col>
                  <v-col>
                    <span :class="published_date_outdated ? 'error--text' : ''">
                      {{ getPublishedDate() }}
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
                  <v-col>
                    <tag-list
                      v-if="story.tags"
                      :tags="story.tags"
                      :truncate="openSummary"
                      :limit="openSummary ? 20 : 5"
                      :color="openSummary"
                    />
                  </v-col>
                </v-row>
                <v-row
                  v-if="openSummary && !published_date_outdated"
                  no-gutters
                  class="my-1"
                >
                  <v-col>
                    <week-chart :story="story" />
                  </v-col>
                </v-row>

                <metainfo
                  v-if="openSummary && news_item_length == 1"
                  :news-item="story.news_items[0]"
                />
              </v-container>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
    <v-row
      v-if="openSummary && news_item_length > 1"
      dense
      class="ma-0 py-0 px-5"
    >
      <v-col cols="11" offset="1">
        <transition-group
          name="news-items-grid"
          class="row d-flex row--dense"
          appear
        >
          <card-news-item
            v-for="item in story.news_items"
            :key="item.id"
            :news-item="item"
            class="mt-3"
          />
        </transition-group>
      </v-col>
    </v-row>
  </v-row>
</template>

<script>
import PopupDeleteItem from '@/components/popups/PopupDeleteItem.vue'
import PopupShareItems from '@/components/popups/PopupShareItems.vue'
import metainfo from '@/components/assess/card/metainfo.vue'
import votes from '@/components/assess/card/votes.vue'
import TagList from '@/components/assess/card/TagList.vue'
import SummarizedContent from '@/components/assess/card/SummarizedContent.vue'
import CardNewsItem from '@/components/assess/CardNewsItem.vue'
import WeekChart from '@/components/assess/card/WeekChart.vue'
import { notifySuccess } from '@/utils/helpers.js'

import { mapGetters } from 'vuex'
import {
  deleteNewsItemAggregate,
  importantNewsItemAggregate,
  readNewsItemAggregate
} from '@/api/assess'

export default {
  name: 'CardStory',
  components: {
    CardNewsItem,
    PopupDeleteItem,
    PopupShareItems,
    metainfo,
    votes,
    TagList,
    WeekChart,
    SummarizedContent
  },
  props: {
    story: {
      type: Object,
      required: true
    },
    selected: { type: Boolean, default: false },
    detailView: { type: Boolean, default: false }
  },
  emits: ['selectItem', 'deleteItem'],
  data: function () {
    return {
      viewDetails: false,
      openSummary: this.detailView,
      sharingDialog: false,
      deleteDialog: false,
      showDialog: false
    }
  },
  computed: {
    item_important() {
      return 'important' in this.story ? this.story.important : false
    },
    published_dates() {
      const pub_dates = this.story.news_items
        .map((item) => item.news_item_data.published)
        .sort()

      return [pub_dates[pub_dates.length - 1], pub_dates[0]]
    },

    story_in_report() {
      return this.story.in_reports_count > 0
    },
    news_item_length() {
      return this.story.news_items.length
    },
    news_item_summary_text() {
      return this.openSummary ? 'Close' : 'Open'
    },
    minButtonWidth() {
      const longestText = `${
        this.news_item_length > 1 ? '(' + this.news_item_length + ')' : ''
      }`
      return longestText.length + 11 + 'ch'
    },
    published_date_outdated() {
      const pub_date = new Date(this.published_dates[0])
      if (!pub_date) {
        return false
      }
      const oneWeekAgo = new Date()
      oneWeekAgo.setDate(oneWeekAgo.getDate() - 7)
      return oneWeekAgo > pub_date
    },
    story_in_reports() {
      return this.story ? this.story.in_reports_count : 0
    },
    is_summarized() {
      return this.story.summary !== undefined && this.story.summary !== ''
    }
  },
  methods: {
    ...mapGetters('users', ['getUsernameById']),

    notify(text) {
      notifySuccess(text)
    },

    toggleSelection() {
      this.$emit('selectItem', this.story.id)
    },
    markAsRead() {
      readNewsItemAggregate(this.story.id)
    },
    markAsImportant() {
      importantNewsItemAggregate(this.story.id)
    },
    deleteNewsItem() {
      deleteNewsItemAggregate(this.story.id)
      this.$emit('deleteItem', this.story.id)
    },
    addToReport() {
      this.sharingDialog = true
    },
    showRelated(event) {
      console.log('not yet implemented')
      console.debug(event)
    },
    updateDetailsView(value) {
      this.viewDetails = value
    },

    getDescription() {
      return this.openSummary
        ? this.news_item_length > 1
          ? this.story.description
          : this.story.news_items[0].news_item_data.content
        : this.story.summary || this.story.description
    },

    getPublishedDate() {
      const pubDateNew = new Date(this.published_dates[0])
      const pubDateNewStr = this.$d(pubDateNew, 'short')
      const pubDateOld = new Date(this.published_dates[1])
      const pubDateOldStr = this.$d(pubDateOld, 'short')
      if (pubDateNew && pubDateOld) {
        return pubDateNewStr === pubDateOldStr
          ? pubDateNewStr
          : `${pubDateOldStr} - ${pubDateNewStr}`
      }
      return ''
    },

    getCollectedDate() {
      const collected = this.story.created
      return collected ? new Date(collected) : new Date(this.story.created)
    },

    getAuthor() {
      return this.story.news_items[0].news_item_data.author
    },

    storyRestricted() {
      return false
    }
  }
}
</script>
