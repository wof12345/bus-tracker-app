<script>
  import { twMerge } from "tailwind-merge";
</script>

<div
  class={twMerge(
    `text-2xl font-semibold leading-[44px] text-gray-900 md:text-3xl md:leading-[72px]`,
    $$props.class,
  )}
>
  <slot />
</div>
