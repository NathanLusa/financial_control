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
  var table = document.getElementById("table-transactions");
  var accumulated = 0

  clearInnerHTML("table-transactions");

  transactions.forEach(transaction => {
    var row = table.insertRow();
    row.classList.add('table-item-link');

    var cell1 = document.createElement('th');
    cell1.scope = "row";
    row.appendChild(cell1);

    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);

    accumulated = accumulated + transaction.value

    // Add some text to the new cells:
    cell1.innerHTML = transaction.date;
    cell2.innerHTML = transaction.description;
    cell3.innerHTML = "R$ " + transaction.value;
    cell4.innerHTML = "R$ " + accumulated;
  });
}

function setAccountsToTable(accounts) {
  var table = document.getElementById("table-accounts")

  clearInnerHTML("table-accounts");

  accounts.forEach(account => {
    var row = table.insertRow()

    var cellAccount = document.createElement('th');
    cellAccount.scope = "row";

    row.appendChild(cellAccount);
    cellValue = row.insertCell(1);

    cellAccount.innerHTML = account.description
    cellValue.innerHTML = account.value;
  });
}

function setDashboardData(data) {
  console.log(data)

  setAccountsToTable(data.accounts)
  setTransactionsToTable(data.transactions)
}

function loadTransactions() {
  fetch('./api/transactions')
    .then(response => response.json())
    .then(data => setTransactionsToTable(data))
    .catch(err => console.log(err));
}

function loadAccounts() {
  fetch('./api/accounts')
    .then(response => response.json())
    .then(data => setAccountsToTable(data))
    .catch(err => console.log(err));
}

function onClickReload(e) {
  console.log("Reload...")

  const e_initial_date = document.getElementById('initial_date')
  const e_finish_date = document.getElementById('finish_date')

  let url = new URL('/api/dashboard', document.location)
  url.search = new URLSearchParams({
    initial_date: e_initial_date.value,
    finish_date: e_finish_date.value,
    accounts: '1,2,3'
  })

  fetch(url)
    .then(handleErrors)
    .then(response => response.json())
    .then(data => setDashboardData(data))
    .catch(err => console.log(err))
}

function onClickClear(e) {
  console.log('clear')
  clearInnerHTML("table-accounts");
  clearInnerHTML("table-transactions");
}

function main() {
  loadAccounts()
  loadTransactions()
}

var buttonClear = document.getElementById("button-clear");
var buttonMain = document.getElementById("button-main");
var buttonReload = document.getElementById("button-reload");

buttonClear.onclick = onClickClear;
buttonMain.onclick = main;
buttonReload.onclick = onClickReload;

// main()