<script>
  import { twMerge } from "tailwind-merge";

</script>

<div class={twMerge("flex w-full flex-col", $$props.class)}>
  <slot />
</div>
