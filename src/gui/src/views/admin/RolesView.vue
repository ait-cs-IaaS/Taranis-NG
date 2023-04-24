<template>
  <div>
    <DataTable
      v-model:items="roles"
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
      :form-format="formFormat"
      @submit="handleSubmit"
    ></EditConfig>
  </div>
</template>

<script>
import DataTable from '@/components/common/DataTable.vue'
import EditConfig from '@/components/config/EditConfig.vue'
import { deleteRole, createRole, updateRole } from '@/api/config'
import { ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import { notifySuccess, objectFromFormat, notifyFailure } from '@/utils/helpers'

export default {
  name: 'RolesView',
  components: {
    DataTable,
    EditConfig
  },
  setup() {
    const store = useStore()
    const roles = ref([])
    const formData = ref({})
    const selected = ref([])
    const edit = ref(false)
    const permissions = ref([])

    const formFormat = computed(() => [
      {
        name: 'id',
        label: 'ID',
        type: 'text',
        disabled: true
      },
      {
        name: 'name',
        label: 'Name',
        type: 'text',
        required: true
      },
      {
        name: 'description',
        label: 'Description',
        type: 'textarea',
        required: true
      },
      {
        name: 'permissions',
        label: 'Permissions',
        type: 'table',
        headers: [
          { text: 'Name', value: 'name' },
          { text: 'Description', value: 'description' }
        ],
        items: permissions.value
      }
    ])

    const loadRoles = () => store.dispatch('config/loadRoles')
    const loadPermissions = () => store.dispatch('config/loadPermissions')
    const getRoles = () => store.getters['config/getRoles']
    const getPermissions = () => store.getters['config/getPermissions']
    const updateItemCount = (count) => store.dispatch('updateItemCount', count)
    const updateData = () => {
      loadRoles().then(() => {
        const sources = getRoles()
        roles.value = sources.items
        updateItemCount({
          total: sources.total_count,
          filtered: sources.length
        })
      })
      loadPermissions().then(() => {
        permissions.value = getPermissions().items
      })
    }

    const addItem = () => {
      formData.value = objectFromFormat(formFormat.value)
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
        deleteRole(item)
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
      createRole(item)
        .then(() => {
          notifySuccess(`Successfully created ${item.name}`)
          updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to create ${item.name}`)
        })
    }

    const updateItem = (item) => {
      updateRole(item)
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
      roles,
      formData,
      selected,
      edit,
      permissions,
      formFormat,
      addItem,
      editItem,
      handleSubmit,
      deleteItem,
      selectionChange,
      updateData
    }
  }
}
</script>
