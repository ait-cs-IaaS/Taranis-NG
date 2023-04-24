<template>
  <v-btn-toggle
    v-model="modelValue"
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
    value: {
      type: String,
      default: 'all'
    }
  },
  emits: ['update:modelValue'],
  computed: {
    modelValue: {
      get() {
        return this.value
      },
      set(newValue) {
        this.setValue(newValue)
      }
    }
  },
  methods: {
    setValue(newValue) {
      console.debug('dateChips.setValue', newValue)
      this.$emit('update:modelValue', newValue)
    }
  }
}
</script>
