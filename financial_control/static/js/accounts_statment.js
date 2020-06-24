import {
  addListener,
  setOnClickEvent,
  handleErrors,
  range,
  dateToString,
  getCookie,
  setCookie
} from './utils.js';

class AccountStatment {

  constructor(selected_month, selected_year, selected_accounts, description, setCookie) {
    this.monthValue = selected_month
    this.yearValue = selected_year
    this.accountsValue = selected_accounts
    this.descriptionValue = description
    this.setCookie = setCookie
  }

  get initial_date() {
    return new Date(this.yearValue, this.monthValue - 1, 1)
  }

  get finish_date() {
    return new Date(this.yearValue, this.monthValue, 0)
  }

  get year() {
    return this.yearValue
  }

  set year(year) {
    this.yearValue = year
    this.setCookie('year', this.yearValue, 1)
  }

  get month() {
    return this.monthValue
  }

  set month(month) {
    this.monthValue = month
    this.setCookie('month', this.monthValue, 1)
  }

  get accounts() {
    return this.accountsValue
  }

  set accounts(accounts) {
    this.accountsValue = accounts
    this.setCookie('accounts', this.accountsValue, 1)
  }

  get description() {
    return this.descriptionValue
  }

  set description(description) {
    this.descriptionValue = description
  }
}

function setDashboardData(data) {
  update(data.transactions, data.month_balances)

  setOnClickEvent("table-item-link", onClickNew);
}

function onClickFilter(e) {
  account_statment.year = document.querySelector('#filter-year').querySelector('label.active').querySelector('input').getAttribute('data-year');
  account_statment.month = document.querySelector('#filter-month').querySelector('label.active').querySelector('input').getAttribute('data-month');
  account_statment.accounts = getSelectedAccounts();
  account_statment.description = document.querySelector('#filter-description').value;

  filter(account_statment)
}

function onClickFilterDropdown(e) {
  if (e) {
    const filter = e.parentElement.getAttribute('aria-labelledby')
    account_statment.year = filter == 'filter-year' ? e.getAttribute('id') : account_statment.year;
    account_statment.month = filter == 'filter-month' ? e.getAttribute('id') : account_statment.month;
  }

  document.querySelector('#filter').querySelector('button#filter-year').innerHTML = account_statment.year;
  document.querySelector('#filter').querySelector('button#filter-month').innerHTML = account_statment.month;

  filter(account_statment)
}

function filter(account_statment) {
  const url = new URL('/api/accounts_statment', document.location)

  url.search = new URLSearchParams({
    accounts: account_statment.accounts,
    initial_date: dateToString(account_statment.initial_date),
    finish_date: dateToString(account_statment.finish_date),
    description: account_statment.description,
  })

  fetch(url)
    .then(handleErrors)
    .then(response => response.json())
    .then(data => setDashboardData(data))
    .catch(err => console.log(err))
}

function onClickNew(e) {
  const url = e.attributes["data-href"].value
  const title = e.attributes["data-modal-title"].value

  modal_title.innerHTML = title

  fetch(url)
    .then(response => response.text())
    .then(body => modal_body.innerHTML = body)
    .catch(err => console.log(err))
}

function amount_class(value) {
  return value >= 0 ? 'positive' : 'negative'
}

function setAccountsSelected(accounts) {
  accounts_input.forEach(input => {
    input.checked = accounts.includes(input.getAttribute('id'))
  });


}

function getSelectedAccounts() {
  let accounts = []

  accounts_input.forEach(input => {
    if (input.checked) {
      accounts.push(input.getAttribute('id'));
    }
  });

  return accounts
}

function MonthBalanceTable(month_balances) {
  const head = `<thead>
                  <th>Account</th>
                  <th>Income</th>
                  <th>Expense</th>
                  <th>Balance</th>
                  <th>Total</th>
                </thead>`;
  const body = month_balances.map(month_balance => MonthBalanceItem(month_balance)).join('');
  return head + body
}

function MonthBalanceItem(month_balance) {
  const amount = parseFloat(month_balance.amount)
  const income = parseFloat(month_balance.income_value)
  const expense = parseFloat(month_balance.expense_value)
  const accumulated = parseFloat(month_balance.accumulated)

  return `<tr>
            <th scope="row">${month_balance.account}</th>
            <td class="amount ${amount_class(income)}">R$ ${income.toFixed(2)}</td>
            <td class="amount ${amount_class(expense)}">R$ ${expense.toFixed(2)}</td>
            <td class="amount ${amount_class(amount)}">R$ ${amount.toFixed(2)}</td>
            <td class="amount ${amount_class(accumulated)}">R$ ${accumulated.toFixed(2)}</td>
          </tr>`;
}

function TransactionTable(transactions) {
  var total = 0;
  const f_accumulate = (value) => total += value;

  return transactions.map(transaction => TransactionItem(transaction, f_accumulate)).join('');
}

function TransactionItem(transaction, f_accumulate) {
  const amount = parseFloat(transaction.value);
  const total = f_accumulate(amount);

  return `
    <tr class="table-item-link" data-toggle="modal" data-target="#modal-dashboard" data-href="${transaction.url}" data-modal-title="Transaction" data-transaction-id="${transaction.id}">
      <th scope="row" class="date">${transaction.date}</th>
      <td>${transaction.description}</td>
      <td class="amount bold ${amount_class(amount)}">R$ ${amount.toFixed(2)}</td>
      <td class="amount ${amount_class(total)}">R$ ${total.toFixed(2)}</td>
    </tr>
  `
}

function update(transactions, month_balances) {
  const table_transactions = document.getElementById("table-transactions");
  const table_month_balances = document.getElementById("table-month-balances");

  table_transactions.innerHTML = TransactionTable(transactions)
  table_month_balances.innerHTML = MonthBalanceTable(month_balances)
}

function get_account_statment_main() {
  const date_now = new Date();
  var selected_year = date_now.getFullYear();
  var selected_month = date_now.getMonth();
  var selected_accounts = getSelectedAccounts();

  const cookie_selected_year = getCookie('year')
  const cookie_selected_month = getCookie('month')
  const cookie_selected_accounts = getCookie('accounts')

  if (cookie_selected_year != "") {
    selected_year = cookie_selected_year
  };
  if (cookie_selected_month != "") {
    selected_month = cookie_selected_month
  };
  if (cookie_selected_accounts != "") {
    selected_accounts = cookie_selected_accounts
  };

  return new AccountStatment(selected_month, selected_year, selected_accounts, '', setCookie)
}

function setEvents() {
  // div_filter_year.querySelectorAll('input').forEach(button => addListener(button, 'click', () => onClickFilter(button)));
  // div_filter_month.querySelectorAll('input').forEach(button => addListener(button, 'click', () => onClickFilter(button)));
  accounts_input.forEach(input => addListener(input, 'click', () => onClickFilter(input)));

  const buttonNewTransaction = document.getElementById("button-new-transaction");
  addListener(buttonNewTransaction, 'click', () => onClickNew(buttonNewTransaction));

  const buttonSearch = document.getElementById("filter-description-button");
  addListener(buttonSearch, 'click', () => onClickFilter(buttonSearch));
};

function setDefaultFilter() {
  const year_input = div_filter_year.querySelector('#year-' + account_statment.year)
  if (year_input) {
    year_input.checked = true;
    year_input.parentElement.classList.add('active')
  }

  const month_input = div_filter_month.querySelector('#month-' + account_statment.month.toString().padStart(2, '0'))
  if (month_input) {
    month_input.checked = true;
    month_input.parentElement.classList.add('active')
  }
};


const accounts_input = document.querySelector('#table-accounts').querySelectorAll('input');
const account_statment = get_account_statment_main();
const modal_dashboard = document.getElementById("modal-dashboard")
const modal_title = modal_dashboard.querySelector(".modal-title")
const modal_body = modal_dashboard.querySelector(".modal-body")
const div_filter_year = document.querySelector('#filter-year')
const div_filter_month = document.querySelector('#filter-month')

window.onload = () => {
  setEvents();
  // setDefaultFilter();
  setAccountsSelected(account_statment.accounts)

  // flatpickr('#calendar', {
  //   mode: "range"
  // })

  filter(account_statment);
}