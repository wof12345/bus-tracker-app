<script>
  import { twMerge } from "tailwind-merge";
</script>

<div class={twMerge("flex items-center justify-center", $$props.class)}>
  <slot />
</div>
