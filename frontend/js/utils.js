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

function range(size, startAt = 0) {
  return [...Array(size).keys()].map(i => i + startAt);
}

function setCookie(cname, cvalue, exdays) {
  var d = new Date();
  d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
  var expires = "expires=" + d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function openDataHref(e) {
  const data_href = e.getAttribute('data-href')

  if (data_href) {
    window.open(data_href, "_self")
  }
}

function formatDate(dateObj, frmt) {
  var pad = function (number) {
    return ("0" + number).slice(-2);
  };
  var formats = {
    // get the date in UTC
    Z: function (date) {
      return date.toISOString();
    },
    // weekday name, short, e.g. Thu
    D: function (date, locale, options) {
      return locale.weekdays.shorthand[formats.w(date, locale, options)];
    },
    // full month name e.g. January
    F: function (date, locale, options) {
      return monthToStr(formats.n(date, locale, options) - 1, false, locale);
    },
    // padded hour 1-12
    G: function (date, locale, options) {
      return pad(formats.h(date, locale, options));
    },
    // hours with leading zero e.g. 03
    H: function (date) {
      return pad(date.getHours());
    },
    // day (1-30) with ordinal suffix e.g. 1st, 2nd
    J: function (date, locale) {
      return locale.ordinal !== undefined ?
        date.getDate() + locale.ordinal(date.getDate()) :
        date.getDate();
    },
    // AM/PM
    K: function (date, locale) {
      return locale.amPM[int(date.getHours() > 11)];
    },
    // shorthand month e.g. Jan, Sep, Oct, etc
    M: function (date, locale) {
      return monthToStr(date.getMonth(), true, locale);
    },
    // seconds 00-59
    S: function (date) {
      return pad(date.getSeconds());
    },
    // unix timestamp
    U: function (date) {
      return date.getTime() / 1000;
    },
    W: function (date, _, options) {
      return options.getWeek(date);
    },
    // full year e.g. 2016
    Y: function (date) {
      return date.getFullYear();
    },
    // day in month, padded (01-30)
    d: function (date) {
      return pad(date.getDate());
    },
    // hour from 1-12 (am/pm)
    h: function (date) {
      return (date.getHours() % 12 ? date.getHours() % 12 : 12);
    },
    // minutes, padded with leading zero e.g. 09
    i: function (date) {
      return pad(date.getMinutes());
    },
    // day in month (1-30)
    j: function (date) {
      return date.getDate();
    },
    // weekday name, full, e.g. Thursday
    l: function (date, locale) {
      return locale.weekdays.longhand[date.getDay()];
    },
    // padded month number (01-12)
    m: function (date) {
      return pad(date.getMonth() + 1);
    },
    // the month number (1-12)
    n: function (date) {
      return date.getMonth() + 1;
    },
    // seconds 0-59
    s: function (date) {
      return date.getSeconds();
    },
    // Unix Milliseconds
    u: function (date) {
      return date.getTime();
    },
    // number of the day of the week
    w: function (date) {
      return date.getDay();
    },
    // last two digits of year e.g. 16 for 2016
    y: function (date) {
      return String(date.getFullYear()).substring(2);
    }
  };
  // var locale = overrideLocale || l10n;
  // if (config.formatDate !== undefined) {
  //     return config.formatDate(dateObj, frmt, locale);
  // }
  return frmt
    .split("")
    .map(function (c, i, arr) {
      return formats[c] && arr[i - 1] !== "\\" ?
        formats[c](dateObj)
        // ? formats[c](dateObj, locale, config)
        :
        c !== "\\" ?
        c :
        "";
    })
    .join("");
};


export {
  addListener,
  setOnClickEvent,
  handleErrors,
  range,
  setCookie,
  getCookie,
  openDataHref,
  formatDate
}