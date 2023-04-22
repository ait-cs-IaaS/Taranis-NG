<template>
  <div class="item-action-btn btn-group">
    <v-btn v-ripple="false" small outlined @click.stop="upvote()">
      <span>{{ likes }}</span>
      <v-icon right color="awake-green-color"
        >mdi-arrow-up-circle-outline</v-icon
      >
    </v-btn>
    <v-btn v-ripple="false" small outlined @click.stop="downvote()">
      <span>{{ dislikes }}</span>
      <v-icon right color="awake-red-color"
        >mdi-arrow-down-circle-outline</v-icon
      >
    </v-btn>
  </div>
</template>

<script>
import { voteNewsItemAggregate } from '@/api/assess'

export default {
  name: 'StoryVotes',
  props: {
    story: {
      type: Object,
      required: true
    }
  },
  data: function () {
    return {
      likes: this.story.likes,
      dislikes: this.story.dislikes
    }
  },
  methods: {
    upvote() {
      this.likes += 1
      voteNewsItemAggregate(this.story.id, 1)
    },
    downvote() {
      this.dislikes += 1
      voteNewsItemAggregate(this.story.id, -1)
    }
  }
}
</script>
