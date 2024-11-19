<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { v4 as uuidv4 } from "uuid";
  import { twMerge } from "tailwind-merge";

  const id = uuidv4();

  export let name = `radio-${id}`;
  export let value = ``;
  export let focus = false;
  export let disabled = false;
  export let drop = false;
  export let text = "";
  export let isSelected = false;
  export let focused = false;

  const dispatch = createEventDispatcher();

  function handleClick() {
    isSelected = !isSelected;
    if (!disabled) {
      dispatch("select", { value });
    }
  }
</script>

<button
  on:focus={() => (focused = true)}
  on:blur={() => (focused = false)}
  class={twMerge(
    "input flex items-start gap-2",
    drop ? "w-full" : "",
    isSelected ? "clicked" : "",
  )}
  on:click={handleClick}
>
  <div
    class={twMerge(
      isSelected
        ? `h-full w-full rounded-full border-[6px] border-[#BA24D5] bg-white ${focused ? "ring-4" : ""}  ring-[#9E77ED3D]`
        : "border-[1px] border-[#D1D5DB] bg-[#f9fafb] hover:border-[6px] hover:border-[#BA24D5]",
      "relative mt-[2px] flex h-4 w-4 flex-shrink-0 items-center justify-center rounded-full  p-[1px] ",
      $$props.class,
    )}
  ></div>

  <div
    class={twMerge(
      "flex items-center gap-0 text-start text-sm font-normal text-[#1C1C1C]",
      $$props.class,
    )}
  >
    {text}
  </div>
</button>

<style>
  .clicked .check-icon {
    display: flex;
  }
</style>
