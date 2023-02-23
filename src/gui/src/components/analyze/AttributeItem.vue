<template>
  <div>
  <v-textarea
    v-if="attribute_item.attribute_name === 'Text'"
    :readonly="read_only"
    v-model="input"
    :label="attribute_item.title"
  ></v-textarea>
  <v-text-field
    v-if="attribute_item.attribute_name === 'String'"
    :readonly="read_only"
    v-model="input"
    :label="attribute_item.title"
  ></v-text-field>
  <v-checkbox
    v-if="attribute_item.attribute_name === 'Boolean'"
    :readonly="read_only"
    v-model="input"
    :label="attribute_item.title"
  />

  </div>
</template>

<script>
export default {
  name: 'AttributeItem',
  components: {},
  props: {
    value: {
      type: String,
      default: '',
      required: true
    },
    attribute_item: {
      type: Object,
      default: () => {},
      required: true
    },
    read_only: { type: Boolean, default: false }
  },
  computed: {
    input: {
      get() {
        return this.value
      },
      set(value) {
        this.$emit('input', value)
      }
    }
  },
  methods: {},
  mounted() {
    console.debug('Mounted AttributeItem')
    console.debug(this.attribute_item)
  }
}
</script>
