<template>
  <v-autocomplete
    v-model="selected"
    v-model:search="search"
    :loading="loading"
    :items="available_tags"
    chips
    density="compact"
    deletable-chips
    clearable
    no-data-text="No tags found"
    item-value="name"
    item-title="name"
    label="Tags"
    multiple
  >
    <template #item="{ props, item }">
      <v-list-item
        v-bind="props"
        :prepend-icon="tagIcon(item.raw.tag_type)"
        :text="shortText(item.raw.name)"
      />
    </template>
    <template #chip="{ props, item }">
      <v-chip
        :prepend-icon="tagIcon(item.raw.tag_type)"
        v-bind="props"
        :text="shortText(item.raw.name)"
      />
    </template>
  </v-autocomplete>
</template>

<script>
import { getTags } from '@/api/assess'
import { mapActions, mapGetters } from 'vuex'
import { tagIconFromType } from '@/utils/helpers'

export default {
  name: 'TagFilter',
  props: {},
  data: () => ({
    loading: false,
    available_tags: [],
    selected_tags: [],
    search: ''
  }),
  computed: {
    selected: {
      get() {
        return this.selected_tags
      },
      set(val) {
        this.setTags(val)
        this.updateNewsItems()
      }
    }
  },
  watch: {
    search(val) {
      val && this.querySelections({ search: val })
    }
  },
  async mounted() {
    this.selected_tags = this.loadFilterTags()
    await this.querySelections()
  },
  methods: {
    ...mapGetters('filter', ['getFilterTags']),
    ...mapActions('filter', ['setTags']),
    ...mapActions('assess', ['updateNewsItems']),
    shortText(item) {
      console.debug('shortText', item)
      return item.length > 15 ? item.substring(0, 15) + '...' : item
    },
    tagIcon(tag_type) {
      return tagIconFromType(tag_type)
    },
    async querySelections(filter) {
      this.loading = true
      await getTags(filter).then((res) => {
        this.available_tags = res.data
        this.selected_tags.forEach((tag) => {
          if (!this.available_tags.includes(tag)) {
            this.available_tags.unshift(tag)
          }
        })
        this.loading = false
      })
    },
    loadFilterTags() {
      const tags = this.getFilterTags()
      if (!tags) {
        return []
      }
      return tags.map((tag) => {
        return { name: tag }
      })
    }
  }
}
</script>
