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
      ></v-switch>
      <v-btn text dark>
        <v-icon left>mdi-content-save</v-icon>
        <span>{{ $t('report_item.save') }}</span>
      </v-btn>
    </v-toolbar>

    <v-row>
      <v-col
        :cols="verticalView ? 6 : 12"
        :class="verticalView ? 'taranis-ng-vertical-view' : ''"
      >
        <v-row no-gutters>
          <v-col cols="12" v-if="edit">
            <span class="caption">ID: {{ report_item.uuid }}</span>
          </v-col>
          <v-col cols="4" class="pr-3">
            <v-select
              :disabled="edit"
              v-model="report_item.report_item_type_id"
              item-text="title"
              item-value="id"
              :items="report_types"
              :label="$t('report_item.report_type')"
            />
          </v-col>
          <v-col cols="4" class="pr-3">
            <v-text-field
              :label="$t('report_item.title_prefix')"
              name="title_prefix"
              v-model="report_item.title_prefix"
            ></v-text-field>
          </v-col>
          <v-col cols="4" class="pr-3">
            <v-text-field
              :label="$t('report_item.title')"
              name="title"
              type="text"
              v-model="report_item.title"
              v-validate="'required'"
              :error-messages="errors.collect('title')"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" class="pa-0 ma-0">
            {{report_item}}
            <v-expansion-panels
              class="mb-1"
              v-for="(attribute_group, i) in report_item.attribute_groups"
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
                  {{ expand_group_items[i].values }}
                  {{ attribute_group.attribute_group_items }}
                  <AttributeContainer
                    :attribute_item="attribute_item"
                    :edit="edit"
                    :modify="modify"
                    :report_item_id="report_item.id"
                  />
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>
          </v-col>
        </v-row>
      </v-col>
      <v-col
        :cols="verticalView ? 6 : 12"
        class="pa-5 taranis-ng-vertical-view"
      >
        <card-story
          v-for="newsItem in report_item.news_item_aggregates"
          :key="newsItem.id"
          :story="newsItem"
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
    expand_panel_groups: [],
    modify: true,
    report_types: [],
    report_types_selection: []
  }),
  computed: {
    report_item() {
      return this.report_item_prop
    }
  },
  methods: {
    ...mapGetters(['getUserId']),
    ...mapGetters('analyze', ['getReportTypes']),
    ...mapActions('analyze', ['loadReportTypes'])
  },
  mounted() {
    this.loadReportTypes().then(() => {
      this.report_types = this.getReportTypes().items
    })
  },
  beforeDestroy() {}
}
</script>
