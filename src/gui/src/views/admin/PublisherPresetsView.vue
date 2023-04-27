<template>
  <div>
    <DataTable
      v-model:items="presets"
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
      v-model:form-format="formFormat"
      :config-data="formData"
      @submit="handleSubmit"
    ></EditConfig>
  </div>
</template>

<script>
import DataTable from '@/components/common/DataTable.vue'
import EditConfig from '@/components/config/EditConfig.vue'
import {
  deletePublisherPreset,
  createPublisherPreset,
  updatePublisherPreset
} from '@/api/config'
import { mapActions as mapActionsVuex } from 'vuex'
import {
  notifySuccess,
  parseParameterValues,
  createParameterValues,
  objectFromFormat,
  notifyFailure
} from '@/utils/helpers'
import { mapActions, mapState } from 'pinia'
import { configStore } from '@/stores/ConfigStore'

export default {
  name: 'PublisherPresetsView',
  components: {
    DataTable,
    EditConfig
  },
  data: () => ({
    presets: [],
    formData: {},
    parameters: {},
    publishers: [],
    edit: false
  }),
  computed: {
    ...mapState(configStore, ['publisher_presets']),
    ...mapState(configStore, { store_publishers: 'publishers' }),
    formFormat() {
      const base = [
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
          name: 'publisher_id',
          label: 'Type',
          type: 'select',
          required: true,
          options: this.publishers,
          disabled: this.edit
        }
      ]
      if (this.parameters[this.formData.publisher_id]) {
        return base.concat(this.parameters[this.formData.publisher_id])
      }
      return base
    }
  },
  mounted() {
    this.updateData()
  },
  methods: {
    ...mapActions(configStore, ['loadPublisherPresets', 'loadPublishers']),
    ...mapActionsVuex(['updateItemCount']),
    updateData() {
      this.loadPublisherPresets().then(() => {
        this.presets = parseParameterValues(this.publisher_presets.items)
        this.updateItemCount({
          total: this.publisher_presets.total_count,
          filtered: this.publisher_presets.length
        })
      })
      this.loadPublishers().then(() => {
        const publishers = this.store_publishers
        this.publishers = publishers.items.map((publisher) => {
          this.parameters[publisher.id] = publisher.parameters.map(
            (parameter) => {
              return {
                name: parameter.key,
                label: parameter.name,
                type: 'text'
              }
            }
          )
          return {
            value: publisher.id,
            text: publisher.name
          }
        })
      })
    },
    addItem() {
      this.formData = objectFromFormat(this.formFormat)
      this.edit = false
    },
    editItem(item) {
      this.formData = item
      this.edit = true
    },
    handleSubmit(submittedData) {
      delete submittedData.parameter_values
      const parameter_list = this.parameters[this.formData.publisher_id].map(
        (item) => item.name
      )
      const updateItem = createParameterValues(parameter_list, submittedData)
      if (this.edit) {
        this.updateItem(updateItem)
      } else {
        this.createItem(updateItem)
      }
    },
    deleteItem(item) {
      if (!item.default) {
        deletePublisherPreset(item)
          .then(() => {
            notifySuccess(`Successfully deleted ${item.name}`)
            this.updateData()
          })
          .catch(() => {
            notifyFailure(`Failed to delete ${item.name}`)
          })
      }
    },
    createItem(item) {
      createPublisherPreset(item)
        .then(() => {
          notifySuccess(`Successfully created ${item.name}`)
          this.updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to create ${item.name}`)
        })
    },
    updateItem(item) {
      updatePublisherPreset(item)
        .then(() => {
          notifySuccess(`Successfully updated ${item.name}`)
          this.updateData()
        })
        .catch(() => {
          notifyFailure(`Failed to update ${item.name}`)
        })
    }
  }
}
</script>
