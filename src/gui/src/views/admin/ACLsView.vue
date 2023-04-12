<template>
  <div>
    <DataTable :addButton="true" :items.sync="acls.items" :headerFilter="['tag', 'id', 'name', 'username']" sortByItem="id"
      :actionColumn="true" @delete-item="deleteItem" @edit-item="editItem" @add-item="addItem"
      @update-items="updateData" />
    <NewACL v-if="showForm" :user_id.sync="userID"></NewACL>
  </div>
</template>

<script>
import DataTable from '@/components/common/DataTable'
import NewACL from '../../components/config/user/NewACL'
import { deleteACLEntry, createACLEntry, updateACLEntry } from '@/api/config'
import { notifySuccess } from '@/utils/helpers'
import { mapActions, mapState } from 'pinia'
import { configStore } from '@/stores/ConfigStore'
import { mapActions as mapActionsVuex } from 'vuex'

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
    ...mapState(configStore, ['acls'])
  },
  methods: {
    ...mapActions(configStore, ['loadACLEntries']),
    ...mapActionsVuex(['updateItemCount']),
    updateData() {
      this.loadACLEntries().then(() => {
        this.updateItemCount({
          total: this.acls.total_count,
          filtered: this.acls.length
        })
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
  },
  mounted() {
    this.updateData()
  },
  beforeDestroy() { }
}

</script>
