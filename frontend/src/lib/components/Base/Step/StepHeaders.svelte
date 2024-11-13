<script>
  import { twMerge } from "tailwind-merge";
</script>

<div class={twMerge("w-full", $$props.containerClass)}>
  <div
    class={twMerge(
      "relative flex w-full min-w-full overflow-auto",
      $$props.class,
    )}
  >
    <slot id={$$props.id} />
  </div>
</div>
