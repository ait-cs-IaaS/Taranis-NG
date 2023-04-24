<template>
  <v-dialog v-model="dialog" width="600">
    <template #activator="{ on: dialog }">
      <v-tooltip open-delay="1000" bottom :disabled="!tooltip">
        <template #activator="{ on: tooltip }">
          <v-btn
            icon
            tile
            class="item-action-btn"
            :class="[{ active: active ? active : false }, extraClass]"
            v-on="{ ...tooltip, ...dialog }"
          >
            <v-icon color="black">{{ icon }}</v-icon>
            <span v-if="buttonText">{{ buttonText }}</span>
          </v-btn>
        </template>
        <span>{{ tooltip }}</span>
      </v-tooltip>
    </template>
    <slot />
  </v-dialog>
</template>

<script>
export default {
  name: 'NewsItemActionDialog',
  props: {
    showDialog: { type: Boolean, default: false },
    active: Boolean,
    icon: { type: String, default: 'mdi-pencil' },
    extraClass: { type: String, default: '' },
    tooltip: { type: String, default: '' },
    buttonText: { type: String, default: '' }
  },
  emits: ['open', 'close'],
  data: () => ({}),
  computed: {
    dialog: {
      get() {
        return this.showDialog
      },
      set(value) {
        if (!value) {
          this.$emit('close')
        } else {
          this.$emit('open')
        }
      }
    }
  },
  methods: {}
}
</script>
