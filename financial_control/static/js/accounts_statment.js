import {
  addListener,
  setOnClickEvent,
  handleErrors,
  range,
  dateToString
} from './utils.js';


function setDashboardData(data) {
  update(data.accounts, data.transactions, data.month_balances)

  setOnClickEvent("table-item-link", onClickNew);
}

function onClickFilter(e) {
  const url = new URL('/api/accounts_statment', document.location)

  const year = document.querySelector('#filter-year').querySelector('label.active').querySelector('input').getAttribute('id')
  const month = document.querySelector('#filter-month').querySelector('label.active').querySelector('input').getAttribute('id')

  const initial_date = new Date(year, month - 1, 1)
  const finish_date = new Date(year, month, 0)

  url.search = new URLSearchParams({
    initial_date: dateToString(initial_date),
    finish_date: dateToString(finish_date),
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

function AccountTable(accounts) {
  return accounts.map(account => AccountItem(account)).join('');
}

function AccountItem(account) {
  return `<tr>
            <th scope="row">${account.description}</th>
            <td>${parseFloat(account.value).toFixed(2)}</td>
          </tr>`
}

function MonthBalanceTable(month_balances) {
  const head = `<thead>
                  <th>Account</th>
                  <th>Date</th>
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
            <td>${month_balance.date}</td>
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

function update(accounts, transactions, month_balances) {
  const table_accounts = document.getElementById("table-accounts")
  const table_transactions = document.getElementById("table-transactions");
  const table_month_balances = document.getElementById("table-month-balances");

  table_accounts.innerHTML = AccountTable(accounts)
  table_transactions.innerHTML = TransactionTable(transactions)
  table_month_balances.innerHTML = MonthBalanceTable(month_balances)
}

function FilterButtons() {
  const years = range(6, 2015)
  const months = range(12, 1)

  const create_div = (id, items, item_checked, pad) => `
    <div class="btn-group btn-group-toggle" data-toggle="buttons" id="${id}">
      ${items.map(item => create_label(item, item_checked, pad)).join('')}
    </div>`;

  const create_label = (item, item_checked, pad) => `
    <label class="btn btn-primary ${item == item_checked ? 'active' : ''}">
      <input type="radio" name="options" id="${item.toString().padStart(pad, '0')}"
        ${item == item_checked ? 'checked' : ''}> ${item.toString().padStart(pad, '0')}
    </label>`;

  const date_now = new Date();
  const year_now = date_now.getFullYear();
  const month_now = date_now.getMonth() + 1;

  const filter_years = create_div('filter-year', years, year_now, 4);
  const filter_months = create_div('filter-month', months, month_now, 2);

  div_filter.innerHTML = filter_years + filter_months;
}

const modal_dashboard = document.getElementById("modal-dashboard")
const modal_title = modal_dashboard.querySelector(".modal-title")
const modal_body = modal_dashboard.querySelector(".modal-body")

const div_filter = document.getElementById('filter');
FilterButtons()

const buttonNewTransaction = document.getElementById("button-new-transaction");

const buttons = document.querySelector('#filter').querySelectorAll('input');
buttons.forEach(button => addListener(button, 'click', () => onClickFilter(button)));

addListener(buttonNewTransaction, 'click', () => onClickNew(buttonNewTransaction));

onClickFilter();