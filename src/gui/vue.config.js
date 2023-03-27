const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  configureWebpack: {
    devtool: 'source-map',
  },
  devServer: {
    allowedHosts: [
      'taranis'
    ]
  }
})
