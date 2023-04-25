<template>
  <div>
    <v-tooltip v-for="(tag, i) in tags.slice(0, limit)" :key="i" bottom>
      <template #activator="{ props }">
        <v-btn
          v-ripple="false"
          v-bind="props"
          small
          variant="text"
          density="compact"
          height="auto"
          class="tag-button"
          :color="labelcolor(i)"
          :prepend-icon="tagIcon(tag.tag_type)"
          @click.stop="updateTags(tag.name)"
        >
          <span
            :style="truncate ? 'max-width: 100px' : ''"
            class="text-decoration-underline text-truncate"
          >
            {{ tag.name }}
          </span>
        </v-btn>
      </template>
    </v-tooltip>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import { tagIconFromType } from '@/utils/helpers'

export default {
  name: 'TagList',
  props: {
    tags: {
      type: Array,
      required: true
    },
    limit: {
      type: Number,
      default: 5
    },
    truncate: {
      type: Boolean,
      default: true
    },
    color: {
      type: Boolean,
      default: true
    }
  },
  data: () => ({
    colorStart: Math.floor(Math.random() * 9)
  }),
  methods: {
    ...mapActions('assess', ['updateNewsItems']),
    ...mapActions('filter', ['appendTag']),

    updateTags(tag) {
      this.appendTag(tag)
      this.updateNewsItems()
    },
    tagIcon(tag_type) {
      return tagIconFromType(tag_type)
    },

    labelcolor: function (i) {
      if (!this.color) {
        return undefined
      }

      const colorList = ['#2E3D7C', '#282528', '#BA292E', '#E15D3A']
      return colorList[(this.colorStart + i) % colorList.length]
    }
  }
}
</script>
