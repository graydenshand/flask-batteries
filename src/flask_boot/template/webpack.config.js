const path = require('path');
const CopyPlugin = require("copy-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
  
module.exports = {
  mode: 'development',
  context: path.resolve(__dirname, 'src'),
  entry: [
    "./assets/javascript/index.js",
    "./assets/stylesheets/styles.scss",
  ],
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'src/static'),
    publicPath: "/static",
    clean: true
  },
  module: {
    rules: [
      {
        test: /\.((s[ac])|c)ss$/i,
        use: [MiniCssExtractPlugin.loader, "css-loader", "sass-loader"],
      },
    ],
  },
  plugins: [
    new CopyPlugin({
      patterns: [
        { from: "assets/images", to: "images"}
      ]
    }),
    new MiniCssExtractPlugin(),
  ],
  devServer: {
    contentBase: path.join(__dirname, "src/static"),
    compress: true,
    port: 3000
  }
};