<template>
  <div>
    <v-container fluid style="min-height: 40vh">
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

        <transition-group
          name="news-items-grid"
          tag="div"
          class="row d-flex align-stretch row--dense stories-grid-container"
          v-else
          appear
        >
          <card-story
            v-for="newsItem in items"
            :key="newsItem.id"
            :story="newsItem"
            :selected="newsItemsSelection.includes(newsItem.id)"
            @deleteItem="removeAndDeleteNewsItem(newsItem.id)"
            @selectItem="selectNewsItem(newsItem.id)"
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
        class="px-1 pt-2 pb-3"
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
import { mapActions as mapActionsVuex, mapState as mapStateVuex } from 'vuex'
import { mapActions, mapState, storeToRefs } from 'pinia'
import { assessStore } from '@/stores/AssessStore'
import { watch } from 'vue'

export default {
  name: 'Assess',
  mixins: [KeyboardMixin('assess')],
  components: {
    CardStory,
    AssessSelectionToolbar
  },
  data: () => ({
    reloading: false,
    items: []
  }),
  methods: {
    ...mapActionsVuex(['updateItemCountTotal', 'updateItemCountFiltered']),
    ...mapActions(assessStore, [
      'updateNewsItems',
      'updateOSINTSourceGroupsList',
      'updateOSINTSources',
      'selectNewsItem'
    ]),
    ...mapActionsVuex('filter', ['resetNewsItemsFilter', 'nextPage']),

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
      this.updateItemCountTotal(this.newsItems.total_count)
      this.updateItemCountFiltered(this.items.length)
      console.debug('number of newsitems: ' + this.newsItems.total_count)
    }
  },
  computed: {
    ...mapState(assessStore, ['newsItems', 'newsItemsSelection']),
    ...mapStateVuex('filter', {
      scope: (state) => state.newsItemsFilter.scope,
      filter: (state) => state.newsItemsFilter
    }),

    moreToLoad() {
      const offset = this.filter.offset ? parseInt(this.filter.offset) : 0
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

    const assessstore = assessStore()
    const { newsItems } = storeToRefs(assessstore)

    watch(newsItems, () => {
      this.getNewsItemsFromStore()
    })
  }
}
</script>
