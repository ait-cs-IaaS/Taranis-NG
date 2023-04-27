<template>
  <v-container fluid>
    <iframe :src="iframeSrc" title="OpenAPI" class="openapi"></iframe>
  </v-container>
</template>

<script>
import { useMainStore } from '@/stores/MainStore'

export default {
  name: 'OpenAPI',
  setup() {
    const store = useMainStore()
    const iframeSrc = store.coreAPIURL + '/doc'
    return { iframeSrc }
  }
}
</script>
