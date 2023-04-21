<template>
  <v-container fluid>
    <iframe :src="iframeSrc" title="OpenAPI" class="openapi"></iframe>
  </v-container>
</template>

<script>
import { useStore } from 'vuex'

export default {
  name: 'OpenAPI',
  setup() {
    const store = useStore()
    const iframeSrc = store.state.coreAPIURL + '/doc'
    return { iframeSrc }
  }
}
</script>
