<template>
  <div>
    <DataTable
      :addButton="true"
      :items.sync="users"
      :headerFilter="['tag', 'id', 'name', 'username']"
      sortByItem="id"
      :actionColumn="true"
      @delete-item="deleteItem"
      @edit-item="editItem"
      @add-item="addItem"
      @update-items="updateData"
    />
    <UserForm v-if="showForm" :user_id="userID"></UserForm>
  </div>
</template>

<script>
import DataTable from '@/components/common/DataTable'
import UserForm from '../../components/config/user/UserForm'
import { deleteUser, createUser, updateUser } from '@/api/config'
import { mapActions, mapGetters } from 'vuex'
import { notifySuccess, notifyFailure } from '@/utils/helpers'

export default {
  name: 'UsersView',
  components: {
    DataTable,
    UserForm
  },
  data: () => ({
    showForm: false,
    users: [],
    selected: [],
    userID: -1
  }),
  methods: {
    ...mapActions('config', ['loadUsers']),
    ...mapGetters('config', ['getUsers']),
    ...mapActions(['updateItemCount']),
    updateData() {
      this.loadUsers().then(() => {
        const sources = this.getUsers()
        this.users = sources.items
        this.updateItemCount({
          total: sources.total_count,
          filtered: sources.length
        })
      })
    },
    addItem() {
      this.userID = -1
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
      deleteUser(item)
        .then(() => {
          notifySuccess(`Successfully deleted ${item.name}`)
          this.updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to delete ${item.name}`)
        })
    },
    createItem(item) {
      createUser(item)
        .then(() => {
          notifySuccess(`Successfully created ${item.name}`)
          this.updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to created ${item.name}`)
        })
    },
    updateItem(item) {
      updateUser(item)
        .then(() => {
          notifySuccess(`Successfully updated ${item.name}`)
          this.updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to update ${item.name}`)
        })
    },
    selectionChange(selected) {
      this.selected = selected.map((item) => item.id)
    }
  },
  mounted() {
    this.updateData()
  }
}
</script>
