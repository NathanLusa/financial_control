function openDataHref(e) {
  const data_href = e.getAttribute('data-href')
  if (data_href) {
    window.open(data_href, "_self")
  }
}

function addListener(element, eventName, handler) {
  if (element.addEventListener) {
    element.addEventListener(eventName, handler, false);
  }
  else if (element.attachEvent) {
    element.attachEvent('on' + eventName, handler);
  }
  else {
    element['on' + eventName] = handler;
  }
}

const list = document.getElementsByClassName("table-item-link");

for (const key in list) {
  if (list.hasOwnProperty(key)) {
    const element = list[key];
    addListener(element, 'click', () => openDataHref(element));
  }
}
