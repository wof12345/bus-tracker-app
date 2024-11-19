<script lang="ts">
  import { twMerge } from "tailwind-merge";
</script>

<div
  class={twMerge(
    "flex w-full items-center overflow-hidden text-ellipsis px-2 text-sm font-normal text-[#475467] ",
    $$props.class,
  )}
>
  <slot />
</div>
