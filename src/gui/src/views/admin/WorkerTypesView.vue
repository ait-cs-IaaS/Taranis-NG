<template>
  <div>
    <DataTable
      v-model:items="worker_types.items"
      :add-button="false"
      :header-filter="['name', 'description', 'type']"
      sort-by-item="name"
      :action-column="true"
      @edit-item="editItem"
      @update-items="updateData"
    >
      <template #actionColumn="source">
        <v-tooltip left>
          <template #activator="{ props }">
            <v-icon
              v-bind="props"
              color="secondary"
              icon="mdi-run"
              @click.stop="executeBot(source.item)"
            />
          </template>
          <span>Execute Bot</span>
        </v-tooltip>
      </template>
    </DataTable>
    <!-- // TODO: https://github.com/SortableJS/vue.draggable.next for reordering -->
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
import { updateBot, executeBotTask } from '@/api/config'
import { ref, computed, onMounted } from 'vue'
import { useConfigStore } from '@/stores/ConfigStore'
import { useMainStore } from '@/stores/MainStore'
import { notifySuccess, notifyFailure } from '@/utils/helpers'
import { storeToRefs } from 'pinia'

export default {
  name: 'WorkerTypesView',
  components: {
    DataTable,
    EditConfig
  },
  setup() {
    const mainStore = useMainStore()
    const configStore = useConfigStore()

    // data
    const { worker_types } = storeToRefs(configStore)
    const formData = ref({})

    // computed
    const formFormat = computed(() => {
      let base = [
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
          rules: [(v) => !!v || 'Required']
        },
        {
          name: 'description',
          label: 'Description',
          type: 'textarea',
          rules: [(v) => !!v || 'Required']
        },
        {
          name: 'type',
          label: 'Type',
          type: 'text',
          disabled: true
        }
      ]
      for (const parameter in formData.value.parameters) {
        base = base.concat({
          name: parameter,
          label: parameter,
          type: 'text'
        })
      }
      return base
    })

    // methods
    const updateData = () => {
      configStore.loadWorkerTypes().then(() => {
        mainStore.itemCountTotal = worker_types.value.total_count
        mainStore.itemCountFiltered = worker_types.value.items.length
      })
    }

    const editItem = (item) => {
      formData.value = item
    }

    const handleSubmit = (submittedData) => {
      console.debug(submittedData)
      updateItem(submittedData)
    }

    const updateItem = (item) => {
      updateBot(item)
        .then(() => {
          notifySuccess(`Successfully updated ${item.id}`)
          updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to update ${item.id}`)
        })
    }

    const executeBot = (item) => {
      executeBotTask(item.id)
        .then(() => {
          notifySuccess(`Successfully executed ${item.id}`)
        })
        .catch(() => {
          notifyFailure(`Failed to execute ${item.id}`)
        })
    }

    onMounted(() => {
      updateData()
    })

    return {
      // data
      worker_types,
      formData,

      // computed
      formFormat,

      // methods
      updateData,
      editItem,
      handleSubmit,
      updateItem,
      executeBot
    }
  }
}
</script>
