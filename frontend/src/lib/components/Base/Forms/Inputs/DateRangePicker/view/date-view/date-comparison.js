// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-nocheck
export function isDateBetweenSelected (a, b, c) {
  const start = a.startOf('day').toDate()
  const stop = b.startOf('day').toDate()
  const day = c.startOf('day').toDate()
  return day > start && day < stop
}
