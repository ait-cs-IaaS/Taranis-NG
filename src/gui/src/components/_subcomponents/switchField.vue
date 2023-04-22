<template>
  <div>
    <v-switch
      v-model="localValue"
      :label="label ? label : ''"
      :color="color ? color : 'success'"
      inset
      dense
      hide-details
      @change="setValue"
    ></v-switch>
  </div>
</template>

<script>
export default {
  name: 'SwitchField',
  props: {
    label: String,
    color: String,
    value: Boolean
  },
  emits: ['input'],
  data: () => ({
    localValue: false
  }),
  mounted() {
    this.localValue = this.value
  },
  methods: {
    setValue() {
      this.$emit('input', this.localValue)
    }
  }
}
</script>
