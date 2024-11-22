<script>
  import { fade } from "svelte/transition";
  import { twMerge } from "tailwind-merge";
  import { v4 as uuidv4 } from "uuid";
  import { onDestroy, onMount } from "svelte";
  import { browser } from "$app/environment";
  import { getScrollBarWidth } from "$lib/components/utils/scrollBarWidth";
  import { clickOutside } from "$lib/components/utils/clickOutside";

  export let visible = false;
  export let id = uuidv4();
  export let anchorEelement;
  export let relativeScrollElement;
  export let parentWidth = false;
  export let left = 20;

  let menu;
  let menuContainer;

  let topPosition = 0;
  let leftPosition;
  let opacity = 0;

  let width;
  let minWidth = "";

  let scrollTop = 0;
  let scrollLeft = 0;

  export function show() {
    setTimeout(() => {
      visible = true;
    }, 50);
  }

  export function hide() {
    visible = false;
  }

  function runStabilizer(visible) {
    if (visible) {
      setTimeout(() => {
        getYScroll();
      }, 50);
    }
  }

  $: runStabilizer(visible);

  function getYScroll(e) {
    if (!visible) return;

    let scrollBarWidth = getScrollBarWidth(false);

    scrollTop =
      e?.target?.scrollTop ||
      window.scrollY ||
      document.documentElement.scrollTop;
    scrollLeft =
      e?.target?.scrollLeft ||
      window.scrollX ||
      document.documentElement.scrollLeft;

    let anchor =
      (anchorEelement
        ? document.querySelector(`.${anchorEelement}`)
        : undefined) ||
      anchorEelement ||
      document.querySelector(`.input-${id}`);

    if (!anchor) return;

    if (anchor) {
      const anchorRect = anchor.getBoundingClientRect();

      topPosition = Math.floor(anchorRect.bottom + 10);

      leftPosition = Math.floor(anchorRect.left - (e ? 0 : scrollBarWidth / 2));

      let leftOffset = leftPosition + left;

      let topOffset = topPosition + menu?.getBoundingClientRect().height + 20;

      if (topOffset > window.innerHeight) {
        topPosition = topPosition - (menu?.getBoundingClientRect().height + 70);
      }

      if (leftOffset > window.innerWidth) {
        leftPosition = leftPosition - (leftOffset - window.innerWidth);
      }

      opacity = 1;

      width = parentWidth ? anchorRect.width + "px" : minWidth;
    }
  }

  onMount(() => {
    let body =
      relativeScrollElement ||
      menuContainer?.closest(".scroll-body") ||
      document.querySelectorAll(`.scroll-body`) ||
      window;

    if (body.length !== undefined) body = body[body.length - 1];

    body?.addEventListener("scroll", getYScroll);
    body?.addEventListener("resize", getYScroll);
  });

  onDestroy(() => {
    if (!browser) return;

    let body =
      relativeScrollElement ||
      menuContainer?.closest(".scroll-body") ||
      document.querySelectorAll(`.scroll-body`) ||
      window;

    if (body.length !== undefined) body = body[body.length - 1];

    body = body[body.length - 1];

    body?.removeEventListener("scroll", getYScroll);
    body?.removeEventListener("resize", getYScroll);
  });
</script>

<div bind:this={menuContainer} class="">
  {#if visible}
    <div
      use:clickOutside={() => {
        hide();
      }}
      transition:fade={{ duration: 100 }}
      bind:this={menu}
      class={twMerge(
        `menu-${id} fixed z-50 flex w-max  overflow-auto rounded-lg bg-white shadow-md opacity-0`,
        $$props.class,
      )}
      style={width
        ? `width: ${width}; top: ${topPosition}px; left: ${leftPosition}px; opacity: ${opacity}; `
        : ""}
    >
      <div class="relative z-10 w-full">
        <slot />
      </div>
    </div>
  {/if}
</div>
