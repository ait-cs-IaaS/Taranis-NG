const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  chainWebpack: (config) => {
    config.resolve.alias.set('vue', '@vue/compat')

    config.module
      .rule('vue')
      .use('vue-loader')
      .tap((options) => {
        return {
          ...options,
          compilerOptions: {
            compatConfig: {
              MODE: 2
            }
          }
        }
      })
  },
  configureWebpack: {
    devtool: 'source-map',
  },
  devServer: {
    allowedHosts: [
      'taranis'
    ]
  }
})
