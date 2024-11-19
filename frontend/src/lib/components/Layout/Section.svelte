<script>
  import { twMerge } from "tailwind-merge";
</script>

<section class={twMerge("mx-auto w-full max-w-7xl px-4 py-11", $$props.class)}>
  <slot />
</section>
