<script>
  import { twMerge } from "tailwind-merge";
</script>

<div
  class={twMerge(
    "shadow-xs flex min-h-[120px] w-full flex-col gap-4 rounded-xl border-[1px] border-[#EAECF0] p-6",
    $$props.class,
  )}
>
  <slot />
</div>
