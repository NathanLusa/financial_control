const path = require('path');

module.exports = {
  mode: "development",
  entry: ['./frontend/index.js'],
  output: {
    filename: 'js/bundle.js',
    path: path.resolve(__dirname, 'financial_control/static')
  },
  module: {
    rules: [{
        test: /\.(scss)$/,
        use: [{
            loader: 'file-loader',
            options: {
              name: 'css/[name].css',
            }
          },
          {
            loader: 'extract-loader'
          },
          {
            loader: 'css-loader?-url'
          },
          {
            loader: 'postcss-loader'
          },
          {
            loader: 'sass-loader'
          }
        ]
      },
      {
        test: /fa-.*\.(woff2|woff|eot|svg|ttf)$/,
        use: [{
          loader: 'file-loader',
          options: {
            name: 'webfonts/[name].[ext]',
          }
        }]
      }
    ]
  }
};