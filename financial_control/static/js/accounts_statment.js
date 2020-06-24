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
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./utils */ \"./frontend/js/utils.js\");\n\n\nclass AccountStatment {\n\n  constructor(selected_month, selected_year, selected_accounts, description, setCookie) {\n    this.monthValue = selected_month\n    this.yearValue = selected_year\n    this.accountsValue = selected_accounts\n    this.descriptionValue = description\n    this.setCookie = setCookie\n  }\n\n  get initial_date() {\n    return new Date(this.yearValue, this.monthValue - 1, 1)\n  }\n\n  get finish_date() {\n    return new Date(this.yearValue, this.monthValue, 0)\n  }\n\n  get year() {\n    return this.yearValue\n  }\n\n  set year(year) {\n    this.yearValue = year\n    this.setCookie('year', this.yearValue, 1)\n  }\n\n  get month() {\n    return this.monthValue\n  }\n\n  set month(month) {\n    this.monthValue = month\n    this.setCookie('month', this.monthValue, 1)\n  }\n\n  get accounts() {\n    return this.accountsValue\n  }\n\n  set accounts(accounts) {\n    this.accountsValue = accounts\n    this.setCookie('accounts', this.accountsValue, 1)\n  }\n\n  get description() {\n    return this.descriptionValue\n  }\n\n  set description(description) {\n    this.descriptionValue = description\n  }\n}\n\nfunction setDashboardData(data) {\n  update(data.transactions, data.month_balances)\n\n  Object(_utils__WEBPACK_IMPORTED_MODULE_0__[\"setOnClickEvent\"])(\"table-item-link\", onClickNew);\n}\n\nfunction onClickFilter(e) {\n  account_statment.year = document.querySelector('#filter-year').querySelector('label.active').querySelector('input').getAttribute('data-year');\n  account_statment.month = document.querySelector('#filter-month').querySelector('label.active').querySelector('input').getAttribute('data-month');\n  account_statment.accounts = getSelectedAccounts();\n  account_statment.description = document.querySelector('#filter-description').value;\n\n  filter(account_statment)\n}\n\nfunction onClickFilterDropdown(e) {\n  if (e) {\n    const filter = e.parentElement.getAttribute('aria-labelledby')\n    account_statment.year = filter == 'filter-year' ? e.getAttribute('id') : account_statment.year;\n    account_statment.month = filter == 'filter-month' ? e.getAttribute('id') : account_statment.month;\n  }\n\n  document.querySelector('#filter').querySelector('button#filter-year').innerHTML = account_statment.year;\n  document.querySelector('#filter').querySelector('button#filter-month').innerHTML = account_statment.month;\n\n  filter(account_statment)\n}\n\nfunction filter(account_statment) {\n  const url = new URL('/api/accounts_statment', document.location)\n\n  url.search = new URLSearchParams({\n    accounts: account_statment.accounts,\n    initial_date: Object(_utils__WEBPACK_IMPORTED_MODULE_0__[\"dateToString\"])(account_statment.initial_date),\n    finish_date: Object(_utils__WEBPACK_IMPORTED_MODULE_0__[\"dateToString\"])(account_statment.finish_date),\n    description: account_statment.description,\n  })\n\n  fetch(url)\n    .then(_utils__WEBPACK_IMPORTED_MODULE_0__[\"handleErrors\"])\n    .then(response => response.json())\n    .then(data => setDashboardData(data))\n    .catch(err => console.log(err))\n}\n\nfunction onClickNew(e) {\n  const url = e.attributes[\"data-href\"].value\n  const title = e.attributes[\"data-modal-title\"].value\n\n  modal_title.innerHTML = title\n\n  fetch(url)\n    .then(response => response.text())\n    .then(body => modal_body.innerHTML = body)\n    .catch(err => console.log(err))\n}\n\nfunction amount_class(value) {\n  return value >= 0 ? 'positive' : 'negative'\n}\n\nfunction setAccountsSelected(accounts) {\n  accounts_input.forEach(input => {\n    input.checked = accounts.includes(input.getAttribute('id'))\n  });\n\n\n}\n\nfunction getSelectedAccounts() {\n  let accounts = []\n\n  accounts_input.forEach(input => {\n    if (input.checked) {\n      accounts.push(input.getAttribute('id'));\n    }\n  });\n\n  return accounts\n}\n\nfunction MonthBalanceTable(month_balances) {\n  const head = `<thead>\n                  <th>Account</th>\n                  <th>Income</th>\n                  <th>Expense</th>\n                  <th>Balance</th>\n                  <th>Total</th>\n                </thead>`;\n  const body = month_balances.map(month_balance => MonthBalanceItem(month_balance)).join('');\n  return head + body\n}\n\nfunction MonthBalanceItem(month_balance) {\n  const amount = parseFloat(month_balance.amount)\n  const income = parseFloat(month_balance.income_value)\n  const expense = parseFloat(month_balance.expense_value)\n  const accumulated = parseFloat(month_balance.accumulated)\n\n  return `<tr>\n            <th scope=\"row\">${month_balance.account}</th>\n            <td class=\"amount ${amount_class(income)}\">R$ ${income.toFixed(2)}</td>\n            <td class=\"amount ${amount_class(expense)}\">R$ ${expense.toFixed(2)}</td>\n            <td class=\"amount ${amount_class(amount)}\">R$ ${amount.toFixed(2)}</td>\n            <td class=\"amount ${amount_class(accumulated)}\">R$ ${accumulated.toFixed(2)}</td>\n          </tr>`;\n}\n\nfunction TransactionTable(transactions) {\n  var total = 0;\n  const f_accumulate = (value) => total += value;\n\n  return transactions.map(transaction => TransactionItem(transaction, f_accumulate)).join('');\n}\n\nfunction TransactionItem(transaction, f_accumulate) {\n  const amount = parseFloat(transaction.value);\n  const total = f_accumulate(amount);\n\n  return `\n    <tr class=\"table-item-link\" data-toggle=\"modal\" data-target=\"#modal-dashboard\" data-href=\"${transaction.url}\" data-modal-title=\"Transaction\" data-transaction-id=\"${transaction.id}\">\n      <th scope=\"row\" class=\"date\">${transaction.date}</th>\n      <td>${transaction.description}</td>\n      <td class=\"amount bold ${amount_class(amount)}\">R$ ${amount.toFixed(2)}</td>\n      <td class=\"amount ${amount_class(total)}\">R$ ${total.toFixed(2)}</td>\n    </tr>\n  `\n}\n\nfunction update(transactions, month_balances) {\n  const table_transactions = document.getElementById(\"table-transactions\");\n  const table_month_balances = document.getElementById(\"table-month-balances\");\n\n  table_transactions.innerHTML = TransactionTable(transactions)\n  table_month_balances.innerHTML = MonthBalanceTable(month_balances)\n}\n\nfunction get_account_statment_main() {\n  const date_now = new Date();\n  var selected_year = date_now.getFullYear();\n  var selected_month = date_now.getMonth();\n  var selected_accounts = getSelectedAccounts();\n\n  const cookie_selected_year = Object(_utils__WEBPACK_IMPORTED_MODULE_0__[\"getCookie\"])('year')\n  const cookie_selected_month = Object(_utils__WEBPACK_IMPORTED_MODULE_0__[\"getCookie\"])('month')\n  const cookie_selected_accounts = Object(_utils__WEBPACK_IMPORTED_MODULE_0__[\"getCookie\"])('accounts')\n\n  if (cookie_selected_year != \"\") {\n    selected_year = cookie_selected_year\n  };\n  if (cookie_selected_month != \"\") {\n    selected_month = cookie_selected_month\n  };\n  if (cookie_selected_accounts != \"\") {\n    selected_accounts = cookie_selected_accounts\n  };\n\n  return new AccountStatment(selected_month, selected_year, selected_accounts, '', _utils__WEBPACK_IMPORTED_MODULE_0__[\"setCookie\"])\n}\n\nfunction setEvents() {\n  // div_filter_year.querySelectorAll('input').forEach(button => addListener(button, 'click', () => onClickFilter(button)));\n  // div_filter_month.querySelectorAll('input').forEach(button => addListener(button, 'click', () => onClickFilter(button)));\n  accounts_input.forEach(input => Object(_utils__WEBPACK_IMPORTED_MODULE_0__[\"addListener\"])(input, 'click', () => onClickFilter(input)));\n\n  const buttonNewTransaction = document.getElementById(\"button-new-transaction\");\n  Object(_utils__WEBPACK_IMPORTED_MODULE_0__[\"addListener\"])(buttonNewTransaction, 'click', () => onClickNew(buttonNewTransaction));\n\n  const buttonSearch = document.getElementById(\"filter-description-button\");\n  Object(_utils__WEBPACK_IMPORTED_MODULE_0__[\"addListener\"])(buttonSearch, 'click', () => onClickFilter(buttonSearch));\n};\n\nfunction setDefaultFilter() {\n  const year_input = div_filter_year.querySelector('#year-' + account_statment.year)\n  if (year_input) {\n    year_input.checked = true;\n    year_input.parentElement.classList.add('active')\n  }\n\n  const month_input = div_filter_month.querySelector('#month-' + account_statment.month.toString().padStart(2, '0'))\n  if (month_input) {\n    month_input.checked = true;\n    month_input.parentElement.classList.add('active')\n  }\n};\n\n\nconst accounts_input = document.querySelector('#table-accounts').querySelectorAll('input');\nconst account_statment = get_account_statment_main();\nconst modal_dashboard = document.getElementById(\"modal-dashboard\")\nconst modal_title = modal_dashboard.querySelector(\".modal-title\")\nconst modal_body = modal_dashboard.querySelector(\".modal-body\")\nconst div_filter_year = document.querySelector('#filter-year')\nconst div_filter_month = document.querySelector('#filter-month')\n\nwindow.onload = () => {\n  setEvents();\n  // setDefaultFilter();\n  setAccountsSelected(account_statment.accounts)\n\n  // flatpickr('#calendar', {\n  //   mode: \"range\"\n  // })\n\n  filter(account_statment);\n}\n\n//# sourceURL=webpack:///./frontend/js/accounts_statment.js?");

/***/ }),

/***/ "./frontend/js/utils.js":
/*!******************************!*\
  !*** ./frontend/js/utils.js ***!
  \******************************/
/*! exports provided: addListener, setOnClickEvent, handleErrors, range, dateToString, setCookie, getCookie, openDataHref */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"addListener\", function() { return addListener; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"setOnClickEvent\", function() { return setOnClickEvent; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"handleErrors\", function() { return handleErrors; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"range\", function() { return range; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"dateToString\", function() { return dateToString; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"setCookie\", function() { return setCookie; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"getCookie\", function() { return getCookie; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"openDataHref\", function() { return openDataHref; });\nfunction addListener(element, eventName, handler) {\n  if (element.addEventListener) {\n    element.addEventListener(eventName, handler, false);\n  } else if (element.attachEvent) {\n    element.attachEvent('on' + eventName, handler);\n  } else {\n    element['on' + eventName] = handler;\n  }\n}\n\nfunction setOnClickEvent(class_name, on_click_event) {\n  const list = document.getElementsByClassName(class_name);\n\n  if (on_click_event) {\n    for (const key in list) {\n      if (list.hasOwnProperty(key)) {\n        const element = list[key];\n        addListener(element, 'click', () => on_click_event(element));\n      }\n    }\n  }\n}\n\nfunction handleErrors(response) {\n  if (!response.ok) {\n    console.log('Deu ruim');\n    response.json()\n      .then(data => alert(data.message))\n      .then(data => {\n        throw Error(data.message)\n      })\n\n  }\n  return response;\n}\n\nfunction range(size, startAt = 0) {\n  return [...Array(size).keys()].map(i => i + startAt);\n}\n\nfunction dateToString(date) {\n  const year = date.getFullYear().toString().padStart(4, '0');\n  const month = (date.getMonth() + 1).toString().padStart(2, '0');\n  const day = date.getDate().toString().padStart(2, '0');\n\n  return `${year}-${month}-${day}`\n}\n\nfunction setCookie(cname, cvalue, exdays) {\n  var d = new Date();\n  d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));\n  var expires = \"expires=\" + d.toUTCString();\n  document.cookie = cname + \"=\" + cvalue + \";\" + expires + \";path=/\";\n}\n\nfunction getCookie(cname) {\n  var name = cname + \"=\";\n  var decodedCookie = decodeURIComponent(document.cookie);\n  var ca = decodedCookie.split(';');\n  for (var i = 0; i < ca.length; i++) {\n    var c = ca[i];\n    while (c.charAt(0) == ' ') {\n      c = c.substring(1);\n    }\n    if (c.indexOf(name) == 0) {\n      return c.substring(name.length, c.length);\n    }\n  }\n  return \"\";\n}\n\nfunction openDataHref(e) {\n  const data_href = e.getAttribute('data-href')\n\n  if (data_href) {\n    window.open(data_href, \"_self\")\n  }\n}\n\n\n\n//# sourceURL=webpack:///./frontend/js/utils.js?");

/***/ })

/******/ });