<template>
  <v-tooltip open-delay="1000" bottom :disabled="!tooltip">
    <template v-slot:activator="{ props }">
      <v-btn
        v-bind="props"
        icon
        tile
        class="news-item-action"
        :class="[{ active: active ? active : false }, extraClass]"
        @click.native.capture="execute($event)"
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
  name: 'newsItemAction',
  props: {
    active: Boolean,
    icon: String,
    extraClass: String,
    tooltip: String,
    buttonText: { type: String, default: '' }
  },
  methods: {
    execute (event) {
      event.stopPropagation()
      this.$emit('click', event)
    }
  }
}
</script>
