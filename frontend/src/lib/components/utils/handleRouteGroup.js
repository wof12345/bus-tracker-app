export function handleRouteGroup(url) {
  return url.replace(/\/?\(.*?\)/, "");
}
