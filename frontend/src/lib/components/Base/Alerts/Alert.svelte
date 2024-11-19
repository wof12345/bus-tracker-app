<script lang="ts">
  import { twMerge } from "tailwind-merge";
  import Paragraph from "../Typography/Paragraph.svelte";
  import { IconExclamationCircle, IconX } from "@tabler/icons-svelte";
  import { fade } from "svelte/transition";
  import CloseButton from "$components/Assets/CloseButton.svelte";
  import IconButton from "../Buttons/IconButton.svelte";

  export let text: string;
  export let type: string;

  export let onCloseClick = () => {};

  let style = "";

  if (type === "error") {
    style = "border-red-500 text-red-500";
  }
</script>

<div
  transition:fade
  class={twMerge(
    "shadow-xs relative flex items-center justify-between gap-3 rounded-lg border border-gray-300 bg-white p-2",
    $$props.class,
    style,
  )}
>
  <div class="flex gap-2">
    <slot />

    {#if type === "error"}
      <IconExclamationCircle />
    {/if}

    <Paragraph>{text}</Paragraph>
  </div>

  <IconButton
    class={twMerge(
      "scale-75 rounded-full bg-white p-0.5 text-black hover:bg-gray-100 hover:bg-opacity-100",
      $$props.class,
    )}
    on:click={onCloseClick}
  >
    <IconX />
  </IconButton>
</div>
