export function loadCache(key = "") {
  const data = localStorage.getItem(key);

  return data;
}

export function setCache(key = "", item) {
  const data = localStorage.setItem(key, item);

  return data;
}

export function deleteCache(key = "") {
  const data = localStorage.removeItem(key);

  return data;
}
