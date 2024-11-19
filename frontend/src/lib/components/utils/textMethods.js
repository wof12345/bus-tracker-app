export function truncateText(text, length) {
  return text.length > length ? text.substring(0, length) + "" : text;
}

export function digitizeNumber(number) {
  if ((number + "").length < 2) {
    number = "0" + number;
  }

  return number;
}

export function StringArrayToObj(array) {
  let obj = {};

  array.forEach((elm) => {
    let pair = elm.split("=");
    let key = pair[0].replace(/"/g, "").trim();

    obj[key] = pair[1];
  });

  return obj;
}
