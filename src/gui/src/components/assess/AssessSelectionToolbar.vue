<template>
  <v-bottom-navigation density="compact">
    <v-row no-gutters>
      <v-col v-if="storySelection.length > 0" class="story-bg toolbar">
        <div>
          <v-btn
            v-for="button in storyButtons"
            :key="button.label"
            :ripple="false"
            size="small"
            class="text-lowercase"
            @click.stop="actionClicked(button.action)"
          >
            <v-icon :icon="button.icon" />
            {{ button.label }}
          </v-btn>
        </div>
        <div class="mr-4">
          <v-btn size="small" class="text-lowercase" @click.stop="deselect">
            <v-icon icon="mdi-selection-remove" />
            deselect
          </v-btn>
          <span>
            Stories selected: <strong>{{ storySelection.length }}</strong>
          </span>
        </div>
      </v-col>
      <v-col v-if="newsItemSelection.length > 0" class="news-item-bg toolbar">
        <div>
          <v-btn
            v-for="button in newsItemButtons"
            :key="button.label"
            :ripple="false"
            size="small"
            class="text-lowercase"
            @click.stop="actionClicked(button.action)"
          >
            <v-icon :icon="button.icon" />
            {{ button.label }}
          </v-btn>
        </div>
        <div class="mr-4">
          <v-btn size="small" class="text-lowercase" @click.stop="deselect">
            <v-icon icon="mdi-selection-remove" />
            deselect
          </v-btn>
          <span>
            News Items selected: <strong>{{ newsItemSelection.length }}</strong>
          </span>
        </div>
      </v-col>
    </v-row>
    <v-dialog v-model="sharingDialog" width="auto">
      <popup-share-items :item-ids="selection" @close="sharingDialog = false" />
    </v-dialog>
  </v-bottom-navigation>
</template>

<script>
import { groupAction } from '@/api/assess'
import PopupShareItems from '@/components/popups/PopupShareItems.vue'
import { useAssessStore } from '@/stores/AssessStore'

import { notifySuccess, notifyFailure } from '@/utils/helpers'
import { storeToRefs } from 'pinia'
import { ref, computed } from 'vue'
import { unGroupAction } from '@/api/assess'

export default {
  name: 'AssessSelectionToolbar',
  components: {
    PopupShareItems
  },
  setup() {
    const assessStore = useAssessStore()
    const { storySelection, newsItemSelection } = storeToRefs(assessStore)
    const sharingDialog = ref(false)

    const storyButtons = computed(() => {
      const buttons = [
        {
          label: 'add to report',
          icon: 'mdi-google-circles-communities',
          action: 'addToReport'
        }
      ]

      if (storySelection.value.length > 1) {
        return [
          ...buttons,
          {
            label: 'merge',
            icon: 'mdi-merge',
            action: 'merge'
          }
        ]
      }
      return buttons
    })

    const newsItemButtons = computed(() => {
      const buttons = [
        {
          label: 'remove',
          icon: 'mdi-card-remove',
          action: 'remove'
        }
      ]
      return buttons
    })

    const actionClicked = (action) => {
      if (action === 'merge') {
        groupAction(storySelection.value)
          .then(() => {
            notifySuccess('Items merged')
            assessStore.clearSelection()
            assessStore.updateNewsItems()
          })
          .catch((err) => {
            notifyFailure('Failed to merge items')
            console.log(err)
          })
      } else if (action === 'addToReport') {
        sharingDialog.value = true
      } else if (action === 'remove') {
        unGroupAction(newsItemSelection.value)
      }
    }

    const deselect = () => {
      assessStore.clearSelection()
    }

    return {
      sharingDialog,
      storySelection,
      storyButtons,
      newsItemButtons,
      newsItemSelection,
      actionClicked,
      deselect
    }
  }
}
</script>

<style scoped>
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.story-bg {
  background-color: #7468e8;
}
.news-item-bg {
  background-color: #fc3c3c;
}
</style>
