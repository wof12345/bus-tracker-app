<script>
  // @ts-nocheck

  import { onMount, createEventDispatcher, getContext, tick } from "svelte";
  import { contextKey } from "./lib/context.js";
  import { getPosition } from "./lib/positioning.js";
  import { once } from "./lib/event-handling.js";
  import { v4 as uuidv4 } from "uuid";
  import { getScrollBarWidth } from "$lib/components/utils/scrollBarWidth.js";

  const { isOpen, isClosing, config, resetView } = getContext(contextKey);
  const dispatch = createEventDispatcher();

  let popover;
  let w;
  let triggerContainer;
  let contentsAnimated;
  let contentsWrapper;
  let isFullscreen = false;
  let translateY = 0;
  let translateX = 0;

  let minWidth = "max-content";

  export let trigger;
  export let parentWidth = false;
  export let id;
  export let anchorEelement;

  $: menu = contentsWrapper;

  export function close() {
    isClosing.set(true);
    once(contentsAnimated, "animationend", () => {
      isClosing.set(false);
      isOpen.set(false);
      dispatch("closed");
    });
  }

  function checkForFocusLoss(evt) {
    if (!$isOpen) return;
    let el = evt.target;
    do {
      if (el === popover) {
        return;
      }
      el = el.parentNode;
    } while (el);
    close();
  }

  onMount(() => {
    config.closeOnFocusLoss &&
      document.addEventListener("click", checkForFocusLoss);
    if (!trigger) {
      return;
    }
    triggerContainer.appendChild(trigger.parentNode.removeChild(trigger));

    return () => {
      config.closeOnFocusLoss &&
        document.removeEventListener("click", checkForFocusLoss);
    };
  });

  const doOpen = async (e) => {
    isOpen.set(true);
    resetView();

    getYScroll(e);

    await tick();
    const { top, left, fullscreen } = getPosition(window, e, config);
    isFullscreen = fullscreen;

    translateY = top;
    translateX = left;

    dispatch("opened");
  };

  let topPosition = 0;
  let leftPosition = 0;
  let width = 0;

  let scrollTop = 0;
  let scrollLeft = 0;
  let maxHeight = 300;
  let opacity = 0;

  function getYScroll(e) {
    if (!$isOpen) return;

    let scrollBarWidth = getScrollBarWidth(false);
    opacity = 0;

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

      setTimeout(() => {
        topPosition = Math.floor(anchorRect.bottom + 10);

        leftPosition = Math.floor(
          anchorRect.left - (e ? 0 : scrollBarWidth / 2),
        );

        let leftOffset =
          leftPosition + menu?.getBoundingClientRect().width + 20;
        let topOffset = topPosition + menu?.getBoundingClientRect().height + 20;

        if (topOffset > window.innerHeight) {
          topPosition =
            topPosition - (menu?.getBoundingClientRect().height + 70);
        }

        if (leftOffset > window.innerWidth) {
          leftPosition = leftPosition - (leftOffset - window.innerWidth);
        }

        opacity = 1;
      }, 50);

      width = parentWidth ? anchorRect.width + "px" : minWidth;
    }
  }
</script>

<svelte:window bind:innerWidth={w} />
<div class="sc-popover" bind:this={popover}>
  <div
    class="trigger"
    on:click={doOpen}
    on:keypress={(e) => e.key === "Enter" && doOpen()}
    bind:this={triggerContainer}
  >
    <slot name="trigger" />
  </div>

  <div
    class="z-0 fixed top-0 left-0 right-0 bottom-0 m-auto pointer-events-none input-{id} w-[300px]"
  ></div>

  <div
    class="contents-wrapper fixed top-0 left-0"
    style={(width
      ? `width: ${width}px; top: ${topPosition}px; left: ${leftPosition}px; max-height: ${maxHeight}px; `
      : "") + `opacity: ${opacity}`}
    class:visible={$isOpen}
    class:shrink={$isClosing}
    class:is-fullscreen={isFullscreen}
    bind:this={contentsWrapper}
  >
    <div class="wrapper w-full" bind:this={contentsAnimated}>
      <div class="contents-inner w-full">
        <slot name="contents" />
      </div>
    </div>
  </div>
</div>

<style>
  .sc-popover {
    position: relative;
  }

  .contents-wrapper {
    transition: none;
    z-index: 50;
    display: none;
  }

  .contents-wrapper.visible {
    display: block;
  }

  .contents-wrapper.visible.is-fullscreen {
    display: flex;
    /* width: 100vw; */
    height: 100%;
    overflow: visible;
  }

  .contents-wrapper.visible .wrapper {
    opacity: 1;
    transform: scale(1);
    display: block;
    border-radius: 10px;
  }

  .contents-wrapper.shrink .wrapper {
    animation: shrink 150ms forwards cubic-bezier(0.92, 0.09, 0.18, 1.05);
  }

  .wrapper {
    background: #fff;
    box-shadow: 0px 5px 5px 5px rgba(0, 0, 0, 0.1);
    opacity: 0.8;
    padding-top: 0;
    display: none;
    animation: grow 200ms forwards cubic-bezier(0.92, 0.09, 0.18, 1.05);
  }

  .contents-inner {
    animation: fadeIn 400ms forwards;
  }

  @keyframes grow {
    0% {
      transform: scale(0.9, 0.1);
      opacity: 0;
    }
    30% {
      opacity: 1;
    }
    100% {
      transform: scale(1);
    }
  }

  @keyframes shrink {
    0% {
      transform: scale(1);
      opacity: 1;
    }
    70% {
      opacity: 1;
    }
    100% {
      opacity: 0;
      transform: scale(0.9, 0.1);
    }
  }

  @keyframes fadeIn {
    0% {
      opacity: 0;
    }
    50% {
      opacity: 0;
    }
    100% {
      opacity: 1;
    }
  }
</style>
