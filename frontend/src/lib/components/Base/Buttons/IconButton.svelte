<script>
  import { twMerge } from "tailwind-merge";

  export let src = undefined;

  export let type = "button";
</script>

<button
  {type}
  class={twMerge(
    `relative flex aspect-square items-center justify-center rounded-lg p-2 hover:cursor-pointer hover:bg-gray-300 hover:bg-opacity-[0.2]  `,
    $$props.class,
  )}
  on:click
>
  <slot />

  {#if src}
    <img {src} alt={src} />
  {/if}
</button>
