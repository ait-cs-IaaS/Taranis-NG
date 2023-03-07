<template>
  <asset
    v-if="asset"
    :asset_prop="asset"
    :edit.sync="edit"
    @assetcreated="assetcreated"
  />
</template>

<script>
import { getAsset } from '@/api/assets'
import { notifySuccess } from '@/utils/helpers'
import Asset from '@/components/assets/Asset'

export default {
  name: 'Asset',
  data: () => ({
    default_asset: {
      id: -1,
      name: '',
      serial: '',
      description: '',
      asset_cpes: [],
      asset_group_id: ''
    },
    asset: undefined,
    edit: true
  }),
  components: {
    Asset
  },
  mounted() {
    this.asset = this.default_asset
  },
  async created() {
    this.asset = await this.loadAsset()
    if (this.asset === undefined) {
      this.asset = this.default_asset
      this.edit = false
    }
  },
  methods: {
    async loadAsset() {
      if (this.$route.params.id && this.$route.params.id !== '0') {
        return await getAsset(this.$route.params.id).then((response) => {
          return response.data
        })
      }
    },
    assetcreated(asset) {
      notifySuccess(`Asset with ID ${asset} created`)
      this.edit = true
    }
  }
}
</script>
