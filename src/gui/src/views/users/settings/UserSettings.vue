<template>
  <v-container fluid>
    <v-card variant="outlined">
      <v-card-title>
        <v-toolbar>
          <v-toolbar-title>
            {{ $t('settings.user_settings') }}
          </v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn
            color="success"
            variant="outlined"
            prepend-icon="mdi-content-save"
            @click="save()"
          >
            {{ $t('settings.save') }}
          </v-btn>
        </v-toolbar>
      </v-card-title>
      <v-card-text>
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
        <h1 class="mt-5 mb-5">Hotkeys</h1>
        <v-row no-gutters class="ma-0">
          <v-tooltip v-for="shortcut in hotkeys" :key="shortcut.alias">
            <template #activator="{ props }">
              <v-btn
                :id="shortcut.alias"
                v-bind="props"
                class="blue lighten-5 ma-1"
                style="width: calc(100% / 3 - 8px)"
                :prepend-icon="shortcut.icon"
                @click.stop="pressKeyDialog(shortcut.alias)"
                @blur="pressKeyVisible = false"
              >
                <span v-if="shortcut.key">
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
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import { useSettingsStore } from '@/stores/SettingsStore'
import { mapActions, mapState, mapWritableState } from 'pinia'
import { useConfigStore } from '@/stores/ConfigStore'

export default {
  name: 'UserSettings',
  data: () => ({
    pressKeyVisible: false,
    shortcuts: [],
    tab: 'general',
    hotkeyAlias: String
  }),
  computed: {
    browser_locale: {
      get() {
        return this.getProfileBrowserLocale
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
    },
    ...mapWritableState(useSettingsStore, [
      'getProfileBrowserLocale',
      'dark_theme',
      'spellcheck',
      'hotkeys'
    ]),
    ...mapState(useConfigStore, ['setLocale'])
  },
  methods: {
    ...mapActions(useSettingsStore, ['saveUserProfile']),
    save() {
      this.saveUserProfile({
        spellcheck: this.spellcheck,
        dark_theme: this.dark_theme,
        hotkeys: this.hotkeys,
        language: this.browser_locale
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

    pressKey(event) {
      const key = event
      const hotkeyIndex = this.hotkeys
        .map(function (e) {
          return e.alias
        })
        .indexOf(this.hotkeyAlias)

      window.removeEventListener('keydown', this.pressKey)

      this.pressKeyVisible = false

      // check doubles and clear
      // TODO: FIX
      this.shortcuts.forEach((doubleKey, i) => {
        if (doubleKey.key_code === key.keyCode && i !== hotkeyIndex) {
          this.shortcuts[i].key_code = 0
          this.shortcuts[i].key = 'undefined'
        }
      })

      // assigned new key
      this.hotkeys[hotkeyIndex].key_code = key.keyCode
      this.hotkeys[hotkeyIndex].key = key.code
    }
  }
}
</script>
