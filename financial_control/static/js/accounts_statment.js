import {
  addListener,
  setOnClickEvent,
  handleErrors
} from './utils.js';


function setDashboardData(data) {
  update(data.accounts, data.transactions, data.month_balances)

  setOnClickEvent("table-item-link", onClickNew);
}

function onClickFilter() {
  const url = new URL('/api/accounts_statment', document.location)

  url.search = new URLSearchParams({
    initial_date: input_initial_date.value,
    finish_date: input_finish_date.value,
    // accounts: '1,2,3'
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

const modal_dashboard = document.getElementById("modal-dashboard")
const modal_title = modal_dashboard.querySelector(".modal-title")
const modal_body = modal_dashboard.querySelector(".modal-body")

const buttonFilter = document.getElementById("button-filter");
const buttonNewTransaction = document.getElementById("button-new-transaction");

const input_initial_date = document.getElementById('initial_date')
const input_finish_date = document.getElementById('finish_date')

addListener(buttonFilter, 'click', () => onClickFilter(buttonFilter));
addListener(buttonNewTransaction, 'click', () => onClickNew(buttonNewTransaction));

onClickFilter(buttonFilter.target);