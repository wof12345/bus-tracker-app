<script lang="ts">
  import { twMerge } from "tailwind-merge";

  export let value: any = "";

  export let text: any = "";
  export let icon: any = null;

  export let onClick = (value: any, icon: any) => {};
</script>

<button
  data-value={value}
  data-text={text}
  type="button"
  class={twMerge(
    "option flex w-full items-center gap-2 px-3 py-2 text-start hover:bg-gray-100 ",
    $$props.class,
  )}
  on:click={() => onClick(value, icon)}
>
  {#if icon}
    <svelte:component this={icon} class="mr-2" />
  {/if}
  <slot />
</button>
