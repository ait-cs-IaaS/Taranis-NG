<template>
  <v-list
    :selected="value"
    density="compact"
    class="py-0"
    color="primary"
    @click:select="updateSelected"
  >
    <v-list-item
      v-for="item in items"
      :key="item.type"
      class="extra-dense"
      :ripple="false"
      density="compact"
      :value="item.type"
      :prepend-icon="item.icon"
    >
      <v-list-item-title>
        {{ item.label }}
      </v-list-item-title>

      <template #append="{ isActive }">
        <v-list-item-action>
          <v-checkbox-btn
            :model-value="isActive"
            density="compact"
            false-icon=""
            true-icon="mdi-check-bold"
          />
        </v-list-item-action>
      </template>
    </v-list-item>
  </v-list>
</template>

<script>
export default {
  name: 'FilterSelectList',
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
  emits: ['update:modelValue'],
  methods: {
    updateSelected(data) {
      console.debug('FilterSortList updateSelected', data)
      this.$emit('update:modelValue', data.id)
    }
  }
}
</script>
