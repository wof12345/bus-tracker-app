<script lang="ts">
  import { twMerge } from "tailwind-merge";
</script>

<row
  class={twMerge(
    "flex w-full flex-col items-center absolute top-0 left-0  justify-between gap-3 border-b border-gray-200 px-6 py-4 sm:flex-row",
    $$props.class,
  )}
>
  <slot />
</row>
