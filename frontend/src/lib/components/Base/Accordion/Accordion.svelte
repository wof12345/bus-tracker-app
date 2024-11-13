<script>
  import { twMerge } from "tailwind-merge";
  import IconButton from "../Buttons/IconButton.svelte";
  import AccordionBody from "./AccordionBody.svelte";
  import { IconCircleMinus, IconCirclePlus } from "@tabler/icons-svelte";

  let collapsed = false;
</script>

<div
  class="flex flex-col"
  on:click={() => {
    collapsed = !collapsed;
  }}
>
  <div
    class={twMerge(
      "flex lg:items-center items-start justify-between p-2",
      $$props.class,
    )}
  >
    <div>
      <slot />
    </div>

    {#if collapsed}
      <img src="/minus-circle.svg" />
    {:else}
      <img src="/IconCirclePlus.svg" />
    {/if}
  </div>

  {#if collapsed}
    <AccordionBody>
      <slot name="drawer" />
    </AccordionBody>
  {/if}
</div>
