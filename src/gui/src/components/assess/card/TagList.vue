<template>
  <div class="d-flex flex-row justify-start flex-wrap">
    <v-tooltip
      v-for="(tag, i) in tags.slice(0, limit)"
      :key="i"
      location="top"
      transition="fade-transition"
      offset="4"
    >
      <template #activator="{ props }">
        <a
          v-bind="props"
          small
          class="mr-1"
          :color="labelcolor(i)"
          @click.stop="updateTags(tag.name)"
        >
          <span class="tag-button"> {{ tag.name }}, </span>
        </a>
      </template>
      <span>
        <v-icon size="small" left class="ma-auto mr-2">{{
          tagIcon(tag.tag_type)
        }}</v-icon>
        <span class="text-caption">
          {{ tag.tag_type }}
        </span>
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
  computed: {
    getChipClass() {
      const c = 'mr-1 mb-1 story-label'
      return this.truncate ? c : c + '-no-trunc'
    },
    getTagClass() {
      return this.truncate ? 'text-truncate' : ''
    }
  },
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

<style lang="scss">
.tag-button {
  text-transform: capitalize;
  letter-spacing: normal;
  text-decoration: underline;
}
</style>
