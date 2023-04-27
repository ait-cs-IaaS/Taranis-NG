<template>
  <div>
    <DataTable
      v-model:items="users"
      :add-button="true"
      :header-filter="['tag', 'id', 'name', 'username']"
      sort-by-item="id"
      :action-column="true"
      @delete-item="deleteItem"
      @edit-item="editItem"
      @add-item="addItem"
      @update-items="updateData"
    />
    <UserForm v-if="showForm" :user_id="userID"></UserForm>
  </div>
</template>

<script>
import DataTable from '@/components/common/DataTable.vue'
import UserForm from '@/components/config/user/UserForm.vue'
import { deleteUser, createUser, updateUser } from '@/api/config'
import { ref, onMounted } from 'vue'
import { useConfigStore } from '@/stores/ConfigStore'
import { notifySuccess, notifyFailure } from '@/utils/helpers'

export default {
  name: 'UsersView',
  components: {
    DataTable,
    UserForm
  },
  setup() {
    const store = useConfigStore()
    const { users } = storeToRefs(store)
    const mainStore = useMainStore()
    const showForm = ref(false)
    const selected = ref([])
    const userID = ref(-1)

    const updateData = () => {
      store.loadUsers().then(() => {
        mainStore.itemCountTotal = users.total_count
        mainStore.itemCountFiltered = users.items.length
      })
    }

    const addItem = () => {
      userID.value = -1
      showForm.value = true
    }

    const editItem = (item) => {
      userID.value = item.id
      showForm.value = true
    }

    const handleSubmit = (submittedData) => {
      if (showForm.value) {
        updateItem(submittedData)
      } else {
        createItem(submittedData)
      }
    }

    const deleteItem = (item) => {
      deleteUser(item)
        .then(() => {
          notifySuccess(`Successfully deleted ${item.name}`)
          updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to delete ${item.name}`)
        })
    }

    const createItem = (item) => {
      createUser(item)
        .then(() => {
          notifySuccess(`Successfully created ${item.name}`)
          updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to create ${item.name}`)
        })
    }

    const updateItem = (item) => {
      updateUser(item)
        .then(() => {
          notifySuccess(`Successfully updated ${item.name}`)
          updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to update ${item.name}`)
        })
    }

    const selectionChange = (selectedItems) => {
      selected.value = selectedItems.map((item) => item.id)
    }

    onMounted(updateData)

    return {
      showForm,
      users,
      selected,
      userID,
      addItem,
      editItem,
      handleSubmit,
      deleteItem,
      createItem,
      updateItem,
      selectionChange
    }
  }
}
</script>
