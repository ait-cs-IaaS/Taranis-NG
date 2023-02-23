<template>
  <div>
    <v-textarea
      v-if="attribute_item.type === 'TEXT'"
      :readonly="read_only"
      v-model="input"
      :label="attribute_item.title"
    ></v-textarea>
    <v-text-field
      v-if="attribute_item.type === 'STRING'"
      :readonly="read_only"
      v-model="input"
      :label="attribute_item.title"
    ></v-text-field>
    <v-checkbox
      v-if="attribute_item.type === 'BOOLEAN'"
      :readonly="read_only"
      v-model="input"
      :label="attribute_item.title"
    />
    <v-select
      v-if="attribute_item.type === 'ENUM'"
      :readonly="read_only"
      v-model="input"
      item-text="value"
      item-value="id"
      :items="attribute_item.attribute_enums"
      :label="attribute_item.title"
    />
    <v-radio-group
      v-if="attribute_item.type === 'RADIO'"
      :disabled="read_only"
      row
      v-model="input"
    >
      <v-radio
        v-for="attr_enum in attribute_item.attribute_enums"
        :key="attr_enum.id"
        :label="attr_enum.value"
        :value="attr_enum.value"
      ></v-radio>
    </v-radio-group>
    <vue-editor
      v-if="attribute_item.type === 'RICH_TEXT'"
      :disabled="read_only"
      v-model="input"
      :editorOptions="{
        height: 300
      }"
    />
    <v-radio-group
      v-if="attribute_item.type === 'TLP'"
      :disabled="read_only"
      row
      v-model="input"
    >
      <v-radio
        :label="$t('attribute.tlp_white')"
        color="gray"
        value="WHITE"
      ></v-radio>
      <v-radio
        :label="$t('attribute.tlp_green')"
        color="green"
        value="GREEN"
      ></v-radio>
      <v-radio
        :label="$t('attribute.tlp_amber')"
        color="orange"
        value="AMBER"
      ></v-radio>
      <v-radio
        :label="$t('attribute.tlp_red')"
        color="red"
        value="RED"
      ></v-radio>
    </v-radio-group>
  </div>
</template>

// ATTACHMENT: 'Attachment', // DATE: 'Date', // CPE: 'CPE', // CVE: 'CVE', //
TIME: 'Time', // DATE_TIME: 'DateTime', // CVSS: 'CVSS'

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
