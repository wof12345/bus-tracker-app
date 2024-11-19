<script>
  import { twMerge } from "tailwind-merge";
</script>

<div class={twMerge(`scroll-body`, $$props.class)}>
  <slot id={$$props.id} />
</div>
