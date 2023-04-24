<template>
  <v-container fluid class="ma-5 mt-5 pa-5 pt-0">
    <v-form id="form" ref="form" @submit.prevent="add">
      <v-row no-gutters>
        <v-btn type="submit" color="success" class="mr-4"> Submit </v-btn>
      </v-row>
      <v-row no-gutters>
        <v-col v-if="edit" cols="12" class="cation grey--text">
          ID:{{ report_type.id }}
        </v-col>
        <v-col cols="12">
          <v-text-field
            v-model="report_type.title"
            v-validate="'required'"
            :disabled="!canUpdate"
            :label="$t('report_type.name')"
            name="name"
            data-vv-name="name"
            :error-messages="errors.collect('name')"
          />
        </v-col>
        <v-col cols="12">
          <v-textarea
            v-model="report_type.description"
            :disabled="!canUpdate"
            :label="$t('report_type.description')"
            name="description"
          />
        </v-col>
      </v-row>

      <v-row no-gutters>
        <v-col cols="12">
          <v-btn v-if="canUpdate" color="primary" @click="addAttributeGroup">
            <v-icon left>{{ UI.ICON.PLUS }}</v-icon>
            <span>{{ $t('report_type.new_group') }}</span>
          </v-btn>
        </v-col>
        <v-col cols="12">
          <v-card
            v-for="(group, index) in report_type.attribute_groups"
            :key="group.id"
            style="margin-top: 8px"
          >
            <v-toolbar dark height="32px">
              <v-spacer></v-spacer>
              <v-toolbar-items v-if="canUpdate">
                <v-icon @click="moveAttributeGroupUp(index)">
                  mdi-arrow-up-bold
                </v-icon>
                <v-icon @click="moveAttributeGroupDown(index)">
                  mdi-arrow-down-bold
                </v-icon>

                <v-icon @click="deleteAttributeGroup(index)"> delete </v-icon>
              </v-toolbar-items>
            </v-toolbar>

            <v-card-text>
              <v-text-field
                v-model="group.title"
                :disabled="!canUpdate"
                :label="$t('report_type.name')"
                name="name"
                type="text"
                :spellcheck="$store.state.settings.spellcheck"
              ></v-text-field>
              <v-textarea
                v-model="group.description"
                :disabled="!canUpdate"
                :label="$t('report_type.description')"
                name="description"
                :spellcheck="$store.state.settings.spellcheck"
              ></v-textarea>
              <v-text-field
                v-model="group.section_title"
                :disabled="!canUpdate"
                :label="$t('report_type.section_title')"
                name="section_title"
                :spellcheck="$store.state.settings.spellcheck"
              ></v-text-field>
              <AttributeTable
                v-model:attributes="
                  report_type.attribute_groups[index].attribute_group_items
                "
                :disabled="!canUpdate"
                @update="(items) => updateAttributeGroupItems(index, items)"
              />
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script>
import { createReportItemType, updateReportItemType } from '@/api/config'
import AttributeTable from './AttributeTable'
import { notifySuccess, notifyFailure } from '@/utils/helpers'

export default {
  name: 'ReportTypeForm',
  components: {
    AttributeTable
  },
  props: {
    reportTypeData: {
      type: Object || null,
      required: false,
      default: null
    }
  },
  data: () => ({
    edit: false,
    report_type: {
      id: -1,
      title: '',
      description: '',
      attribute_groups: []
    }
  }),
  mounted() {
    if (this.reportTypeData) {
      this.edit = true
      this.report_type = this.reportTypeData
    }
  },
  methods: {
    updateAttributeGroupItems(index, items) {
      console.debug('RECEIVED')
      this.report_type.attribute_groups[index].attribute_group_items = items
    },
    editAttributeItem(index, item) {
      console.debug(`Edit Attribute Item ${item}`)
    },
    deleteAttributeItem(index, item) {
      console.debug(`Delete Attribute Item ${item}`)
    },
    addReportType() {
      this.edit = false
      this.report_type.id = -1
      this.report_type.title = ''
      this.report_type.description = ''
      this.report_type.categories = []
      this.report_type.attribute_groups = []
      this.$validator.reset()
    },

    addAttributeGroup() {
      this.report_type.attribute_groups.push({
        index: this.report_type.attribute_groups.length,
        id: -1,
        title: '',
        description: '',
        section: -1,
        section_title: '',
        attribute_group_items: []
      })
    },

    moveAttributeGroupUp(index) {
      if (index > 0) {
        this.report_type.attribute_groups.splice(
          index - 1,
          0,
          this.report_type.attribute_groups.splice(index, 1)[0]
        )
      }
    },

    moveAttributeGroupDown(index) {
      if (index < this.report_type.attribute_groups.length - 1) {
        this.report_type.attribute_groups.splice(
          index + 1,
          0,
          this.report_type.attribute_groups.splice(index, 1)[0]
        )
      }
    },

    deleteAttributeGroup(index) {
      this.report_type.attribute_groups.splice(index, 1)
    },

    add() {
      console.debug('Submitting: ')
      console.debug(this.report_type.attribute_groups)
      this.$validator.validateAll().then(() => {
        if (!this.$validator.errors.any()) {
          for (let x = 0; x < this.report_type.attribute_groups.length; x++) {
            this.report_type.attribute_groups[x].index = x

            for (
              let y = 0;
              y <
              this.report_type.attribute_groups[x].attribute_group_items.length;
              y++
            ) {
              this.report_type.attribute_groups[x].attribute_group_items[
                y
              ].index = y
            }
          }

          if (this.edit) {
            updateReportItemType(this.report_type)
              .then(() => {
                this.$validator.reset()
                notifySuccess('report_type.successful_edit')
              })
              .catch(() => {
                notifyFailure('report_type.error')
              })
          } else {
            createReportItemType(this.report_type)
              .then(() => {
                this.$validator.reset()
                notifySuccess('report_type.successful')
              })
              .catch(() => {
                notifyFailure('report_type.error')
              })
          }
        } else {
          notifyFailure('report_type.validation_error')
        }
      })
    }
  }
}
</script>
