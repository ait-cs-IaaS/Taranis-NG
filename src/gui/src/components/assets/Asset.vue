<template>
  <v-container fluid>
    <v-row no-gutters>
      <v-col cols="6" class="pr-3">
        <v-text-field
          :label="$t('asset.name')"
          v-model="asset.name"
          :rules="required"
        />
      </v-col>
      <v-col cols="6" class="pr-3">
        <v-text-field :hint="$t('asset.serial')" v-model="asset.serial" />
      </v-col>
      <v-col cols="12" class="pr-3">
        <v-textarea
          :label="$t('asset.description')"
          v-model="asset.description"
          :spellcheck="$store.state.settings.spellcheck"
        />
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col cols="12">
        <CPETable :asset_cpes="asset.asset_cpes" @update-cpes="update" />
      </v-col>
      <v-col cols="12">
        <card-vulnerability :vulnerabilities="vulnerabilities" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { createAsset, updateAsset } from '@/api/assets'

import CPETable from '@/components/assets/CPETable'
import CardVulnerability from '@/components/assets/CardVulnerability'

export default {
  name: 'Asset',
  components: {
    CPETable,
    CardVulnerability
  },
  props: {
    asset_prop: { type: Object, default: () => {}, required: true },
    edit: { type: Boolean, default: false }
  },
  emits: ['reportcreated'],
  data: function () {
    return {
      required: [(v) => !!v || 'Required'],
      vulnerabilities: [],
      asset: this.asset_prop
    }
  },
  methods: {
    cardLayout() {
      return 'CardVulnerability'
    },
    addAsset() {
      this.visible = true
      this.asset.id = -1
      this.asset.name = ''
      this.asset.serial = ''
      this.asset.description = ''
      this.asset.asset_cpes = []
      this.asset.asset_group_id = ''
      this.$validator.reset()
    },

    add() {
      this.$validator.validateAll().then(() => {
        if (!this.$validator.errors.any()) {
          for (let i = 0; i < this.asset.asset_cpes.length; i++) {
            this.asset.asset_cpes[i].value = this.asset.asset_cpes[
              i
            ].value.replace('*', '%')
          }

          if (this.edit === true) {
            updateAsset(this.asset)
              .then(() => {
                this.$validator.reset()
                this.visible = false
                this.$root.$emit('notification', {
                  type: 'success',
                  loc: 'asset.successful_edit'
                })
              })
              .catch(() => {
                this.show_error = true
              })
          } else {
            createAsset(this.asset)
              .then(() => {
                this.$validator.reset()
                this.visible = false
                this.$root.$emit('notification', {
                  type: 'success',
                  loc: 'asset.successful'
                })
              })
              .catch(() => {
                this.show_error = true
              })
          }
        } else {
          this.show_validation_error = true
        }
      })
    },

    update(cpes) {
      this.asset.asset_cpes = cpes
    }
  },
  mounted() {}
}
</script>
