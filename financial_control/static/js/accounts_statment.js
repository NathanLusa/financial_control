import {
  addListener,
  setOnClickEvent,
  handleErrors
} from './utils.js';


function setDashboardData(data) {
  update(data.accounts, data.transactions)

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

function AccountTable(accounts) {
  return accounts.map(account => AccountItem(account)).join('');
}

function AccountItem(account) {
  return `<tr>
            <th scope="row">${account.description}</th>
            <td>${account.value.toFixed(2)}</td>
          </tr>`
}

function TransactionTable(transactions) {
  var total = 0;
  const f_accumulate = (value) => total += value;

  return transactions.map(transaction => TransactionItem(transaction, f_accumulate)).join('');
}

function TransactionItem(transaction, f_accumulate) {
  const amount = parseFloat(transaction.value);
  const total = f_accumulate(amount);
  const amount_class = amount >= 0 ? 'positive' : 'negative';
  const total_class = total >= 0 ? 'positive' : 'negative';

  return `
    <tr class="table-item-link" data-toggle="modal" data-target="#modal-dashboard" data-href="${transaction.url}" data-modal-title="Transaction" data-transaction-id="${transaction.id}">
      <th scope="row" class="date">${transaction.date}</th>
      <td>${transaction.description}</td>
      <td class="amount bold ${amount_class}">R$ ${amount.toFixed(2)}</td>
      <td class="amount ${total_class}">R$ ${total.toFixed(2)}</td>
    </tr>
  `
}

function update(accounts, transactions) {
  const table_accounts = document.getElementById("table-accounts")
  const table_transactions = document.getElementById("table-transactions");

  table_accounts.innerHTML = AccountTable(accounts)
  table_transactions.innerHTML = TransactionTable(transactions)
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