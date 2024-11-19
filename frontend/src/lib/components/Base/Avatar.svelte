<script>
  import { IconUser } from "@tabler/icons-svelte";
  import { twMerge } from "tailwind-merge";

  export let src;
</script>

<div
  class={twMerge(
    `aspect-square h-14 w-14 min-w-max overflow-hidden rounded-full p-1 flex items-center justify-center bg-white`,
    $$props.class,
  )}
>
  {#if src}
    <img class=" h-full w-full object-cover object-center" {src} alt="/" />
  {:else}
    <IconUser />
  {/if}
</div>
