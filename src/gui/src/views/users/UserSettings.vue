<template>
  <v-container fluid>
    <v-card variant="outlined">
      <v-card-item>
        <h1>{{ $t('settings.user_settings') }}</h1>
        <v-spacer></v-spacer>
        <v-btn color="success" @click="save()">
          <v-icon left>mdi-content-save</v-icon>
          <span>{{ $t('settings.save') }}</span>
        </v-btn>
      </v-card-item>
      <v-card-text>
        <v-tabs v-model="tab" fixed-tabs density="compact">
          <v-tab value="general">
            <span>{{ $t('settings.tab_general') }}</span>
          </v-tab>
          <v-tab value="wordlist">
            <span>{{ $t('settings.tab_wordlists') }}</span>
          </v-tab>
          <v-tab value="hotkeys">
            <span>{{ $t('settings.tab_hotkeys') }}</span>
          </v-tab>
        </v-tabs>
        <v-window v-model="tab">
          <v-window-item value="general">
            <v-row justify="center" align="center">
              <v-col>
                <v-switch
                  v-model="spellcheck"
                  :label="$t('settings.spellcheck')"
                ></v-switch>
              </v-col>
              <v-col>
                <v-switch
                  v-model="dark_theme"
                  :label="$t('settings.dark_theme')"
                  @change="darkToggle"
                ></v-switch>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="4">
                <v-autocomplete
                  v-model="browser_locale"
                  :items="locale_descriptions"
                  :item-title="(item) => item.value + ' - ' + item.text"
                  hint="Select your locale"
                  :label="$t('settings.locale')"
                  solo
                  persistent-hint
                ></v-autocomplete>
              </v-col>
            </v-row>
          </v-window-item>
          <v-window-item value="wordlist">
            <v-data-table
              v-model="selected_word_lists"
              :headers="headers"
              :items="word_lists"
              item-value="id"
              show-select
            >
              <template #top>
                <v-toolbar flat color="white">
                  <v-toolbar-title>
                    {{ $t('osint_source.word_lists') }}
                  </v-toolbar-title>
                </v-toolbar>
              </template>
            </v-data-table>
          </v-window-item>
          <v-window-item value="hotkeys">
            <v-row no-gutters class="ma-0">
              <v-tooltip
                v-for="shortcut in shortcuts"
                :key="shortcut.alias"
                top
              >
                <template #activator="{ props }">
                  <v-btn
                    :id="shortcut.alias"
                    v-bind="props"
                    class="blue lighten-5 ma-1"
                    style="width: calc(100% / 3 - 8px)"
                    text
                    @click.stop="pressKeyDialog(shortcut.alias)"
                    @blur="pressKeyVisible = false"
                  >
                    <v-icon left>{{ shortcut.icon }}</v-icon>
                    <span v-if="shortcut.key != 'undefined'" class="caption">
                      {{ shortcut.key }}
                    </span>
                    <v-icon v-else color="error">mdi-alert</v-icon>
                  </v-btn>
                </template>
                <span>
                  {{ $t('settings.' + shortcut.alias) }}
                </span>
              </v-tooltip>
            </v-row>
          </v-window-item>
        </v-window>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'UserSettings',
  data: () => ({
    dark_theme: false,
    spellcheck: null,
    pressKeyVisible: false,
    shortcuts: [],
    tab: 'general',
    hotkeyAlias: String,
    headers: [
      {
        text: 'Name',
        align: 'start',
        value: 'name'
      },
      { text: 'Description', value: 'description' }
    ],
    word_lists: [],
    selected_word_lists: []
  }),
  computed: {
    browser_locale: {
      get() {
        return this.getProfileBrowserLocale()
      },
      set(value) {
        this.$i18n.locale = value
        this.setLocale(value)
        console.warn('TODO: extend user profile to include locale')
        // TODO: extend user profile to include locale
        // this.saveUserProfile({ browser_locale: value })
      }
    },
    locale_descriptions() {
      return [
        { value: 'en', text: 'English' },
        { value: 'de', text: 'Deutsch' },
        { value: 'sk', text: 'Slovensky' }
      ]
    }
  },
  mounted() {
    this.spellcheck = this.getProfileSpellcheck()
    this.dark_theme = this.getProfileDarkTheme()
    this.selected_word_lists = this.getProfileWordLists()
    this.shortcuts = this.getProfileHotkeys()
    this.loadWordList()
  },
  methods: {
    ...mapGetters('settings', [
      'getProfileSpellcheck',
      'getProfileDarkTheme',
      'getProfileHotkeys',
      'getProfileWordLists',
      'getProfileBrowserLocale'
    ]),
    ...mapActions('settings', ['saveUserProfile', 'setLocale']),
    ...mapActions('config', ['loadWordLists']),
    ...mapGetters('config', ['getWordLists']),
    save() {
      this.saveUserProfile({
        spellcheck: this.spellcheck,
        dark_theme: this.dark_theme,
        hotkeys: this.shortcuts,
        word_lists: this.selected_word_lists
      })
    },

    darkToggle() {
      this.$vuetify.theme.dark = this.dark_theme
    },

    pressKeyDialog(event) {
      window.addEventListener('keydown', this.pressKey, false)

      this.pressKeyVisible = true
      this.hotkeyAlias = event
    },

    loadWordList() {
      this.loadWordLists().then(() => {
        this.word_lists = this.getWordLists().items
      })
    },

    pressKey(event) {
      const key = event
      const hotkeyIndex = this.shortcuts
        .map(function (e) {
          return e.alias
        })
        .indexOf(this.hotkeyAlias)

      window.removeEventListener('keydown', this.pressKey)

      this.pressKeyVisible = false

      // check doubles and clear
      this.shortcuts.forEach((doubleKey, i) => {
        if (doubleKey.key_code === key.keyCode && i !== hotkeyIndex) {
          this.shortcuts[i].key_code = 0
          this.shortcuts[i].key = 'undefined'
        }
      })

      // assigned new key
      this.shortcuts[hotkeyIndex].key_code = key.keyCode
      this.shortcuts[hotkeyIndex].key = key.code
    }
  }
}
</script>
