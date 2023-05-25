<template>
  <div>
    <DataTable
      v-model:items="acls.items"
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
import { ref, onMounted } from 'vue'
import DataTable from '@/components/common/DataTable.vue'
import NewACL from '@/components/config/user/NewACL.vue'
import { deleteACLEntry, createACLEntry, updateACLEntry } from '@/api/config'
import { notifySuccess } from '@/utils/helpers'
import { useConfigStore } from '@/stores/ConfigStore'
import { useMainStore } from '@/stores/MainStore'

export default {
  name: 'ACLsView',
  components: {
    DataTable,
    NewACL
  },
  setup() {
    const showForm = ref(false)
    const edit = ref(false)
    const userID = ref(null)
    const acls = useConfigStore().acls
    const mainStore = useMainStore()

    const updateData = () => {
      useConfigStore()
        .loadACLEntries()
        .then(() => {
          mainStore.itemCountTotal = acls.total_count
          mainStore.itemCountFiltered = acls.items.length
        })
    }

    const addItem = () => {
      userID.value = null
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
      deleteACLEntry(item).then(() => {
        notifySuccess(`Successfully deleted ${item.name}`)
        updateData()
      })
    }

    const createItem = (item) => {
      createACLEntry(item).then(() => {
        notifySuccess(`Successfully created ${item.name}`)
        updateData()
      })
    }

    const updateItem = (item) => {
      updateACLEntry(item).then(() => {
        notifySuccess(`Successfully updated ${item.name}`)
        updateData()
      })
    }

    onMounted(() => {
      updateData()
    })

    return {
      showForm,
      edit,
      userID,
      acls,
      addItem,
      editItem,
      handleSubmit,
      deleteItem,
      createItem,
      updateItem,
      updateData
    }
  }
}
</script>
