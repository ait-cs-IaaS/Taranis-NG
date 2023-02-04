<template>
  <v-autocomplete
    v-model="selected"
    :loading="loading"
    :items="tags"
    chips
    dense
    deletable-chips
    :search-input.sync="search"
    clearable
    flat
    no-data-text="No tags found"
    hide-details
    label="Tags"
    item-text="name"
    item-value="name"
    multiple
  >
  </v-autocomplete>
</template>

<script>
import { getTags } from '@/api/assess'

export default {
  name: 'tagFilter',
  emits: ['input'],
  data: () => ({
    selected: [],
    loading: false,
    tags: [],
    search: ''
  }),
  props: {},
  watch: {
    search(val) {
      val && val !== this.select && this.querySelections(val)
    }
  },
  methods: {
    querySelections(v) {
      this.loading = true
      getTags().then((res) => {
        this.tags = res.data
        this.loading = false
      })
    }
  },
  mounted() {
    this.querySelections()
  }
}
</script>
