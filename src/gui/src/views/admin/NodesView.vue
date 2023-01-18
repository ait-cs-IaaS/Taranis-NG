<template>
  <div>
    <ConfigTable
      :addButton="true"
      :items.sync="nodes"
      :headerFilter="['tag', 'name', 'title', 'description']"
      sortByItem="id"
      :actionColumn=true
      @delete-item="deleteItem"
      @edit-item="editItem"
      @add-item="addItem"
    />
    <EditConfig
      v-if="formData && Object.keys(formData).length > 0"
      :configData="formData"
      @submit="handleSubmit"
    ></EditConfig>
  </div>
</template>

<script>
import ConfigTable from '../../components/config/ConfigTable'
import EditConfig from '../../components/config/EditConfig'
import { deleteNode, createNode, updateNode } from '@/api/config'
import { mapActions, mapGetters } from 'vuex'
import { notifySuccess, notifyFailure, emptyValues } from '@/utils/helpers'

export default {
  name: 'Nodes',
  components: {
    ConfigTable,
    EditConfig
  },
  data: () => ({
    nodes: [],
    formData: {},
    edit: false
  }),
  methods: {
    ...mapActions('config', ['loadNodes']),
    ...mapActions(['updateItemCount']),
    ...mapGetters('config', ['getNodes']),
    ...mapActions(['updateItemCount']),
    updateData() {
      this.loadNodes().then(() => {
        const sources = this.getNodes()
        this.nodes = sources.items
        this.updateItemCount({ total: sources.total_count, filtered: sources.length })
      })
    },
    addItem() {
      this.formData = emptyValues(this.nodes[0])
      this.edit = false
    },
    editItem(item) {
      this.formData = item
      this.edit = true
    },
    handleSubmit(submittedData) {
      console.log(submittedData)
      if (this.edit) {
        this.updateItem(submittedData)
      } else {
        this.createItem(submittedData)
      }
    },
    deleteItem(item) {
      console.log(item)
      deleteNode(item).then(() => {
        notifySuccess(`Successfully deleted ${item.name}`)
        this.updateData()
      }).catch(() => {
        notifyFailure(`Failed to delete ${item.name}`)
      })
    },
    createItem(item) {
      createNode(item).then(() => {
        notifySuccess(`Successfully created ${item.name}`)
        this.updateData()
      }).catch(() => {
        notifyFailure(`Failed to create ${item.name}`)
      })
    },
    updateItem(item) {
      updateNode(item).then(() => {
        notifySuccess(`Successfully updated ${item.name}`)
        this.updateData()
      }).catch(() => {
        notifyFailure(`Failed to update ${item.name}`)
      })
    }
  },
  mounted () {
    this.updateData()
  },
  beforeDestroy () {}
}
</script>
