<script lang="ts">
  import { twMerge } from "tailwind-merge";

  export let onClick = () => {};
</script>

<row
  on:click={() => onClick()}
  class={twMerge(
    "grid min-w-max auto-cols-fr grid-flow-col hover:bg-gray-50 border-t border-t-gray-200 bg-white px-6 py-4 md:min-w-full",
    $$props.class,
  )}
>
  <slot />
</row>
