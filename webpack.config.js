const path = require('path');

module.exports = {
  mode: "development",
  entry: {
    app: './frontend/index.js',
    accounts_statment: './frontend/js/accounts_statment'
  },
  output: {
    filename: 'js/[name].js',
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