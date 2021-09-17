import {
  handleErrors,
  setOnClickEvent
} from './utils.js'

function openDataHref(e) {
  const data_href = e.getAttribute('data-href')

  if (data_href) {
    window.open(data_href, "_self")
  }
}

function setEvents() {
  setOnClickEvent("table-item-link", openDataHref);
  setOnClickEvent("sidebar-item", openDataHref);
}

function setNavBarNotifications(data) {
  // <span class="notification-icon-badge"></span>
  const notification_item = document.getElementById('notification-item')
  const notification_list = document.getElementById('notification-list')

  if (data.notifications.length > 0) {
    notification_item.innerHTML = notification_item.innerHTML + '<span class="notification-icon-badge"></span>'
  }

  notification_list.innerHTML = NotificationList(data.notifications)
}

function loadNavBarNotifications() {
  const url = new URL('/api/notifications/', document.location)

  fetch(url)
    .then(handleErrors)
    .then(response => response.json())
    .then(data => setNavBarNotifications(data))
    .catch(err => console.log(err))
}

function NotificationList(notifications) {
  // <a class="dropdown-item" href="#">Alguma ação</a>
  return notifications.map(notification => `<a class="dropdown-item" href="${notification.url}">${notification.description}</a>`).join('')
}

function main() {
  setEvents();
  loadNavBarNotifications();
}

main();