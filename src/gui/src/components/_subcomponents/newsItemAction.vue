<template>
  <v-tooltip open-delay="1000" bottom :disabled="!tooltip">
    <template #activator="{ props }">
      <v-btn
        v-bind="props"
        icon
        tile
        class="news-item-action"
        :class="[{ active: active ? active : false }, extraClass]"
        @click.capture="execute($event)"
      >
        <v-icon color="black">{{ icon }}</v-icon>
        {{ buttonText }}
      </v-btn>
    </template>
    <span>{{ tooltip }}</span>
  </v-tooltip>
</template>

<script>
export default {
  name: 'NewsItemAction',
  props: {
    active: Boolean,
    icon: { type: String, default: 'mdi-pencil' },
    extraClass: { type: String, default: '' },
    tooltip: { type: String, default: '' },
    buttonText: { type: String, default: '' }
  },
  emits: ['click'],
  methods: {
    execute(event) {
      event.stopPropagation()
      this.$emit('click', event)
    }
  }
}
</script>
