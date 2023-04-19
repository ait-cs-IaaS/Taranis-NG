<template>
  <v-list dense class="py-0">
    <v-list-item-group
      active-class="selected"
      :value="value"
      @change="setValue"
      multiple
      class="filter-list"
    >
      <template>
        <v-list-item
          v-for="item in items"
          :key="item.type"
          class="extra-dense"
          :ripple="false"
          :value="item.type"
        >
          <template v-slot:prepend>
            <v-icon small color="grey" :icon="item.icon" />
          </template>

          <v-list-item-title class="py-1 mt-auto mb-auto">
            {{ item.label }}
          </v-list-item-title>

          <template v-slot:append="{ isActive }">
            <v-list-item-action>
              <v-icon
                v-if="isActive"
                small
                class="mt-auto mb-auto dark-grey--text"
              >
                mdi-check-bold
              </v-icon>
            </v-list-item-action>
          </template>
        </v-list-item>
      </template>
    </v-list-item-group>
  </v-list>
</template>

<script>
export default {
  name: 'filterSelectList',
  emits: ['input'],
  props: {
    value: {
      type: Array,
      default: () => []
    },
    items: {
      type: Array,
      default: () => []
    }
  },
  methods: {
    setValue(newValue) {
      this.$emit('input', newValue)
    }
  }
}
</script>
