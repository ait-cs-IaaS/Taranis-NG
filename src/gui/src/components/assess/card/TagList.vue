<template>
  <div class="ml-0 pl-0">
    <v-tooltip v-for="(tag, i) in tags.slice(0, limit)" :key="i" bottom>
      <template #activator="{ props }">
        <a v-bind="props" class="mr-2" @click.stop="updateTags(tag.name)">
          <v-icon start size="small" :icon="tagIcon(tag.tag_type)" />
          <span
            :style="truncate ? 'max-width: 80px' : 'max-width: 120px'"
            :class="
              'd-inline-block text-decoration-underline text-truncate ' +
              labelcolor(i)
            "
          >
            {{ tag.name }}
          </span>
        </a>
      </template>
      <span>
        <v-icon start :icon="tagIcon(tag.tag_type)" />
        {{ tag.name }}
      </span>
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
        return ''
      }

      const colorList = ['text-red', 'text-blue', 'text-green', 'text-black']
      return colorList[(this.colorStart + i) % colorList.length]
    }
  }
}
</script>
