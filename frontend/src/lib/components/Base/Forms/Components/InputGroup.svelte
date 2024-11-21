<script lang="ts">
  import { twMerge } from "tailwind-merge";

  export let flow = "row";
</script>

<div
  class={twMerge(
    `input-group flex h-max w-full flex-col items-start justify-between gap-2 md:flex-row`,
    $$props.class,
  )}
  class:md:flex-col={flow === "col"}
>
  <slot />
</div>
