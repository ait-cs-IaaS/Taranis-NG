<template>
  <v-card>
    <v-toolbar>
      <v-toolbar-title>
        <span v-if="edit">{{ $t('report_item.edit') }}</span>
        <span v-else>{{ $t('report_item.add_new') }}</span>
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <v-row class="ma-6"> IMPORT / EXPORT FILE </v-row>

      <v-switch
        style="padding-top: 25px"
        v-model="verticalView"
        label="Side-by-side view"
      ></v-switch>
      <v-switch
        style="padding-top: 25px"
        v-model="report_item.completed"
        label="Completed"
        @change="onEdit('completed')"
      ></v-switch>
      <v-btn v-if="!edit" text dark type="submit" form="form">
        <v-icon left>mdi-content-save</v-icon>
        <span>{{ $t('report_item.save') }}</span>
      </v-btn>
    </v-toolbar>

    <v-row>
      <v-col
        :cols="verticalView ? 6 : 12"
        :style="
          verticalView ? 'height:calc(100vh - 3em); overflow-y: auto;' : ''
        "
      >
        <v-form @submit.prevent="add" id="form" ref="form" class="px-4">
          <v-row no-gutters>
            <v-col cols="12" v-if="edit">
              <span class="caption grey--text">ID: {{ report_item.uuid }}</span>
            </v-col>
            <v-col cols="4" class="pr-3">
              <v-combobox
                @change="reportSelected"
                :disabled="edit"
                v-model="selected_type"
                :items="report_types"
                item-text="title"
                :label="$t('report_item.report_type')"
              />
            </v-col>
            <v-col cols="4" class="pr-3">
              <v-text-field
                @focus="onFocus('title_prefix')"
                @blur="onBlur('title_prefix')"
                @keyup="onKeyUp('title_prefix')"
                :label="$t('report_item.title_prefix')"
                name="title_prefix"
                v-model="report_item.title_prefix"
                :spellcheck="$store.state.settings.spellcheck"
              ></v-text-field>
            </v-col>
            <v-col cols="4" class="pr-3">
              <v-text-field
                @focus="onFocus('title')"
                @blur="onBlur('title')"
                @keyup="onKeyUp('title')"
                :label="$t('report_item.title')"
                name="title"
                type="text"
                v-model="report_item.title"
                v-validate="'required'"
                data-vv-name="title"
                :error-messages="errors.collect('title')"
                :spellcheck="$store.state.settings.spellcheck"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" class="pa-0 ma-0">
              <v-expansion-panels
                class="mb-1"
                v-for="(attribute_group, i) in attribute_groups"
                :key="attribute_group.id"
                v-model="expandPanelGroups"
                multiple
              >
                <v-expansion-panel>
                  <v-expansion-panel-header
                    color="primary--text"
                    class="body-1 text-uppercase pa-3"
                  >
                    {{ attribute_group.title }}
                  </v-expansion-panel-header>
                  <v-expansion-panel-content>
                    <v-expansion-panels
                      multiple
                      focusable
                      class="items"
                      v-model="expand_group_items[i].values"
                    >
                      <v-expansion-panel
                        v-for="attribute_item in attribute_group.attribute_group_items"
                        :key="attribute_item.attribute_group_item.id"
                        class="item-panel"
                      >
                        {{ attribute_item }}
                        <br />
                        XXXX
                        <br />
                        {{ attribute_item.attribute_group_item }}
                        <v-expansion-panel-header
                          class="pa-2 font-weight-bold primary--text rounded-0"
                        >
                          <v-row>
                            <span>
                              {{
                                attribute_item.attribute_group_item.title
                              }}</span
                            >
                          </v-row>
                        </v-expansion-panel-header>
                        <v-expansion-panel-content class="pt-0">
                          <AttributeContainer
                            :attribute_item="attribute_item"
                            :edit="edit"
                            :modify="modify"
                            :report_item_id="report_item.id"
                          />
                        </v-expansion-panel-content>
                      </v-expansion-panel>
                    </v-expansion-panels>
                  </v-expansion-panel-content>
                </v-expansion-panel>
              </v-expansion-panels>
            </v-col>
          </v-row>

          <v-row no-gutters class="pt-2">
            <v-col cols="12">
              <v-alert v-if="show_validation_error" dense type="error" text>
                {{ $t('report_item.validation_error') }}
              </v-alert>
              <v-alert v-if="show_error" dense type="error" text>
                {{ $t('report_item.error') }}
              </v-alert>
            </v-col>
          </v-row>
        </v-form>
      </v-col>
      <v-col
        v-if="verticalView"
        :cols="verticalView ? 6 : 0"
        style="height: calc(100vh - 3em); overflow-y: auto"
        class="pa-5 taranis-ng-vertical-view"
      >
        <card-story
          v-for="(newsItem, index) in news_item_aggregates"
          :key="newsItem.id"
          :newsItem="newsItem"
          :position="index"
        ></card-story>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
// import {
//   createReportItem,
//   updateReportItem,
//   lockReportItem,
//   unlockReportItem,
//   holdLockReportItem,
//   getReportItem,
//   getReportItemData,
//   getReportItemLocks
// } from '@/api/analyze'

import AttributeContainer from '@/components/common/attribute/AttributeContainer'
import CardStory from '@/components/assess/CardStory'

import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'ReportItem',
  props: {
    report_item_prop: Object,
    edit: { type: Boolean, default: false }
  },
  components: {
    AttributeContainer,
    CardStory
  },
  data: () => ({
    verticalView: true,
    headers: [
      { text: 'Value', value: 'value', align: 'left', sortable: true },
      { text: 'Actions', value: 'action', align: 'right', sortable: false }
    ],
    dialog: false,
    dialog_csv: false,
    expand_panel_groups: [],
    expand_group_items: [],
    modify: true,
    overlay: false,
    local_reports: true,
    key_timeout: null,
    show_validation_error: false,
    show_error: false,
    report_types: [],
    selected_type: null,
    attribute_groups: [],
    news_item_aggregates: [],
    remote_report_items: [],
    field_locks: {
      title_prefix: false,
      title: false
    }
  }),
  computed: {
    report_item() {
      return this.report_item_prop
    }
  },
  methods: {
    ...mapGetters(['getUserId']),
    ...mapGetters('analyze', ['getReportItemTypes']),
    ...mapActions('analyze', ['loadReportItemTypes'])
  },
  mounted() {
    this.loadReportItemTypes().then(() => {
      this.report_types = this.getReportItemTypes().items
    })
  },
  beforeDestroy() {}
}
</script>
