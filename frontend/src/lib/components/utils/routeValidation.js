import { browser } from '$app/environment';

function handleGroup(activePath = '') {
  let pathGroupArray = activePath.split(')');

  if (pathGroupArray.length > 0) activePath = pathGroupArray[1];

  return activePath;
}

export function getPathNameFromString(string) {
  let path = string?.split('?')

  if (path.length > 0) path = path[0]
  else path = string

  return path
}

export function declareActiveRoute(
  activePath,
  referencePath,
  checkFixedPath,
  callback = () => { }
) {
  if (!activePath || !browser) return;

  const routeArray = activePath.split('/');
  const lastRouteName = routeArray[routeArray.length - 1];

  activePath = handleGroup(activePath);


  if (!checkFixedPath) {
    if (activePath.includes(referencePath.href) && referencePath.href !== '/') {
      callback(referencePath);

      return true;
    }
  } else {
    if (activePath === referencePath.href && referencePath.href !== '/') {
      callback(referencePath);

      return true;
    }
  }

  return false;
}

function checkIfParamValid(value) {
  if (value == undefined || value === '') return false

  return true
}

export function addSeachParamToURL({ url = window.location.href, key, value, remove = [] }) {

  if (!key) return

  let param = "";
  let paramObj = {};


  let paramString = url.split("?")[1];

  paramString?.split("&").forEach((elm) => {

    let paramItem = elm.split("=");

    if (!paramItem[0] || paramItem[0] === '') return

    paramObj[paramItem[0]] = paramItem[1];
  });

  paramObj[key] = value;


  let paramKeyArray = Object.keys(paramObj);

  for (let i = 0; i < paramKeyArray.length; i++) {
    if (i === 0) param += '?'

    param +=
      checkIfParamValid(paramObj[paramKeyArray[i]]) ? (
        paramKeyArray[i] +
        "=" +
        paramObj[paramKeyArray[i]] +
        (i == paramKeyArray.length - 1 ? "" : "&")
      ) : '';
  }



  return url.split("?")[0] + param
}
