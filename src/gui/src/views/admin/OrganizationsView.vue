<template>
  <div>
    <DataTable
      v-model:items="organizations"
      :add-button="true"
      :header-filter="['tag', 'id', 'name', 'description']"
      sort-by-item="id"
      :action-column="true"
      @delete-item="deleteItem"
      @edit-item="editItem"
      @add-item="addItem"
      @update-items="updateData"
    />
    <EditConfig
      v-if="formData && Object.keys(formData).length > 0"
      :config-data="formData"
      @submit="handleSubmit"
    ></EditConfig>
  </div>
</template>

<script>
import DataTable from '@/components/common/DataTable.vue'
import EditConfig from '@/components/config/EditConfig.vue'
import {
  deleteOrganization,
  createOrganization,
  updateOrganization
} from '@/api/config'
import { useStore } from 'vuex'
import { notifySuccess, emptyValues, notifyFailure } from '@/utils/helpers'
import { ref, onMounted } from 'vue'

export default {
  name: 'OrganizationsView',
  components: {
    DataTable,
    EditConfig
  },
  setup() {
    const store = useStore()
    const organizations = ref([])
    const formData = ref({})
    const edit = ref(false)

    const loadOrganizations = () => store.dispatch('config/loadOrganizations')
    const getOrganizations = () => store.getters['config/getOrganizations']
    const updateItemCount = (count) => store.dispatch('updateItemCount', count)

    const updateData = () => {
      loadOrganizations().then(() => {
        const sources = getOrganizations()
        organizations.value = sources.items
        updateItemCount({
          total: sources.total_count,
          filtered: sources.length
        })
      })
    }

    const addItem = () => {
      formData.value = emptyValues(organizations.value[0])
      edit.value = false
    }

    const editItem = (item) => {
      formData.value = item
      edit.value = true
    }

    const handleSubmit = (submittedData) => {
      console.log(submittedData)
      if (edit.value) {
        updateItem(submittedData)
      } else {
        createItem(submittedData)
      }
    }

    const deleteItem = (item) => {
      if (!item.default) {
        deleteOrganization(item)
          .then(() => {
            notifySuccess(`Successfully deleted ${item.name}`)
            updateData()
          })
          .catch(() => {
            notifyFailure(`Failed to delete ${item.name}`)
          })
      }
    }

    const createItem = (item) => {
      createOrganization(item)
        .then(() => {
          notifySuccess(`Successfully created ${item.name}`)
          updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to create ${item.name}`)
        })
    }

    const updateItem = (item) => {
      updateOrganization(item)
        .then(() => {
          notifySuccess(`Successfully updated ${item.name}`)
          updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to update ${item.name}`)
        })
    }

    onMounted(updateData)

    return {
      organizations,
      formData,
      edit,
      addItem,
      editItem,
      handleSubmit,
      deleteItem,
      createItem,
      updateItem
    }
  }
}
</script>
