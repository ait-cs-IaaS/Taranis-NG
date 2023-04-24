<template>
  <v-list dense class="py-0">
    <v-list-item-group
      v-model="selected"
      active-class="selected"
      density="compact"
      mandatory
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
    </v-list-item-group>
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
  emits: ['input'],
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
        this.$emit('input', newValue)
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
