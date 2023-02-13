<template>
  <v-card>
    <v-toolbar dark color="secondary">
      <v-toolbar-title>{{ story.title }}</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon :title="$t('assess.tooltip.delete_item')">
        <v-icon color="red">mdi-delete</v-icon>
      </v-btn>
    </v-toolbar>
    <v-row justify="center" class="px-4 py-4">
      <v-row justify="center" class="subtitle-2 info--text pt-4 ma-0">
        <v-flex>
          <v-row class="text-center">
            <v-col>
              <span class="overline font-weight-bold">
                {{ $t('assess.created') }}
              </span>
              <br />
              <span class="caption">
                {{ $d(new Date(story.created), 'long') }}
              </span>
            </v-col>
            <v-col>
              <span class="overline font-weight-bold"> NewsItem ID </span>
              <br />
              <span class="caption">
                {{ story.id }}
              </span>
            </v-col>
          </v-row>
        </v-flex>
      </v-row>
      <hr style="width: calc(100%); border: 0px" />
      <v-row class="headline">
        <span class="display-1 font-weight-light py-4">
          {{ story.title }}
        </span>
      </v-row>
      <v-row class="py-4">
        <span>{{ getDescription }}</span>
      </v-row>
    </v-row>
  </v-card>
</template>

<script>
export default {
  name: 'StoryDetail',
  components: {},
  emits: ['view'],
  props: {
    story: {}
  },
  data: () => ({}),
  computed: {
    getDescription() {
      return this.story.summary || this.story.description
    }
  },
  mounted() {
    console.log(this.story)
  },
  methods: {}
}
</script>
