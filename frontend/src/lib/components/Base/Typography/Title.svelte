<script>
  import { twMerge } from "tailwind-merge";
</script>

<div
  class={twMerge(
    `text-3xl font-semibold leading-6 text-gray-900 md:text-3xl md:leading-8`,
    $$props.class,
  )}
>
  <slot />
</div>
