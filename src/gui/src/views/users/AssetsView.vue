<template>
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
            <v-icon
              v-on="on"
              color="secondary"
              @click.stop="createProduct(item)"
            >
              mdi-file
            </v-icon>
          </template>
          <span>Create Product</span>
        </v-tooltip>
      </template>
    </DataTable>
</template>

<script>
import DataTable from '@/components/common/DataTable'
import {
  // createAssetGroup,
  // updateAssetGroup,
  // deleteAssetGroup,
  // solveVulnerability,
  createAsset,
  updateAsset,
  deleteAsset
} from '@/api/assets'
import { mapActions, mapGetters } from 'vuex'
import { notifySuccess, notifyFailure } from '@/utils/helpers'

export default {
  name: 'Analyze',
  components: {
    DataTable
  },
  data: function () {
    return {
      selected: [],
      assets: [],
      asset_groups: []
    }
  },
  methods: {
    ...mapActions('assets', ['loadAssetGroups', 'loadAssets']),
    ...mapGetters('assets', ['getAssetGroups', 'getAssets']),
    ...mapActions(['updateItemCount']),
    updateData() {
      this.loadAssets().then(() => {
        const sources = this.getAssets()
        this.assets = sources
        this.updateItemCount({
          total: sources.length,
          filtered: sources.length
        })
      })
      this.loadAssetGroups().then(() => {
        this.asset_groups = this.getAssetGroups().items
      })
    },
    addItem() {
      this.$router.push('/asset/0')
    },
    editItem(item) {
      this.$router.push('/asset/' + item.id)
    },
    handleSubmit(submittedData) {
      console.log(submittedData)
    },
    deleteItem(item) {
      deleteAsset(item)
        .then(() => {
          notifySuccess(`Successfully deleted ${item.name}`)
          this.updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to delete ${item.name}`)
        })
    },
    createItem(item) {
      createAsset(item)
        .then(() => {
          notifySuccess(`Successfully created ${item.name}`)
          this.updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to create ${item.name}`)
        })
    },
    updateItem(item) {
      updateAsset(item)
        .then(() => {
          notifySuccess(`Successfully updated ${item.name}`)
          this.updateData()
        })
        .catch(() => {
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
