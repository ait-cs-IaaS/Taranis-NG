<template>
  <div>
    <v-textarea
      v-if="attribute_item.type === 'TEXT'"
      v-model="input"
      :readonly="read_only"
      :label="attribute_item.title"
    ></v-textarea>
    <v-text-field
      v-if="attribute_item.type === 'STRING'"
      v-model="input"
      :readonly="read_only"
      :label="attribute_item.title"
    ></v-text-field>
    <v-checkbox
      v-if="attribute_item.type === 'BOOLEAN'"
      v-model="input"
      :readonly="read_only"
      :label="attribute_item.title"
    />
    <v-select
      v-if="attribute_item.type === 'ENUM'"
      v-model="input"
      :readonly="read_only"
      item-title="value"
      item-value="id"
      :items="attribute_item.attribute_enums"
      :label="attribute_item.title"
    />
    <v-radio-group
      v-if="attribute_item.type === 'RADIO'"
      v-model="input"
      :disabled="read_only"
      row
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
      v-model="input"
      :disabled="read_only"
      :editor-options="{
        height: 300
      }"
    />
    <v-radio-group
      v-if="attribute_item.type === 'TLP'"
      v-model="input"
      :disabled="read_only"
      row
      :label="attribute_item.title"
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
    <date-picker
      v-if="attribute_item.type === 'DATE'"
      v-model="input"
      :placeholder="attribute_item.title"
      :disabled="read_only"
    />
    <date-picker
      v-if="attribute_item.type === 'DATE_TIME'"
      v-model="input"
      :placeholder="attribute_item.title"
      type="datetime"
      :disabled="read_only"
    />
    <date-picker
      v-if="attribute_item.type === 'TIME'"
      v-model="input"
      :placeholder="attribute_item.title"
      type="time"
      :show-second="false"
      :disabled="read_only"
    />
    <v-autocomplete
      v-if="attribute_item.type === 'CPE' || attribute_item.type === 'CVE'"
      v-model="input"
      :readonly="read_only"
      :label="attribute_item.title"
      :items="attribute_item.attribute_enums"
    >
      <!-- TODO: Use MyAssets for Autocomplete -->
    </v-autocomplete>
    <AttributeCVSS v-if="attribute_item.type === 'CVSS'" v-model="input" />
  </div>
</template>

// ATTACHMENT: 'Attachment'

<script>
import AttributeCVSS from './AttributeCVSS.vue'

export default {
  name: 'AttributeItem',
  components: {
    AttributeCVSS
  },
  props: {
    value: {
      type: String,
      default: '',
      required: true
    },
    attribute_item: {
      type: Object,
      required: true
    },
    read_only: { type: Boolean, default: false }
  },
  emits: ['input'],
  computed: {
    input: {
      get() {
        return this.value
      },
      set(value) {
        this.$emit('input', value)
      }
    }
  }
}
</script>
