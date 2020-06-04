function addListener(element, eventName, handler) {
  if (element.addEventListener) {
    element.addEventListener(eventName, handler, false);
  } else if (element.attachEvent) {
    element.attachEvent('on' + eventName, handler);
  } else {
    element['on' + eventName] = handler;
  }
}

function setOnClickEvent(class_name, on_click_event) {
  const list = document.getElementsByClassName(class_name);

  if (on_click_event) {
    for (const key in list) {
      if (list.hasOwnProperty(key)) {
        const element = list[key];
        addListener(element, 'click', () => on_click_event(element));
      }
    }
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


export {
  addListener,
  setOnClickEvent,
  handleErrors
}