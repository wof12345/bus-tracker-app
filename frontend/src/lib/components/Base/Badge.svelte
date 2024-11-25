<script>
  import { twMerge } from "tailwind-merge";
</script>

<div
  class={twMerge(
    "shadow-xs rounded-2xl px-2 overflow-hidden text-ellipsis whitespace-nowrap md:text-xs",
    $$props.class,
  )}
>
  <slot />
</div>
