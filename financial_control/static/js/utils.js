function addListener(element, eventName, handler) {
  if (element.addEventListener) {
    element.addEventListener(eventName, handler, false);
  } else if (element.attachEvent) {
    element.attachEvent('on' + eventName, handler);
  } else {
    element['on' + eventName] = handler;
  }
}

function setOnClickTableItemLink(on_click_event) {
  const list = document.getElementsByClassName("table-item-link");

  if (on_click_event) {
    for (const key in list) {
      if (list.hasOwnProperty(key)) {
        const element = list[key];
        addListener(element, 'click', () => on_click_event(element));
      }
    }
  }
}


export {
  addListener,
  setOnClickTableItemLink
}