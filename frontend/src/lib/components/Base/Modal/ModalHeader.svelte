<script>
  import { twMerge } from "tailwind-merge";
</script>

<div
  class={twMerge(
    "flex  items-center justify-between border-b border-gray-200 p-6 py-5",
    $$props.class,
  )}
>
  <div class="max-w-[90%]">
    <slot />
  </div>
</div>
