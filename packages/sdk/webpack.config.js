const path = require('path');
const TerserPlugin = require('terser-webpack-plugin');

module.exports = {
  entry: './src/index.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'ad-scouter-sdk.js',
    library: 'adScouter',
    libraryTarget: 'umd',
    globalObject: 'this',
    clean: true
  },
  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          compress: {
            drop_console: false, // 디버깅을 위해 console.log 유지
            drop_debugger: true,
          },
          mangle: {
            reserved: ['adScouter'] // 전역 변수명 보호
          }
        }
      })
    ]
  },
  mode: 'production',
  target: 'web',
  resolve: {
    extensions: ['.js']
  }
};
