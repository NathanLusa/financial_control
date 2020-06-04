import {
  addListener,
  setOnClickEvent
} from './utils.js';

const modal_dashboard = document.getElementById("modal-dashboard")
const modal_title = modal_dashboard.querySelector(".modal-title")
const modal_body = modal_dashboard.querySelector(".modal-body")

const buttonClear = document.getElementById("button-clear");
const buttonFilter = document.getElementById("button-filter");
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
    console.log('Deu ruim');
    response.json()
      .then(data => alert(data.message))
      .then(data => {
        throw Error(data.message)
      })

  }
  return response;
}

function getClassPositiveNegative(value) {
  return (value >= 0) ? 'positive' : 'negative'
}

function setTransactionsToTable(transactions) {
  var accumulated = 0.0

  clearInnerHTML("table-transactions");

  transactions.forEach(transaction => {
    const col_date = document.createElement('th');
    const row = table_transactions.insertRow();
    const amount = parseFloat(transaction.value);
    // const date = new Date(transaction.date + 'GMT-0300');

    accumulated += amount;

    row.appendChild(col_date);
    const col_description = row.insertCell(1);
    const col_amount = row.insertCell(2);
    const col_accumulated = row.insertCell(3);

    col_date.scope = "row";
    col_date.classList.add('date')

    col_amount.classList.add('amount')
    col_amount.classList.add('bold')
    col_amount.classList.add(getClassPositiveNegative(amount))

    col_accumulated.classList.add('amount')
    col_accumulated.classList.add(getClassPositiveNegative(accumulated))

    row.classList.add('table-item-link');
    row.setAttribute('data-toggle', 'modal');
    row.setAttribute('data-target', '#modal-dashboard');
    row.setAttribute('data-href', transaction.url);
    row.setAttribute('data-modal-title', 'Transaction');
    row.setAttribute('data-transaction-id', transaction.id);

    // col_date.innerHTML = date;
    col_date.innerHTML = transaction.date;
    col_description.innerHTML = transaction.description;
    col_amount.innerHTML = "R$ " + amount.toFixed(2);
    col_accumulated.innerHTML = "R$ " + accumulated.toFixed(2);
  });

  setOnClickEvent("table-item-link", onClickNew);
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
addListener(buttonNewTransaction, 'click', () => onClickNew(buttonNewTransaction));

onClickFilter(buttonFilter.target)