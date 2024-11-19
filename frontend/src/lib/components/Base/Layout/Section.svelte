<script>
  import { twMerge } from "tailwind-merge";
</script>

<section
  class={twMerge("mx-auto h-max w-full px-4 py-11 md:px-8", $$props.class)}
>
  <slot />
</section>
