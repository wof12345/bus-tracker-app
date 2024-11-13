<script>
  import { twMerge } from "tailwind-merge";

  let header;
</script>

<div
  bind:this={header}
  class={twMerge(
    `tab-header tab-inactive overflow-auto border-b-[2px] p-3 text-sm font-semibold transition delay-150 hover:cursor-pointer
     hover:border-[#BA24D5] hover:bg-brand-50 hover:text-[#9F1AB1]`,
    $$props.class,
  )}
>
  <slot />
</div>
