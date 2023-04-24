<template>
  <v-container>
    <v-row>
      <v-col :class="UI.CLASS.card_offset">
        <v-hover v-slot="{ hover }">
          <v-card :elevation="hover ? 12 : 2" @click.stop="cardItemToolbar">
            <v-layout class="status">
              <v-row>
                <v-col :style="UI.STYLE.card_tag">
                  <v-icon center>{{ card.tag }}</v-icon>
                </v-col>
                <v-col>
                  <div class="grey--text">{{ $t('card_item.title') }}</div>
                  <span>{{ card.title }}</span>
                </v-col>
                <v-col>
                  <div class="grey--text">
                    {{ $t('card_item.description') }}
                  </div>
                  <span>{{ card.subtitle }}</span>
                </v-col>
              </v-row>
            </v-layout>
          </v-card>
        </v-hover>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'CardProduct',
  props: {
    card: {
      type: Object,
      required: true
    }
  },
  data: () => ({
    toolbar: false
  }),
  methods: {
    itemClicked(data) {
      this.$root.$emit('show-product-edit', data)
    },
    deleteClicked(data) {
      this.$root.$emit('delete-product', data)
    },
    cardItemToolbar(action) {
      switch (action) {
        case 'edit':
          break

        case 'delete':
          this.deleteClicked(this.card)
          break

        default:
          this.toolbar = false
          this.itemClicked(this.card)
          break
      }
    }
  }
}
</script>
