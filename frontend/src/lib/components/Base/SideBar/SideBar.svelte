<script>
  import { twMerge } from "tailwind-merge";
  import IconButton from "../Buttons/IconButton.svelte";
  import { IconX } from "@tabler/icons-svelte";

  export let visible = false;

  export function show() {
    document.body.classList.add("overflow-hidden");
    visible = true;
  }

  export function hide() {
    document.body.classList.remove("overflow-hidden");
    visible = false;
  }
</script>

{#if visible}
  <div
    class="fixed left-0 top-0 z-50 flex h-screen w-screen bg-[#555961] transition-none "
  >
    <button class="fixed left-0 top-0 z-0 h-full w-full" on:click={hide}
    ></button>

    <IconButton
      class="absolute right-2.5 top-2.5 z-20 w-9 p-2"
      on:click={() => hide()}
    >
      <IconX />
    </IconButton>

    <div
      class={twMerge(
        "relative z-10 flex h-screen  w-full max-w-[311px] flex-col overflow-hidden ",
        $$props.class
      )}
    >
      <slot />
    </div>
  </div>
{/if}
