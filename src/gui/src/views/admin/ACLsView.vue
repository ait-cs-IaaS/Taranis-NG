<template>
  <div>
    <DataTable
      v-model:items="acls"
      :add-button="true"
      :header-filter="['tag', 'id', 'name', 'username']"
      sort-by-item="id"
      :action-column="true"
      @delete-item="deleteItem"
      @edit-item="editItem"
      @add-item="addItem"
      @update-items="updateData"
    />
    <NewACL v-if="showForm" :user_id="userID"></NewACL>
  </div>
</template>

<script>
import DataTable from '@/components/common/DataTable.vue'
import NewACL from '@/components/config/user/NewACL.vue'
import { deleteACLEntry, createACLEntry, updateACLEntry } from '@/api/config'
import { notifySuccess } from '@/utils/helpers'
import { mapActions, mapState, mapWritableState } from 'pinia'
import { useConfigStore } from '@/stores/ConfigStore'
import { useMainStore } from '@/stores/MainStore'

export default {
  name: 'ACLsView',
  components: {
    DataTable,
    NewACL
  },
  data: () => ({
    showForm: false,
    edit: false
  }),
  computed: {
    ...mapState(useConfigStore, ['acls']),
    ...mapWritableState(useMainStore, ['itemCountTotal', 'itemCountFiltered'])
  },
  mounted() {
    this.updateData()
  },
  methods: {
    ...mapActions(useConfigStore, ['loadACLEntries']),
    updateData() {
      this.loadACLEntries().then(() => {
        this.itemCountTotal = this.acls.total_count
        this.itemCountFiltered = this.acls.items.length
      })
    },
    addItem() {
      this.userID = null
      this.showForm = true
    },
    editItem(item) {
      this.userID = item.id
      this.showForm = true
    },
    handleSubmit(submittedData) {
      if (this.showForm) {
        this.updateItem(submittedData)
      } else {
        this.createItem(submittedData)
      }
    },
    deleteItem(item) {
      deleteACLEntry(item).then(() => {
        notifySuccess(`Successfully deleted ${item.name}`)
        this.updateData()
      })
    },
    createItem(item) {
      createACLEntry(item).then(() => {
        notifySuccess(`Successfully created ${item.name}`)
        this.updateData()
      })
    },
    updateItem(item) {
      updateACLEntry(item).then(() => {
        notifySuccess(`Successfully updated ${item.name}`)
        this.updateData()
      })
    }
  }
}
</script>
