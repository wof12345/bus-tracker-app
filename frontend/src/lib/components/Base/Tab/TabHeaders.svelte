<script>
  import { twMerge } from "tailwind-merge";
</script>

<div
  class="max-w-full overflow-auto [&::-webkit-scrollbar-thumb]:bg-transparent"
>
  <div
    class={twMerge(
      "flex w-max min-w-full gap-2 overflow-auto border-b border-gray-200",
      $$props.class,
    )}
  >
    <slot id={$$props.id} />
  </div>
</div>
