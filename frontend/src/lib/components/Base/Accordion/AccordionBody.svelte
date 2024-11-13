<script>
  import { fly, slide } from "svelte/transition";
  import { twMerge } from "tailwind-merge";
</script>

<div
  class={twMerge("flex w-full justify-center py-3", $$props.class)}
  transition:slide
>
  <slot />
</div>
