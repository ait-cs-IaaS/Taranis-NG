<template>
  <div>
    <DataTable
      v-model:items="osint_source_groups.items"
      :add-button="true"
      :header-filter="['tag', 'default', 'name', 'description']"
      sort-by-item="id"
      :action-column="true"
      @delete-item="deleteItem"
      @edit-item="editItem"
      @add-item="addItem"
      @selection-change="selectionChange"
      @update-items="updateData"
    >
    </DataTable>
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
import {
  createOSINTSourceGroup,
  deleteOSINTSourceGroup,
  updateOSINTSourceGroup
} from '@/api/config'
import { ref, computed, onMounted } from 'vue'
import { notifySuccess, objectFromFormat, notifyFailure } from '@/utils/helpers'
import { useConfigStore } from '@/stores/ConfigStore'
import { storeToRefs } from 'pinia'

export default {
  name: 'OSINTSourceGroupsView',
  components: {
    DataTable,
    EditConfig
  },
  setup() {
    const store = useConfigStore()
    const mainStore = useMainStore()
    const { osint_source_groups, osint_sources } = storeToRefs(store)
    const selected = ref([])
    const formData = ref({})
    const edit = ref(false)

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
        name: 'osint_sources',
        label: 'Sources',
        type: 'table',
        headers: [
          { text: 'Name', value: 'name' },
          { text: 'Description', value: 'description' }
        ],
        items: osint_sources.items
      }
    ])

    const updateData = () => {
      store.loadOSINTSourceGroups().then(() => {
        mainStore.itemCountTotal = osint_source_groups.total_count
        mainStore.itemCountFiltered = osint_source_groups.items.length
      })
      loadOSINTSources().then()
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
      if (edit.value) {
        console.debug(`Update: ${submittedData}`)
        updateItem(submittedData)
      } else {
        console.debug(`Create: ${submittedData}`)
        createItem(submittedData)
      }
    }

    const deleteItem = (item) => {
      deleteOSINTSourceGroup(item)
        .then(() => {
          notifySuccess(`Successfully deleted ${item.name}`)
          updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to delete ${item.name}`)
        })
    }

    const createItem = (item) => {
      createOSINTSourceGroup(item)
        .then(() => {
          notifySuccess(`Successfully created ${item.name}`)
          updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to create ${item.name}`)
        })
    }

    const updateItem = (item) => {
      updateOSINTSourceGroup(item)
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
      osint_source_groups,
      osint_sources,
      selected,
      formData,
      edit,
      formFormat,
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
