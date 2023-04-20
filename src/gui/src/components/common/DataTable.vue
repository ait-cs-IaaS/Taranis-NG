<template>
  <v-container fluid class="ma-5 mt-5 pa-5 pt-0">
    <slot name="header"></slot>
    <v-data-table
      :headers="headers"
      :items="items"
      :search="search"
      :sort-by="[{ key: sortByItem }]"
      class="elevation-1"
      show-select
      :custom-filter="customFilter"
      @click:row="rowClick"
      @update:modelValue="emitFilterChange"
    >
      <template v-slot:top>
        <v-card>
          <v-card-title>
            <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="Search"
              single-line
              class="mr-8"
              hide-details
            ></v-text-field>
            <v-btn
              color="error"
              dark
              class="ml-8"
              @click="deleteItems(selected)"
              v-if="selected.length > 0"
            >
              Delete {{ selected.length }}
            </v-btn>
            <v-btn
              color="primary"
              dark
              class="ml-8"
              @click="addItem"
              v-if="addButton"
            >
              New Item
            </v-btn>
            <slot name="titlebar"></slot>
          </v-card-title>
        </v-card>
      </template>
      <template v-slot:item.default="{ item }">
        <v-chip :color="getDefaultColor(item.default)" dark>
          {{ item.default }}
        </v-chip>
      </template>

      <template v-slot:item.tag="{ item }">
        <v-icon small class="mr-1" :icon="item.raw.tag" />
      </template>

      <template v-slot:item.actions="{ item }">
        <div class="d-inline-flex">
          <slot name="actionColumn"></slot>
          <v-tooltip left>
            <template v-slot:activator="{ props }">
              <v-icon v-bind="props" color="red" @click.stop="deleteItem(item)">
                mdi-delete
              </v-icon>
            </template>
            <span>Delete</span>
          </v-tooltip>
        </div>
      </template>
      <template v-slot:bottom v-if="items.length < 10" />
      <template v-slot:no-data>
        <v-btn color="primary" @click.stop="updateItems()">
          <v-icon class="mr-1">mdi-refresh</v-icon>
          Refresh
        </v-btn>
      </template>
    </v-data-table>
  </v-container>
</template>

<script>
import { mapActions } from 'vuex'
import { defineComponent, toRaw } from 'vue'

export default defineComponent({
  name: 'DataTable',
  components: {},
  emits: ['delete-item', 'edit-item', 'add-item', 'selection-change'],
  props: {
    items: {
      type: Array,
      required: true
    },
    addButton: {
      type: Boolean,
      default: false
    },
    sortByItem: {
      type: String,
      default: null
    },
    headerFilter: {
      type: Array
    },
    actionColumn: {
      type: Boolean,
      default: false
    }
  },
  data: () => ({
    search: '',
    selected: []
  }),
  computed: {
    headers() {
      const actionHeader = {
        title: 'Actions',
        key: 'actions',
        sortable: false,
        width: '30px'
      }
      let headers = []
      if (this.headerFilter.length > 0) {
        if (typeof this.headerFilter[0] !== 'object') {
          headers = this.headerFilter.map((key) => this.headerTransform(key))
        } else {
          headers = this.headerFilter
        }
      } else if (this.items.length > 0) {
        headers = Object.keys(this.items[0]).map((key) =>
          this.headerTransform(key)
        )
      }
      if (this.actionColumn) {
        headers.push(actionHeader)
      }
      return headers
    }
  },
  methods: {
    ...mapActions(['updateItemCountFiltered']),

    headerTransform(key) {
      if (key === 'tag') {
        return {
          title: key,
          key: key,
          sortable: false,
          width: '15px'
        }
      }
      return { title: key, key: key }
    },
    emitFilterChange(selected) {
      this.selected = selected
      this.$emit('selection-change', selected)
      this.updateItemCountFiltered(selected.length)
    },
    customFilter(value, query) {
      return (
        value != null &&
        query != null &&
        typeof value === 'string' &&
        value.toString().indexOf(query) !== -1
      )
    },

    rowClick(event, value) {
      const item = toRaw(value.item.raw)
      this.$emit('edit-item', item)
    },
    addItem() {
      this.$emit('add-item')
    },
    getDefaultColor(defaultgroup) {
      return defaultgroup ? 'green' : ''
    },
    deleteItem(item) {
      this.$emit('delete-item', item)
    },
    deleteItems(items) {
      items.forEach((item) => this.deleteItem(item))
    },
    updateItems() {
      this.$emit('update-items')
    }
  }
})
</script>
