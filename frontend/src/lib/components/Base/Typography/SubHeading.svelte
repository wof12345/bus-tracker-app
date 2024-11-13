<script>
  import { twMerge } from "tailwind-merge";
</script>

<div
  class={twMerge(
    `text-primary-700 text-sm  font-semibold leading-[20px]  md:text-lg md:leading-6`,
    $$props.class,
  )}
>
  <slot />
</div>
