<template>
  <v-container fluid class="ma-5 mt-5 pa-5 pt-0">
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
          color="primary"
          dark
          class="ml-8"
          @click="addItem"
          v-if="addButton"
        >
          New Item
        </v-btn>
      </v-card-title>
      <v-data-table
        ref="configTable"
        :headers="headers"
        :items="items"
        :search="search"
        :group-by="groupByItem"
        :sort-by="sortByItem"
        class="elevation-1"
        hide-default-footer
        @click:row="rowClick"
      >
        <template v-slot:[`group.header`]="{ items }">
          <th :colspan="headers.length" class="text-left">
            {{ items[0].collector_type }}
          </th>
        </template>

        <template v-slot:[`header.tag`]="{}"></template>
        <template v-slot:[`header.actions`]="{}"></template>

        <template v-slot:[`item.default`]="{ item }">
          <v-chip :color="getDefaultColor(item.default)" dark>
            {{ item.default }}
          </v-chip>
        </template>

        <template v-slot:[`item.tag`]="{ item }">
          <v-icon small class="mr-2">
            {{ item.tag }}
          </v-icon>
        </template>
        <template v-slot:[`item.actions`]="{ item }">
          <v-icon small class="mr-2" @click.stop="rowClick(item)">
            mdi-pencil
          </v-icon>
          <v-icon small @click.stop="deleteItem(item)"> mdi-delete </v-icon>
        </template>
        <template v-slot:no-data>
          <v-btn color="primary">Reset</v-btn>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: 'ConfigTable',
  components: {},
  emits: ['delete-item', 'edit-item', 'add-item'],
  props: {
    items: {
      type: Array,
      required: true
    },
    addButton: {
      type: Boolean,
      default: false
    },
    groupByItem: {
      type: String,
      default: null
    },
    sortByItem: {
      type: String,
      default: null
    },
    headerFilter: {
      type: Array,
      default: () => []
    },
    actionColumn: {
      type: Boolean,
      default: false
    }
  },
  data: () => ({
    search: ''
  }),
  computed: {
    headers() {
      var actionHeader = {
        text: 'Actions',
        value: 'actions',
        sortable: false,
        width: '15px'
      }
      var headers = []
      if (this.headerFilter.length > 0) {
        headers = this.headerFilter.map((key) => this.headerTransform(key))
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
    headerTransform(key) {
      if (key === 'tag') {
        return {
          text: key,
          value: key,
          sortable: false,
          width: '15px'
        }
      }
      return { text: key, value: key }
    },
    rowClick(item) {
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
    }
  }
}
</script>
