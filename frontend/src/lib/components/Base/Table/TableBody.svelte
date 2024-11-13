<script lang="ts">
  import { twMerge } from "tailwind-merge";
</script>

<div
  class={twMerge(
    "sc-bg-t sc-thumb sc-track sc-w max-h-[800px] min-w-max overflow-auto lg:min-w-full",
    $$props.class,
  )}
>
  <slot />
</div>
