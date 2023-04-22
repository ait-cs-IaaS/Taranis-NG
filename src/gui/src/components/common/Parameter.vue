<template>
  <div>
    <!-- TODO: i18 :label-->
    <v-text-field
      v-model="value"
      v-validate="'required'"
      :label="parameter.name"
      name="value"
      type="text"
      data-vv-name="value"
      :error-messages="errors.collect('value')"
    ></v-text-field>
  </div>
</template>

<script>
export default {
  name: 'ParameterView',
  props: ['parameter'],
  data: () => ({
    value: ''
  })
}
</script>
