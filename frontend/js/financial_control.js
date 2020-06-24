import {
  setOnClickEvent
} from './utils.js'

function openDataHref(e) {
  const data_href = e.getAttribute('data-href')

  if (data_href) {
    window.open(data_href, "_self")
  }
}

setOnClickEvent("table-item-link", openDataHref);
setOnClickEvent("sidebar-item", openDataHref);