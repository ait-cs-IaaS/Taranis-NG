module.exports = {
  css: {
    loaderOptions: {
      scss: {
        additionalData: '@import "@/styles/variables.scss";'
      }
    }
  },
  configureWebpack: {
    devtool: 'source-map',
  },
  devServer: {
    allowedHosts: [
      'taranis'
    ]
  }
}
