<script lang="ts">
  import { twMerge } from "tailwind-merge";
</script>

<div
  class={twMerge(
    "w-full  overflow-auto rounded-lg border-[1px] border-gray-200 bg-white shadow-sm",
    $$props.class,
  )}
>
  <slot />
</div>
