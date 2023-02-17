<template>
<div>
    <DataTable
      :addButton="true"
      :items.sync="report_items"
      :headerFilter="['tag', 'title', 'created']"
      sortByItem="id"
      :actionColumn="true"
      @delete-item="deleteItem"
      @edit-item="editItem"
      @add-item="addItem"
      @update-items="updateData"
      @selection-change="selectionChange"
    >
    <template v-slot:actionColumn>
      <v-tooltip left>
        <template v-slot:activator="{ on }">
          <v-icon v-on="on" color="secondary" @click.stop="createProduct(item)"> mdi-file </v-icon>
        </template>
        <span>Create Product</span>
      </v-tooltip>
    </template>
    </DataTable>
    <v-dialog
      v-model="dialog"
    >
      <v-card>
        <v-card-title class="text-h5">
          {{ $t('report_item.add_new') }}
        </v-card-title>

        <v-card-text>
          <v-row>
            <v-col cols="4" class="pr-3">
              {{ report_types }}
              <v-select
                v-model="report_item.report_item_type_id"
                item-text="title"
                item-value="id"
                :items="report_types"
                :label="$t('report_item.report_type')"
              />
            </v-col>
            <v-col cols="4" class="pr-3">
              <v-text-field
                :label="$t('report_item.title_prefix')"
                name="title_prefix"
                v-model="report_item.title_prefix"
              ></v-text-field>
            </v-col>
            <v-col cols="4" class="pr-3">
              <v-text-field
                :label="$t('report_item.title')"
                name="title"
                v-model="report_item.title"
              ></v-text-field>
            </v-col>
          </v-row>
        </v-card-text>

        <v-card-actions>
          <v-btn
            color="green darken-1"
            @click="dialog = false"
          >
            Create
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

</div>
</template>

<script>
import DataTable from '@/components/common/DataTable'
import { deleteReportItem, createReportItem, updateReportItem } from '@/api/analyze'
import { mapActions, mapGetters } from 'vuex'
import { notifySuccess, notifyFailure } from '@/utils/helpers'

export default {
  name: 'Analyze',
  components: {
    DataTable
  },
  data: () => ({
    report_items: [],
    report_types: {},
    report_item: {
      report_item_type_id: null,
      title_prefix: '',
      title: ''
    },
    dialog: false
  }),
  methods: {
    ...mapActions('analyze', ['loadReportItems']),
    ...mapGetters('analyze', ['getReportItems']),
    ...mapActions(['updateItemCount']),
    updateData() {
      this.loadReportItems().then(() => {
        const sources = this.getReportItems()
        console.debug(sources)
        this.report_items = sources
        this.updateItemCount({
          total: sources.length,
          filtered: sources.length
        })
      })
      this.loadReportTypes().then(() => {
        this.report_types = this.getReportTypes().items
      })
    },
    addItem() {
      this.dialog = true
    },
    editItem(item) {
      this.$router.push('/report/' + item.id)
    },
    handleSubmit(submittedData) {
      console.log(submittedData)
    },
    deleteItem(item) {
      if (!item.default) {
        deleteReportItem(item).then(() => {
          notifySuccess(`Successfully deleted ${item.name}`)
          this.updateData()
        }).catch(() => {
          notifyFailure(`Failed to delete ${item.name}`)
        })
      }
    },
    createItem(item) {
      createReportItem(item).then(() => {
        notifySuccess(`Successfully created ${item.name}`)
        this.updateData()
      }).catch(() => {
        notifyFailure(`Failed to create ${item.name}`)
      })
    },
    updateItem(item) {
      updateReportItem(item).then(() => {
        notifySuccess(`Successfully updated ${item.name}`)
        this.updateData()
      }).catch(() => {
        notifyFailure(`Failed to update ${item.name}`)
      })
    },
    createProduct() {
      this.$router.push({ name: 'product', params: { id: null } })
    },
    selectionChange(selected) {
      this.selected = selected.map((item) => item.id)
    }
  },
  mounted() {
    this.updateData()
  },
  beforeDestroy() {}
}
</script>
