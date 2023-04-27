<template>
  <div>
    <v-container fluid class="flex-column">
      <transition name="empty-list-transition" mode="out-in">
        <v-row v-if="!items">
          <v-col cols="12" class="empty-list-notification">
            <v-icon x-large> mdi-circle-off-outline </v-icon>
            <span v-if="items.total_count">
              The currently selected filters do not yield any results. Try
              changing the filters.
            </span>
            <span v-else> No elements to display. </span>
          </v-col>
        </v-row>

        <!-- class="row d-flex align-stretch row--dense stories-grid-container" -->
        <transition-group
          v-else
          name="news-items-grid"
          tag="div"
          class="row d-flex align-stretch row--dense flex-column"
          appear
        >
          <card-story
            v-for="newsItem in items"
            :key="newsItem.id"
            :story="newsItem"
            :selected="getNewsItemsSelection().includes(newsItem.id)"
            @delete-item="removeAndDeleteNewsItem(newsItem.id)"
            @select-item="selectNewsItem(newsItem.id)"
          ></card-story>
        </transition-group>
      </transition>
    </v-container>

    <!-- TODO: Loader not working -->
    <div class="text-subtitle-1 text-center dark-grey--text mt-3">
      <div v-if="moreToLoad">
        <v-btn @click="loadNext">Next Page</v-btn>
      </div>
      <div v-else>
        <v-icon left color="primary">mdi-checkbox-marked-circle-outline</v-icon>
        All items loaded.
      </div>
    </div>

    <v-expand-transition>
      <assess-selection-toolbar
        v-if="activeSelection"
        :selection="newsItemsSelection"
      ></assess-selection-toolbar>
    </v-expand-transition>
  </div>
</template>

<script>
import KeyboardMixin from '../../assets/keyboard_mixin'
import CardStory from '@/components/assess/CardStory'
import AssessSelectionToolbar from '@/components/assess/AssessSelectionToolbar'
import { mapActions, mapState, storeToRefs, mapWritableState } from 'pinia'
import { useAssessStore } from '@/stores/AssessStore'
import { watch } from 'vue'
import { useFilterStore } from '@/stores/FilterStore'

export default {
  name: 'AssessView',
  components: {
    CardStory,
    AssessSelectionToolbar
  },
  mixins: [KeyboardMixin('assess')],
  data: () => ({
    reloading: false,
    items: []
  }),
  computed: {
    ...mapState(useAssessStore, ['newsItems', 'newsItemsSelection']),
    ...mapState(useFilterStore, ['newsItemsFilter']),
    moreToLoad() {
      const offset = this.newsItemsFilter.offset
        ? parseInt(this.newsItemsFilter.offset)
        : 0
      const length = offset + this.items.length
      return length < this.newsItems.total_count
    },

    activeSelection() {
      return this.newsItemsSelection.length > 0
    }
  },

  created() {
    this.updateOSINTSourceGroupsList()
    this.updateOSINTSources()
    this.updateNewsItems()

    const assessstore = useAssessStore()
    const { newsItems } = storeToRefs(assessstore)

    watch(newsItems, () => {
      this.getNewsItemsFromStore()
    })
  },
  methods: {
    ...mapWritableState(useMainStore, ['itemCountTotal', 'itemCountFiltered']),
    ...mapActions(useAssessStore, [
      'updateNewsItems',
      'updateOSINTSourceGroupsList',
      'updateOSINTSources',
      'selectNewsItem'
    ]),
    ...mapActions(useFilterStore, ['nextPage']),
    removeAndDeleteNewsItem(id) {
      this.items = this.items.filter((x) => x.id !== id)
    },

    loadNext() {
      this.nextPage()
      this.updateNewsItems()
    },

    // TODO: Call API via Store
    // + pass filter parameter for presorting
    getNewsItemsFromStore() {
      this.items = this.newsItems.items
      this.itemCountTotal = this.newsItems.total_count
      this.itemCountFiltered = this.items.length
      console.debug('number of newsitems: ' + this.newsItems.total_count)
    }
  }
}
</script>
