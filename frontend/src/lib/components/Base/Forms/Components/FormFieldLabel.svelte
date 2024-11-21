<script>
  import Text from "$components/Base/Typography/Text.svelte";
  import { twMerge } from "tailwind-merge";
</script>

<Text
  class={twMerge(
    "form-label w-full flex-1 overflow-hidden text-ellipsis text-sm font-semibold",
    $$props.class,
  )}
>
  <slot />
</Text>
