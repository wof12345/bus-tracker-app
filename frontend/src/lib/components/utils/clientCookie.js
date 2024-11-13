import { StringArrayToObj } from "./textMethods";

export function getCookie(key = "token") {
  let token;

  try {
    const keyValueCookie = document?.cookie?.split(";");

    let cookies = StringArrayToObj(keyValueCookie);
    token = cookies[key];
  } catch (error) {
    // console.log(error);
  } finally {
    return token;
  }
}

export function deleteCookie(name, path = "/", domain) {
  if (getCookie(name)) {
    document.cookie =
      name +
      "=" +
      (path ? ";path=" + path : "") +
      ";expires=Thu, 01 Jan 1970 00:00:01 GMT";
  }


}
