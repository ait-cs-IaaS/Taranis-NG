<template>
  <v-row v-bind="UI.DIALOG.ROW.WINDOW">
    <v-btn
      v-if="modify && groups.length > 0"
      depressed
      small
      @click="openSelector"
    >
      <v-icon left>mdi-plus</v-icon>
      <span>{{ $t('report_item.select_remote') }}</span>
    </v-btn>

    <v-dialog v-bind="UI.DIALOG.FULLSCREEN" v-model="dialog" news-item-selector>
      <v-card fixed>
        <v-toolbar v-bind="UI.DIALOG.TOOLBAR" :style="UI.STYLE.z10000">
          <v-btn icon dark @click="close">
            <v-icon>mdi-close-circle</v-icon>
          </v-btn>
          <v-toolbar-title>{{
            $t('report_item.select_remote')
          }}</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn text dark @click="add">
            <v-icon left>mdi-plus-box</v-icon>
            <span>{{ $t('report_item.add') }}</span>
          </v-btn>
        </v-toolbar>

        <v-row class="cs-inside">
          <v-col class="cs-panel">
            <v-list-item
              v-for="link in links"
              :key="link.id"
              dense
              :class="link.id === selected_group_id ? 'active' : ''"
              @click="changeGroup($event, link.id)"
            >
              <v-list-item-content v-if="!link.separator">
                <v-icon regular color="cx-drawer-text">{{ link.icon }}</v-icon>
                <v-list-item-title class="cx-drawer-text--text"
                  >{{ $t(link.title) }}
                </v-list-item-title>
              </v-list-item-content>
              <v-list-item-content v-else class="separator">
                <v-divider class="section-divider" color="white"></v-divider>
              </v-list-item-content>
            </v-list-item>
          </v-col>
          <v-col class="cs-content">
            <ToolbarFilterAnalyze
              ref="toolbarFilter"
              publish_selector
              total_count_title="analyze.total_count"
              @update-report-items-filter="updateFilter"
            ></ToolbarFilterAnalyze>
            <ContentDataAnalyze
              ref="contentData"
              publish_selector
              :selection="values"
              class="item-selector"
              card-item="CardAnalyze"
              @show-remote-report-item-detail="showReportItemDetail"
              @new-data-loaded="newDataLoaded"
            />
          </v-col>
        </v-row>
      </v-card>
    </v-dialog>

    <v-spacer style="height: 8px"></v-spacer>

    <RemoteReportItem ref="remoteReportItemDialog" />

    <component
      :is="cardLayout()"
      v-for="value in values"
      :key="value.id"
      publish_selector
      class="item-selector ml-4"
      :card="value"
      @show-remote-report-item-detail="showReportItemDetail"
      @remove-report-item-from-selector="removeReportItemFromSelector"
    />
  </v-row>
</template>

<script>
import ContentDataAnalyze from '@/components/analyze/ContentDataAnalyze.vue'
import CardAnalyze from '../analyze/CardAnalyze'
import ToolbarFilterAnalyze from '@/components/analyze/ToolbarFilterAnalyze.vue'
import RemoteReportItem from '@/components/analyze/RemoteReportItem.vue'
import Permissions from '@/services/auth/permissions'
import { getReportItemData, updateReportItem } from '@/api/analyze'
import { useAnalyzeStore } from '@/stores/AnalyzeStore'
import { mapActions, mapState } from 'pinia'
import { useMainStore } from '@/stores/MainStore'

export default {
  name: 'RemoteReportItemSelector',
  components: {
    ToolbarFilterAnalyze,
    ContentDataAnalyze,
    CardAnalyze,
    RemoteReportItem
  },
  props: {
    report_items: Array,
    modify: Boolean,
    edit: Boolean,
    report_item_id: Number
  },
  data: () => ({
    values: this.report_items,
    dialog: false,
    value: '',
    groups: [],
    links: [],
    selected_group_id: ''
  }),
  computed: {
    ...mapState(useAnalyzeStore, [
      'report_item_groups',
      'current_report_item_group_id',
      'selection_report'
    ]),
    ...mapState(useMainStore, ['user']),
    canModify() {
      return (
        this.edit === false ||
        (this.checkPermission(Permissions.ANALYZE_UPDATE) &&
          this.modify === true)
      )
    }
  },
  methods: {
    ...mapActions(useAnalyzeStore, [
      'loadReportItemGroups',
      'setMultiSelectReport'
    ]),

    newDataLoaded(count) {
      this.$refs.toolbarFilter.updateDataCount(count)
    },

    changeGroup(e, group_id) {
      this.selected_group_id = group_id
      this.current_report_item_group_id = group_id
      this.$refs.contentData.updateData(false, false)
    },

    updateFilter(filter) {
      this.$refs.contentData.updateFilter(filter)
    },

    showReportItemDetail(report_item) {
      this.$refs.remoteReportItemDialog.showDetail(report_item)
    },

    removeReportItemFromSelector(report_item) {
      const data = {}
      data.delete = true
      data.remote_report_item_id = report_item.id

      if (this.edit === true) {
        updateReportItem(this.report_item_id, data).then(() => {
          const i = this.values.indexOf(report_item)
          this.values.splice(i, 1)
        })
      } else {
        const i = this.values.indexOf(report_item)
        this.values.splice(i, 1)
      }
    },

    cardLayout: function () {
      return 'CardAnalyze'
    },

    openSelector() {
      this.setMultiSelectReport(true)
      this.dialog = true
      this.$refs.contentData.updateData(false, false)
    },

    add() {
      const selection = this.selection_report
      const added_values = []
      const data = {}
      data.add = true
      data.report_item_id = this.report_item_id
      data.remote_report_item_ids = []
      for (let i = 0; i < selection.length; i++) {
        let found = false
        for (let j = 0; j < this.values.length; j++) {
          if (this.values[j].id === selection[i].item.id) {
            found = true
            break
          }
        }

        if (found === false) {
          added_values.push(selection[i].item)
          data.remote_report_item_ids.push(selection[i].item.id)
        }
      }

      if (this.edit === true) {
        updateReportItem(this.report_item_id, data).then(() => {
          for (let i = 0; i < added_values.length; i++) {
            this.values.push(added_values[i])
          }
        })
      } else {
        for (let i = 0; i < added_values.length; i++) {
          this.values.push(added_values[i])
        }
      }
      this.close()
    },

    close() {
      this.setMultiSelectReport(false)
      this.dialog = false
    },

    report_item_updated(data_info) {
      if (
        this.edit === true &&
        this.report_item_id === data_info.report_item_id
      ) {
        if (data_info.user_id !== this.user.id) {
          if (data_info.add !== undefined) {
            getReportItemData(this.report_item_id, data_info).then(
              (response) => {
                const data = response.data
                for (let i = 0; i < data.remote_report_items.length; i++) {
                  this.values.push(data.remote_report_items[i])
                }
              }
            )
          } else if (data_info.delete !== undefined) {
            for (let i = 0; i < this.values.length; i++) {
              if (this.values[i].id === data_info.remote_report_item_id) {
                this.values.splice(i, 1)
                break
              }
            }
          }
        }
      }
    }
  },
  mounted() {
    this.loadReportItemGroups().then(() => {
      this.groups = this.report_item_groups

      for (let i = 0; i < this.groups.length; i++) {
        this.links.push({
          icon: 'mdi-arrow-down-bold-circle-outline',
          title: this.groups[i],
          id: this.groups[i]
        })
      }

      if (this.current_report_item_group_id === null && this.links) {
        if (this.links.length > 0) {
          this.selected_group_id = this.links[0].id
          this.current_report_item_group_id = this.links[0].id
        }
      } else {
        this.selected_group_id = this.current_report_item_group_id
      }
    })

    this.$root.$on('report-item-updated', this.report_item_updated)
  },

  beforeUnmount() {
    this.$root.$off('report-item-updated', this.report_item_updated)
  }
}
</script>
