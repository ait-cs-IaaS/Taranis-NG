<template>
  <v-card-subtitle>
    <span>
      <v-icon :icon="tagIcon" />
      {{ tagText }}
    </span>
    <span class="ml-5"> Cluster size: {{ cluster.size }}</span>
    <v-divider class="mt-2 mb-2" />
  </v-card-subtitle>
  <v-card-text>
    {{ cluster }}
  </v-card-text>
</template>

<script>
import { ref, computed } from 'vue'
import { tagIconFromType, tagTextFromType } from '@/utils/helpers'

export default {
  name: 'TrendingCard',
  props: {
    cluster: { type: Object, required: true }
  },
  setup(props) {
    const tagType = ref(props.cluster.tag_type)

    const tagIcon = computed(() => {
      return tagIconFromType(tagType.value)
    })

    const tagText = computed(() => {
      return tagTextFromType(tagType.value)
    })

    return {
      tagType,
      tagIcon,
      tagText
    }
  }
}
</script>
