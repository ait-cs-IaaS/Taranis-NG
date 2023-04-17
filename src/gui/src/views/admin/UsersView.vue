<template>
  <div>
    <DataTable
      :addButton="true"
      :items.sync="users.items"
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
import { mapActions as mapActionsVuex } from 'vuex'
import { mapActions, mapState } from 'pinia'
import { configStore } from '@/stores/ConfigStore'

export default {
  name: 'UsersView',
  components: {
    DataTable,
    UserForm
  },
  data: () => ({
    showForm: false,
    selected: [],
    userID: -1
  }),
  computed: {
    ...mapState(configStore, ['users'])
  },
  methods: {
    ...mapActions(configStore, ['loadUsers']),
    ...mapActionsVuex(['updateItemCount']),
    updateData() {
      this.loadUsers().then(() => {
        this.updateItemCount({
          total: this.users.total_count,
          filtered: this.users.length
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
      if (!item.default) {
        deleteUser(item).then(() => {
          this.message = `Successfully deleted ${item.name}`
          this.dialog = true
          this.$root.$emit('notification', {
            type: 'success',
            loc: `Successfully deleted ${item.name}`
          })
          this.updateData()
        })
      }
    },
    createItem(item) {
      createUser(item).then(() => {
        this.$root.$emit('notification', {
          type: 'success',
          loc: `Successfully added ${item.name}`
        })
        this.updateData()
      })
    },
    updateItem(item) {
      updateUser(item).then(() => {
        this.$root.$emit('notification', {
          type: 'success',
          loc: `Successfully updated ${item.name}`
        })
        this.updateData()
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
