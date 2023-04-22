<template>
  <p :class="news_item_summary_class">
    <v-tooltip v-if="is_summarized" top>
      <template #activator="{ on, attrs }">
        <v-icon v-bind="attrs" v-on="on">mdi-text-short</v-icon>
      </template>
      <span>This text is Summarized</span>
    </v-tooltip>
    {{ content }}
  </p>
</template>

<script>
export default {
  name: 'TagList',
  props: {
    content: {
      type: String,
      default: ''
    },
    is_summarized: {
      type: Boolean,
      default: false
    },
    open: {
      type: Boolean,
      default: false
    }
  },
  data: () => ({
    colorStart: Math.floor(Math.random() * 9)
  }),
  computed: {
    news_item_summary_class() {
      return this.open ? 'news-item-summary-no-clip' : 'news-item-summary'
    }
  },
  methods: {}
}
</script>
