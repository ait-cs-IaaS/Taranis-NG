<template>
  <v-container fluid class="ma-5 mt-5 pa-5 pt-0">
    <v-form
      @submit.prevent="handleSubmit"
      id="edit_config_form"
      ref="config_form"
      class="px-4"
    >
      <v-row no-gutters v-for="(item, i) in formData" :key="i">
        <v-text-field
          v-model="formData[i]"
          :label="i"
          required
          :disabled="i === 'id'"
          :type="typeof item === 'number' ? 'number' : 'text'"
          v-if="typeof item === 'number' || typeof item === 'string'"
        ></v-text-field>
        <div v-if="typeof item === 'object'">
          <div v-for="(subitem, j) in item" :key="j">
            <v-text-field
              v-model="item[j]"
              :label="j"
              required
              :disabled="j === 'id'"
              :type="typeof subitem === 'number' ? 'number' : 'text'"
              v-if="typeof subitem === 'number' || typeof subitem === 'string'"
            ></v-text-field>
          </div>
        </div>
      </v-row>
      <v-row no-gutters>
        <v-btn type="submit" color="success" class="mr-4"> Submit </v-btn>
      </v-row>
    </v-form>
  </v-container>
</template>

<script>
export default {
  name: 'EditConfig',
  emits: ['submit'],
  props: {
    configData: {
      type: Object,
      required: true
    }
  },
  computed: {
    formData() {
      return this.configData
    }
  },
  methods: {
    handleSubmit() {
      if (!this.$refs.config_form.validate()) {
        return
      }
      this.$emit('submit', this.formData)
    }
  }
}
</script>
