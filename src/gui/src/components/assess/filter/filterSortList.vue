<template>
  <v-list
    :selected="selected"
    density="compact"
    class="py-0"
    active-color="primary"
  >
    <v-list-item
      v-for="item in orderOptions"
      :key="item.title"
      density="compact"
      :ripple="false"
      :value="item.type + '_' + item.direction"
      :prepend-icon="item.icon"
      @click.capture="changeDirection($event, item)"
    >
      <v-list-item-title class="py-1 mt-auto mb-auto">
        {{ item.label }}
      </v-list-item-title>

      <template #append="{ isActive }">
        <v-list-item-action>
          <v-icon v-if="isActive" :icon="activeIcon(item)" />
        </v-list-item-action>
      </template>
    </v-list-item>
  </v-list>
</template>

<script>
export default {
  name: 'FilterSortList',
  props: {
    value: {
      type: Object,
      default: () => ({})
    },
    items: {
      type: Array,
      default: () => []
    }
  },
  emits: ['update:modelValue'],
  data: function () {
    return {
      orderOptions: this.items
    }
  },
  computed: {
    selected: {
      get() {
        return this.value
      },
      set(newValue) {
        this.$emit('update:modelValue', newValue)
      }
    }
  },
  methods: {
    activeIcon(item) {
      return item.direction === 'ASC' ? 'mdi-chevron-up' : 'mdi-chevron-down'
    },

    changeDirection(event, item) {
      event.preventDefault()
      this.orderOptions.forEach((option) => {
        if (option.type === item.type) {
          option.direction = option.direction === 'ASC' ? 'DESC' : 'ASC'
        }
      })
    }
  }
}
</script>
