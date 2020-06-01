import {
  addListener,
  setOnClickTableItemLink
} from './utils.js';

const modal_dashboard = document.getElementById("modal-dashboard")
const modal_title = modal_dashboard.querySelector(".modal-title")
const modal_body = modal_dashboard.querySelector(".modal-body")

const buttonClear = document.getElementById("button-clear");
const buttonFilter = document.getElementById("button-filter");
const buttonNewAccount = document.getElementById("button-new-account");
const buttonNewTransaction = document.getElementById("button-new-transaction");

const input_initial_date = document.getElementById('initial_date')
const inpyt_finish_date = document.getElementById('finish_date')

const table_accounts = document.getElementById("table-accounts")
const table_transactions = document.getElementById("table-transactions");

function clearInnerHTML(elementName) {
  var element = document.getElementById(elementName);
  if (element) {
    element.innerHTML = ""
  }
}

function handleErrors(response) {
  if (!response.ok) {
    response.json()
      .then(data => {
        throw Error(data.message)
      })
  }
  return response;
}

function setTransactionsToTable(transactions) {
  var accumulated = 0.0

  clearInnerHTML("table-transactions");

  transactions.forEach(transaction => {
    const first_cell = document.createElement('th');
    const row = table_transactions.insertRow();

    row.appendChild(first_cell);
    const cell2 = row.insertCell(1);
    const cell3 = row.insertCell(2);
    const cell4 = row.insertCell(3);

    first_cell.scope = "row";
    row.classList.add('table-item-link');
    row.setAttribute('data-toggle', 'modal');
    row.setAttribute('data-target',
      '#modal-dashboard');
    row.setAttribute('data-href', transaction.url);
    row.setAttribute('data-modal-title', 'Transaction');
    row.setAttribute('data-transaction-id', transaction.id);

    const amount = parseFloat(transaction.value);
    accumulated += amount;

    // Add some text to the new cells:
    first_cell.innerHTML = transaction.date;
    cell2.innerHTML = transaction.description;
    cell3.innerHTML = "R$ " + amount.toFixed(2);
    cell4.innerHTML = "R$ " + accumulated.toFixed(2);
  });

  setOnClickTableItemLink(onClickNew);
}

function setAccountsToTable(accounts) {
  clearInnerHTML("table-accounts");

  accounts.forEach(account => {
    const row = table_accounts.insertRow()
    const cellAccount = document.createElement('th');

    row.appendChild(cellAccount);

    const cellValue = row.insertCell(1);
    cellAccount.scope = "row";

    cellAccount.innerHTML = account.description
    cellValue.innerHTML = account.value;
  });
}

function setDashboardData(data) {
  setAccountsToTable(data.accounts)
  setTransactionsToTable(data.transactions)
}

function onClickFilter(e) {
  const url = new URL('/api/accounts_statment', document.location)

  url.search = new URLSearchParams({
    initial_date: input_initial_date.value,
    finish_date: inpyt_finish_date.value,
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

function onClickClear(e) {
  console.log('clear')
  clearInnerHTML("table-accounts");
  clearInnerHTML("table-transactions");
}

addListener(buttonClear, 'click', () => onClickClear(buttonClear));
addListener(buttonFilter, 'click', () => onClickFilter(buttonFilter));
// addListener(buttonNewAccount, 'click', () => onClickNew(buttonNewAccount));
addListener(buttonNewTransaction, 'click', () => onClickNew(buttonNewTransaction));

onClickFilter(buttonFilter.target)