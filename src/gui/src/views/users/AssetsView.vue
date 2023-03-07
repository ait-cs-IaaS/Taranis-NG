<template>
  <container>
    <DataTable
      :addButton="true"
      :items.sync="assets"
      :headerFilter="headers"
      sortByItem="id"
      groupByItem="asset_group"
      :actionColumn="true"
      @delete-item="deleteAsset"
      @edit-item="editAsset"
      @add-item="addAsset"
      @update-items="updateData"
      @selection-change="selectionChange"
    >
      <template v-slot:header>
        <h1>Assets</h1>
      </template>
      <template v-slot:[`item.name`]="{ item }">
        <v-chip
          color="red"
          dark
        >
          {{ item }}
        </v-chip>
      </template>
    </DataTable>
    <DataTable
      :addButton="true"
      :items.sync="asset_groups"
      :headerFilter="['tag', 'name', 'description']"
      sortByItem="id"
      :actionColumn="true"
      @delete-item="deleteAssetGroup"
      @edit-item="editAssetGroup"
      @add-item="addAssetGroup"
      @update-items="updateData"
      @selection-change="selectionChange"
    >
      <template v-slot:header>
        <h1>Asset Groups</h1>
      </template>
      <template v-slot:[`item.name`]="{ item }">
        <v-chip
          color="red"
          dark
        >
          {{ item }}
        </v-chip>
      </template>
    </DataTable>
  </container>
</template>

<script>
import DataTable from '@/components/common/DataTable'
import {
  deleteAssetGroup,
  // solveVulnerability,
  deleteAsset
} from '@/api/assets'
import { mapActions, mapGetters } from 'vuex'
import { notifySuccess, notifyFailure } from '@/utils/helpers'

export default {
  name: 'Assets',
  components: {
    DataTable
  },
  data: function () {
    return {
      selected: [],
      assets: [],
      asset_groups: [],
      headers: [
        { text: 'tag', value: 'tag', sortable: false, width: '15px' },
        { text: 'name', value: 'name' },
        { text: 'description', value: 'description' }
      ]
    }
  },
  methods: {
    ...mapActions('assets', ['loadAssetGroups', 'loadAssets']),
    ...mapGetters('assets', ['getAssetGroups', 'getAssets']),
    ...mapActions(['updateItemCount']),
    updateData() {
      this.loadAssets().then(() => {
        const sources = this.getAssets()
        this.assets = sources.items
        this.updateItemCount({
          total: sources.total_count,
          filtered: sources.length
        })
      })
      this.loadAssetGroups().then(() => {
        this.asset_groups = this.getAssetGroups().items
      })
    },
    addAsset() {
      this.$router.push('/asset/0')
    },
    editAsset(item) {
      this.$router.push('/asset/' + item.id)
    },
    addAssetGroup() {
      this.$router.push('/asset-group/0')
    },
    editAssetGroup(item) {
      this.$router.push('/asset-group/' + item.id)
    },
    deleteAsset(item) {
      deleteAsset(item)
        .then(() => {
          notifySuccess(`Successfully deleted ${item.name}`)
          this.updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to delete ${item.name}`)
        })
    },
    deleteAssetGroup(item) {
      deleteAssetGroup(item)
        .then(() => {
          notifySuccess(`Successfully deleted ${item.name}`)
          this.updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to delete ${item.name}`)
        })
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
