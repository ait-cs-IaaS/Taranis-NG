<template>
  <v-data-table
    v-model="selected_word_lists"
    :headers="headers"
    :items="word_lists.items"
    show-select
  >
    <template #top>
      <v-toolbar color="white">
        <v-toolbar-title>
          {{ $t('osint_source.word_lists') }}
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn color="green" dark variant="outlined" @click="save">
          {{ $t('button.save') }}
        </v-btn>
      </v-toolbar>
    </template>
  </v-data-table>
</template>

<script>
import { useConfigStore } from '@/stores/ConfigStore'
import { useSettingsStore } from '@/stores/SettingsStore'
import { storeToRefs } from 'pinia'
import { onMounted } from 'vue'

export default {
  name: 'UserWordListsView',
  setup() {
    const configStore = useConfigStore()
    const settingsStore = useSettingsStore()

    const headers = [
      {
        title: 'Name',
        align: 'start',
        key: 'name'
      },
      { title: 'Description', key: 'description' }
    ]

    const save = () => {
      settingsStore.saveWordLists(selected_word_lists.value)
    }

    const { word_lists } = storeToRefs(configStore)
    const { word_lists: selected_word_lists } = storeToRefs(settingsStore)

    onMounted(() => {
      configStore.loadWordLists()
    })

    return {
      headers,
      save,
      word_lists,
      selected_word_lists
    }
  }
}
</script>
