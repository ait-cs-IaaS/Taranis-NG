<template>
  <v-btn-toggle
    v-model="selected"
    variant="outlined"
    density="compact"
    divided
    selected-class="text-primary"
  >
    <v-btn variant="text" value="all">all</v-btn>
    <v-btn variant="text" value="today">today</v-btn>
    <v-btn variant="text" value="week">one week</v-btn>
  </v-btn-toggle>
</template>

<script>
export default {
  name: 'DateChips',
  props: {
    modelValue: {
      type: String,
      default: 'all'
    }
  },
  emits: ['update:modelValue'],
  computed: {
    selected: {
      get() {
        return this.modelValue
      },
      set(val) {
        console.debug('dateChips.setValue', val)
        this.$emit('update:modelValue', val)
      }
    }
  }
}
</script>
