<script>
  import { twMerge } from "tailwind-merge";
</script>

<div
  class={twMerge(
    `sc-w sc-bg sc-bg-t sc-thumb flex flex-col relative overflow-hidden overflow-y-auto p-6 py-3 ::-webkit-scrollbar`,
    $$props.class,
  )}
>
  <slot />
</div>
