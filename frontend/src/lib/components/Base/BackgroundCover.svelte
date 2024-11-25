<script lang="ts">
  import { fade } from "svelte/transition";
  import { twMerge } from "tailwind-merge";

  export let visible: any = undefined;

  export let hide = () => {};
</script>

<div
  transition:fade
  class={twMerge(
    `${visible ? "flex" : "hidden"} fixed left-0 top-0
		z-[200] h-screen
		w-screen bg-[#000000a5]  bg-opacity-100`,
    $$props.class,
  )}
  on:click={() => {
    hide();
  }}
>
  <slot />
</div>
