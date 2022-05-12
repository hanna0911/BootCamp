const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: [
    'vuetify'
  ],
  publicPath: '/',
  outputDir: 'dist', //和编译结果输出路径有关，开发阶段不用管
  devServer: {
      open: true, //是否开启
      //host: 'https://frontend-wewritebugs.app.secoder.net',
      host: 'localhost', // 本地debug用
      port: '8080',
      proxy: {
        '/api': {
          //target: 'https://backend-wewritebugs.app.secoder.net', // 实际后端地址 
          target: 'http://localhost:8000', // 本地debug用
          ws: true,
          changeOrigin: true,
          pathRewrite: { //url转换
              '^/api': '/api'
          } 
        },
        '/files': {
          target: 'http://localhost:8000', // 本地debug用
          ws: true,
          changeOrigin: true,
          pathRewrite: { //url转换
              '^/files': '/files'
          } 
        },
      } 
  }
})
