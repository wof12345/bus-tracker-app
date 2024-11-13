<script>
  import IconButton from "$components/Base/Buttons/IconButton.svelte";
  import { IconX } from "@tabler/icons-svelte";
  import { twMerge } from "tailwind-merge";

  export let onClick = () => {};

  let iconColor = "#98A2B3";

  function handleMouseEnter() {
    iconColor = "#667085";
  }

  function handleMouseLeave() {
    iconColor = "#98A2B3";
  }
</script>

<button
  on:click={() => onClick()}
  class={twMerge(
    `relative flex aspect-square items-center justify-center rounded-lg p-2 hover:cursor-pointer hover:bg-gray-300 hover:bg-opacity-[0.2] w-11 h-11 focus-within:ring-4 focus:ring-[#98A2B324]`,
    $$props.class,
  )}
  on:mouseenter={handleMouseEnter}
  on:mouseleave={handleMouseLeave}
>
  <IconX color={iconColor} size="24" />
</button>
