<script>
  import { twMerge } from "tailwind-merge";

  export let value;

  let header;
</script>

<div
  bind:this={header}
  data-value={value}
  class={twMerge(
    `tab-header tab-inactive overflow-auto border-b-[2px] p-3 text-sm font-semibold transition delay-150 hover:cursor-pointer
     hover:border-primary-800 hover:bg-primary-100 hover:text-primary-800`,
    $$props.class,
  )}
>
  <slot />
</div>
