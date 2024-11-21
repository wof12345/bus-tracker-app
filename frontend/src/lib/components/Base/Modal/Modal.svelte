<script lang="ts">
  import { twMerge } from "tailwind-merge";
  import BackgroundCover from "../BackgroundCover.svelte";
  import { fade, scale } from "svelte/transition";
  import { getScrollBarWidth } from "../../utils/scrollBarWidth";
  import CloseButton from "$components/Assets/CloseButton.svelte";

  export let visible = false;
  export let notificationModal = false;
  export let notiSuccessModal = false;
  export let crossbtnHide = false;
  export let hideCross = false;

  export let onClose = () => {};
  export let onOpen = () => {};

  export function show() {
    let scrollBarwidth = getScrollBarWidth();
    document.body.style = `padding-right: ${scrollBarwidth}px; overflow:hidden; transition: 0s;`;

    visible = true;
    onOpen();
  }

  export function hide() {
    document.body.style = `transition: 0s;`;
    visible = false;
    onClose();
  }

  function handleMouseEnter() {
    hideCross = false;
  }
  function handleMouseLeave() {
    hideCross = true;
  }
</script>

{#if visible}
  <div
    class="fixed left-0 top-0 z-[101] flex h-screen w-screen items-center {notificationModal
      ? 'justify-start pl-72'
      : 'justify-center'}  overflow-hidden"
  >
    <BackgroundCover
      {hide}
      {visible}
      class={notificationModal || notiSuccessModal ? "bg-transparent" : ""}
    />

    <div
      transition:scale={{ duration: 250 }}
      class={twMerge(
        "relative z-40 flex h-max w-max flex-col overflow-hidden rounded-lg bg-white",
        $$props.class,
      )}
      on:mouseenter={handleMouseEnter}
      on:mouseleave={handleMouseLeave}
    >
      {#if crossbtnHide}
        <CloseButton
          class="{hideCross
            ? 'hidden'
            : ''} absolute right-2 top-2 z-50 bg-white p-2 hover:bg-white hover:bg-opacity-100"
          onClick={hide}
        />
      {:else}
        <CloseButton class=" absolute right-4 top-3 z-50 p-1" onClick={hide} />
      {/if}

      <slot />
    </div>
  </div>
{/if}
