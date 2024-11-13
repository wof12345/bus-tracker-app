export function getScrollBarWidth(checkForScrollBar = true, elm = undefined) {
  const box = elm || document.body;

  if (checkForScrollBar) {
    const scrollBarVisible =
      window.innerWidth <= document.documentElement.clientWidth;

    if (scrollBarVisible) return 0;

    const outer = document.createElement('div');

    outer.style.visibility = 'hidden';
    outer.style.overflow = 'scroll';

    box.appendChild(outer);

    const scrollbarWidth = outer.offsetWidth - outer.clientWidth;

    box.removeChild(outer);

    return scrollbarWidth;
  } else {
    const scrollDiv = document.createElement('div');
    scrollDiv.style.width = '100px';
    scrollDiv.style.height = '100px';
    scrollDiv.style.position = 'absolute';

    scrollDiv.style.top = '-9999px';

    box.appendChild(scrollDiv);

    const beforeWidth = scrollDiv.offsetWidth;

    scrollDiv.style.overflow = 'scroll';

    const afterWidth = scrollDiv.offsetWidth;

    const scrollbarWidth = beforeWidth - afterWidth;

    box.removeChild(scrollDiv);

    return scrollbarWidth;
  }
}
