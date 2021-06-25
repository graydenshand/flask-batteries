const path = require('path');
  
module.exports = {
  mode: 'development',
  context: path.resolve(__dirname, 'src'),
  entry: [
    "./assets/javascript/index.js",
  ],
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'src/static'),
  },
  module: {
    rules: [
      {
        test: /\.((s[ac])|c)ss$/i,
        use: [
          // Creates `style` nodes from JS strings
          "style-loader",
          // Translates CSS into CommonJS
          "css-loader",
          // Compiles Sass to CSS
          "sass-loader"
        ],
      },
    ],
  },
  devServer: {
    contentBase: path.join(__dirname, "src/static"),
    compress: true,
    port: 3000
  }
};