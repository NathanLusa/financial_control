/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./frontend/js/accounts_statment.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./frontend/js/accounts_statment.js":
/*!******************************************!*\
  !*** ./frontend/js/accounts_statment.js ***!
  \******************************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./utils */ \"./frontend/js/utils.js\");\n\n\nclass AccountStatment {\n\n  constructor(selected_month, selected_year, selected_accounts, description, setCookie) {\n    this.monthValue = selected_month\n    this.yearValue = selected_year\n    this.accountsValue = selected_accounts\n    this.descriptionValue = description\n    this.setCookie = setCookie\n  }\n\n  get initial_date() {\n    return new Date(this.yearValue, this.monthValue - 1, 1)\n  }\n\n  get finish_date() {\n    return new Date(this.yearValue, this.monthValue, 0)\n  }\n\n  get year() {\n    return this.yearValue\n  }\n\n  set year(year) {\n    this.yearValue = year\n    this.setCookie('year', this.yearValue, 1)\n  }\n\n  get month() {\n    return this.monthValue\n  }\n\n  set month(month) {\n    this.monthValue = month\n    this.setCookie('month', this.monthValue, 1)\n  }\n\n  get accounts() {\n    return this.accountsValue\n  }\n\n  set accounts(accounts) {\n    this.accountsValue = accounts\n    this.setCookie('accounts', this.accountsValue, 1)\n  }\n\n  get description() {\n    return this.descriptionValue\n  }\n\n  set description(description) {\n    this.descriptionValue = description\n    this.setCookie('description', this.descriptionValue, 1)\n  }\n\n  incMonth() {\n    this.monthValue = this.monthValue == 12 ? 1 : Number(this.monthValue) + 1\n    this.yearValue = this.monthValue == 1 ? Number(this.yearValue) + 1 : this.yearValue\n  }\n\n  decMonth() {\n    this.monthValue = this.monthValue == 1 ? 12 : Number(this.monthValue) - 1\n    this.yearValue = this.monthValue == 12 ? Number(this.yearValue) - 1 : this.yearValue\n  }\n}\n\nfunction setDashboardData(data) {\n  update(data.transactions, data.month_balances)\n\n  Object(_utils__WEBPACK_IMPORTED_MODULE_0__[\"setOnClickEvent\"])(\"table-item-link\", onClickNew);\n}\n\nfunction onClickCalendarNext(e) {\n  account_statment.incMonth();\n  calendar.value = Object(_utils__WEBPACK_IMPORTED_MODULE_0__[\"formatDate\"])(account_statment.initial_date, 'Y-m')\n  onClickFilter(e)\n}\n\nfunction onClickCalendarPrior(e) {\n  account_statment.decMonth();\n  calendar.value = Object(_utils__WEBPACK_IMPORTED_MODULE_0__[\"formatDate\"])(account_statment.initial_date, 'Y-m')\n  onClickFilter(e)\n}\n\nfunction onClickFilter(e) {\n  const date = calendar.value;\n\n  account_statment.year = date.split('-')[0]\n  account_statment.month = date.split('-')[1]\n  account_statment.accounts = getSelectedAccounts();\n  account_statment.description = filter_description.value;\n\n  filter(account_statment)\n}\n\nfunction filter(account_statment) {\n  const url = new URL('/api/accounts_statment', document.location)\n\n  url.search = new URLSearchParams({\n    accounts: account_statment.accounts,\n    initial_date: Object(_utils__WEBPACK_IMPORTED_MODULE_0__[\"formatDate\"])(account_statment.initial_date, 'Y-m-d'),\n    finish_date: Object(_utils__WEBPACK_IMPORTED_MODULE_0__[\"formatDate\"])(account_statment.finish_date, 'Y-m-d'),\n    description: account_statment.description,\n  })\n\n  fetch(url)\n    .then(_utils__WEBPACK_IMPORTED_MODULE_0__[\"handleErrors\"])\n    .then(response => response.json())\n    .then(data => setDashboardData(data))\n    .catch(err => console.log(err))\n}\n\nfunction onClickNew(e) {\n  const url = e.attributes[\"data-href\"].value\n  const title = e.attributes[\"data-modal-title\"].value\n\n  modal_title.innerHTML = title\n\n  fetch(url)\n    .then(response => response.text())\n    .then(body => modal_body.innerHTML = body)\n    .catch(err => console.log(err))\n}\n\nfunction amount_class(value) {\n  return value >= 0 ? 'positive' : 'negative'\n}\n\nfunction setAccountsSelected(accounts) {\n  accounts_input.forEach(input => {\n    input.checked = accounts.includes(input.getAttribute('id'))\n  });\n}\n\nfunction getSelectedAccounts() {\n  let accounts = []\n\n  accounts_input.forEach(input => {\n    if (input.checked) {\n      accounts.push(input.getAttribute('id'));\n    }\n  });\n\n  return accounts\n}\n\nfunction MonthBalanceTable(month_balances) {\n  const head = `<thead>\n                  <th>Account</th>\n                  <th>Income</th>\n                  <th>Expense</th>\n                  <th>Balance</th>\n                  <th>Total</th>\n                </thead>`;\n  const body = month_balances.map(month_balance => MonthBalanceItem(month_balance)).join('');\n  return head + body\n}\n\nfunction MonthBalanceItem(month_balance) {\n  const amount = parseFloat(month_balance.amount)\n  const income = parseFloat(month_balance.income_value)\n  const expense = parseFloat(month_balance.expense_value)\n  const accumulated = parseFloat(month_balance.accumulated)\n\n  return `<tr>\n            <th scope=\"row\">\n              <h5>\n                <span class=\"badge badge-${month_balance.account.color.toLowerCase()}\">${month_balance.account.description}</span>\n                </h5>\n            </th>\n            <td class=\"amount ${amount_class(income)}\">R$ ${income.toFixed(2)}</td>\n            <td class=\"amount ${amount_class(expense)}\">R$ ${expense.toFixed(2)}</td>\n            <td class=\"amount ${amount_class(amount)}\">R$ ${amount.toFixed(2)}</td>\n            <td class=\"amount ${amount_class(accumulated)}\">R$ ${accumulated.toFixed(2)}</td>\n          </tr>`;\n}\n\nfunction TransactionTable(month_balance, transactions) {\n  var total = 0;\n  const f_accumulate = (value) => total += value;\n\n  const initial_amount = month_balance\n    .filter(month => month.prev_amount != 0)\n    .map(month => {\n      return {\n        id: '#',\n        url: '#',\n        account: {\n          description: month.account.description,\n          color: month.account.color\n        },\n        date: month.date,\n        description: 'Initial amount',\n        value: month.prev_amount\n      }\n    });\n\n  return initial_amount.map(transaction => TransactionItem(transaction, f_accumulate)).join('') +\n    transactions.map(transaction => TransactionItem(transaction, f_accumulate)).join('');\n}\n\nfunction TransactionItem(transaction, f_accumulate) {\n  const amount = parseFloat(transaction.value);\n  const total = f_accumulate(amount);\n\n  return `\n    <tr ${transaction.id > 0 ? 'class=\"table-item-link\" data-toggle=\"modal\"' : ''}\n        data-target=\"#modal-dashboard\" \n        data-href=\"${transaction.url}\" \n        data-modal-title=\"Transaction\" \n        data-transaction-id=\"${transaction.id}\">\n      <th scope=\"row\" class=\"date\">${transaction.date}</th>\n      <td>\n        ${transaction.description} <br>\n        <span class=\"badge badge-${transaction.account.color.toLowerCase()}\">${transaction.account.description}</span>\n        ${transaction.category ? '<span class=\"badge badge-secondary\">' + transaction.category + '</span>' : ''}\n        ${transaction.status ? '<span class=\"badge badge-' + transaction.status_color + '\">' + transaction.status + '</span>' : ''}\n      </td>\n      <td class=\"amount bold ${amount_class(amount)}\">R$ ${amount.toFixed(2)}</td>\n      <td class=\"amount ${amount_class(total)}\">R$ ${total.toFixed(2)}</td>\n    </tr>\n  `\n}\n\nfunction update(transactions, month_balances) {\n  const table_transactions = document.getElementById(\"table-transactions\");\n  const table_month_balances = document.getElementById(\"table-month-balances\");\n\n  table_transactions.innerHTML = TransactionTable(month_balances, transactions)\n  table_month_balances.innerHTML = MonthBalanceTable(month_balances)\n}\n\nfunction get_account_statment_main() {\n  const date_now = new Date();\n  var selected_year = date_now.getFullYear();\n  var selected_month = date_now.getMonth();\n  var selected_accounts = getSelectedAccounts();\n\n  const cookie_selected_year = Object(_utils__WEBPACK_IMPORTED_MODULE_0__[\"getCookie\"])('year')\n  const cookie_selected_month = Object(_utils__WEBPACK_IMPORTED_MODULE_0__[\"getCookie\"])('month')\n  const cookie_selected_accounts = Object(_utils__WEBPACK_IMPORTED_MODULE_0__[\"getCookie\"])('accounts')\n  const cookie_selected_description = Object(_utils__WEBPACK_IMPORTED_MODULE_0__[\"getCookie\"])('description')\n\n  if (cookie_selected_year != \"\") {\n    selected_year = cookie_selected_year\n  };\n  if (cookie_selected_month != \"\") {\n    selected_month = cookie_selected_month\n  };\n  if (cookie_selected_accounts != \"\") {\n    selected_accounts = cookie_selected_accounts\n  };\n\n  return new AccountStatment(selected_month, selected_year, selected_accounts, cookie_selected_description, _utils__WEBPACK_IMPORTED_MODULE_0__[\"setCookie\"])\n}\n\nfunction setEvents() {\n  accounts_input.forEach(input => Object(_utils__WEBPACK_IMPORTED_MODULE_0__[\"addListener\"])(input, 'click', () => onClickFilter(input)));\n\n  Object(_utils__WEBPACK_IMPORTED_MODULE_0__[\"addListener\"])(calendar, 'change', () => onClickFilter(calendar));\n\n  const calendar_prior = document.querySelector('.filter #calendar-prior')\n  Object(_utils__WEBPACK_IMPORTED_MODULE_0__[\"addListener\"])(calendar_prior, 'click', () => onClickCalendarPrior(calendar_prior));\n\n  const calendar_next = document.querySelector('.filter #calendar-next')\n  Object(_utils__WEBPACK_IMPORTED_MODULE_0__[\"addListener\"])(calendar_next, 'click', () => onClickCalendarNext(calendar_next));\n\n  const button_search = document.querySelector('#filter-description-button')\n  Object(_utils__WEBPACK_IMPORTED_MODULE_0__[\"addListener\"])(button_search, 'click', () => onClickFilter(button_search));\n\n  const buttonNewTransaction = document.getElementById(\"button-new-transaction\");\n  Object(_utils__WEBPACK_IMPORTED_MODULE_0__[\"addListener\"])(buttonNewTransaction, 'click', () => onClickNew(buttonNewTransaction));\n\n  const buttonNewTransfer = document.getElementById(\"button-new-transfer\");\n  Object(_utils__WEBPACK_IMPORTED_MODULE_0__[\"addListener\"])(buttonNewTransfer, 'click', () => onClickNew(buttonNewTransfer));\n\n  // const buttonSearch = document.getElementById(\"filter-description-button\");\n  // addListener(buttonSearch, 'click', () => onClickFilter(buttonSearch));\n};\n\nfunction setDefaults() {\n  calendar.value = Object(_utils__WEBPACK_IMPORTED_MODULE_0__[\"formatDate\"])(account_statment.initial_date, 'Y-m');\n  filter_description.value = account_statment.description\n  setAccountsSelected(account_statment.accounts)\n}\n\nconst accounts_input = document.querySelector('#accounts').querySelectorAll('input');\nconst account_statment = get_account_statment_main();\nconst modal_dashboard = document.getElementById(\"modal-dashboard\")\nconst modal_title = modal_dashboard.querySelector(\".modal-title\")\nconst modal_body = modal_dashboard.querySelector(\".modal-body\")\nconst calendar = document.querySelector('.filter #calendar')\nconst filter_description = document.querySelector('#filter-description')\n\nwindow.onload = () => {\n  setDefaults();\n  setEvents();\n\n  filter(account_statment);\n}\n\n//# sourceURL=webpack:///./frontend/js/accounts_statment.js?");

/***/ }),

/***/ "./frontend/js/utils.js":
/*!******************************!*\
  !*** ./frontend/js/utils.js ***!
  \******************************/
/*! exports provided: addListener, setOnClickEvent, handleErrors, range, setCookie, getCookie, openDataHref, formatDate */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"addListener\", function() { return addListener; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"setOnClickEvent\", function() { return setOnClickEvent; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"handleErrors\", function() { return handleErrors; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"range\", function() { return range; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"setCookie\", function() { return setCookie; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"getCookie\", function() { return getCookie; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"openDataHref\", function() { return openDataHref; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"formatDate\", function() { return formatDate; });\nfunction addListener(element, eventName, handler) {\n  if (element.addEventListener) {\n    element.addEventListener(eventName, handler, false);\n  } else if (element.attachEvent) {\n    element.attachEvent('on' + eventName, handler);\n  } else {\n    element['on' + eventName] = handler;\n  }\n}\n\nfunction setOnClickEvent(class_name, on_click_event) {\n  const list = document.getElementsByClassName(class_name);\n\n  if (on_click_event) {\n    for (const key in list) {\n      if (list.hasOwnProperty(key)) {\n        const element = list[key];\n        addListener(element, 'click', () => on_click_event(element));\n      }\n    }\n  }\n}\n\nfunction handleErrors(response) {\n  if (!response.ok) {\n    console.log('Deu ruim');\n    response.json()\n      .then(data => alert(data.message))\n      .then(data => {\n        throw Error(data.message)\n      })\n\n  }\n  return response;\n}\n\nfunction range(size, startAt = 0) {\n  return [...Array(size).keys()].map(i => i + startAt);\n}\n\nfunction setCookie(cname, cvalue, exdays) {\n  var d = new Date();\n  d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));\n  var expires = \"expires=\" + d.toUTCString();\n  document.cookie = cname + \"=\" + cvalue + \";\" + expires + \";path=/\";\n}\n\nfunction getCookie(cname) {\n  var name = cname + \"=\";\n  var decodedCookie = decodeURIComponent(document.cookie);\n  var ca = decodedCookie.split(';');\n  for (var i = 0; i < ca.length; i++) {\n    var c = ca[i];\n    while (c.charAt(0) == ' ') {\n      c = c.substring(1);\n    }\n    if (c.indexOf(name) == 0) {\n      return c.substring(name.length, c.length);\n    }\n  }\n  return \"\";\n}\n\nfunction openDataHref(e) {\n  const data_href = e.getAttribute('data-href')\n\n  if (data_href) {\n    window.open(data_href, \"_self\")\n  }\n}\n\nfunction formatDate(dateObj, frmt) {\n  var pad = function (number) {\n    return (\"0\" + number).slice(-2);\n  };\n  var formats = {\n    // get the date in UTC\n    Z: function (date) {\n      return date.toISOString();\n    },\n    // weekday name, short, e.g. Thu\n    D: function (date, locale, options) {\n      return locale.weekdays.shorthand[formats.w(date, locale, options)];\n    },\n    // full month name e.g. January\n    F: function (date, locale, options) {\n      return monthToStr(formats.n(date, locale, options) - 1, false, locale);\n    },\n    // padded hour 1-12\n    G: function (date, locale, options) {\n      return pad(formats.h(date, locale, options));\n    },\n    // hours with leading zero e.g. 03\n    H: function (date) {\n      return pad(date.getHours());\n    },\n    // day (1-30) with ordinal suffix e.g. 1st, 2nd\n    J: function (date, locale) {\n      return locale.ordinal !== undefined ?\n        date.getDate() + locale.ordinal(date.getDate()) :\n        date.getDate();\n    },\n    // AM/PM\n    K: function (date, locale) {\n      return locale.amPM[int(date.getHours() > 11)];\n    },\n    // shorthand month e.g. Jan, Sep, Oct, etc\n    M: function (date, locale) {\n      return monthToStr(date.getMonth(), true, locale);\n    },\n    // seconds 00-59\n    S: function (date) {\n      return pad(date.getSeconds());\n    },\n    // unix timestamp\n    U: function (date) {\n      return date.getTime() / 1000;\n    },\n    W: function (date, _, options) {\n      return options.getWeek(date);\n    },\n    // full year e.g. 2016\n    Y: function (date) {\n      return date.getFullYear();\n    },\n    // day in month, padded (01-30)\n    d: function (date) {\n      return pad(date.getDate());\n    },\n    // hour from 1-12 (am/pm)\n    h: function (date) {\n      return (date.getHours() % 12 ? date.getHours() % 12 : 12);\n    },\n    // minutes, padded with leading zero e.g. 09\n    i: function (date) {\n      return pad(date.getMinutes());\n    },\n    // day in month (1-30)\n    j: function (date) {\n      return date.getDate();\n    },\n    // weekday name, full, e.g. Thursday\n    l: function (date, locale) {\n      return locale.weekdays.longhand[date.getDay()];\n    },\n    // padded month number (01-12)\n    m: function (date) {\n      return pad(date.getMonth() + 1);\n    },\n    // the month number (1-12)\n    n: function (date) {\n      return date.getMonth() + 1;\n    },\n    // seconds 0-59\n    s: function (date) {\n      return date.getSeconds();\n    },\n    // Unix Milliseconds\n    u: function (date) {\n      return date.getTime();\n    },\n    // number of the day of the week\n    w: function (date) {\n      return date.getDay();\n    },\n    // last two digits of year e.g. 16 for 2016\n    y: function (date) {\n      return String(date.getFullYear()).substring(2);\n    }\n  };\n  // var locale = overrideLocale || l10n;\n  // if (config.formatDate !== undefined) {\n  //     return config.formatDate(dateObj, frmt, locale);\n  // }\n  return frmt\n    .split(\"\")\n    .map(function (c, i, arr) {\n      return formats[c] && arr[i - 1] !== \"\\\\\" ?\n        formats[c](dateObj)\n        // ? formats[c](dateObj, locale, config)\n        :\n        c !== \"\\\\\" ?\n        c :\n        \"\";\n    })\n    .join(\"\");\n};\n\n\n\n\n//# sourceURL=webpack:///./frontend/js/utils.js?");

/***/ })

/******/ });