<script>
  import { twMerge } from "tailwind-merge";
  import { IconCheck } from "@tabler/icons-svelte";
  import { createEventDispatcher, onMount } from "svelte";
  import { browser } from "$app/environment";

  export let text = "";
  export let value = text;

  export let checked = false;
  export let focused = false;

  export let valueArray = [];

  let isHovered = false;
  let checkboxRef;

  const dispatch = createEventDispatcher();

  function handleClick() {
    checked = !checked;
    dispatch("toggle", { checked, text });

    if (!valueArray?.length) valueArray = valueArray?.value || [];

    if (checked) {
      if (valueArray.find((elm) => elm == value) === undefined) {
        valueArray.push(value);
      }
    } else {
      let valueIndex = valueArray.indexOf(value);
      if (valueIndex > -1) {
        valueArray.splice(valueIndex, 1);
      }
    }

    valueArray = valueArray;
  }

  function isChecked() {
    if (!browser || !valueArray) return;

    let checkValueArray = valueArray.value || valueArray;

    if (checkValueArray?.find((elm) => elm == value)) {
      checked = true;
    } else {
      checked = false;
    }
  }

  function handleTextClick() {
    checkboxRef?.focus();
  }

  $: isChecked(valueArray);
</script>

<button class="flex items-center gap-0" on:click={handleClick}>
  <button
    on:mouseenter={() => (isHovered = true)}
    on:mouseleave={() => (isHovered = false)}
    class="relative mr-2 flex h-4 w-4 flex-shrink-0 items-center justify-center rounded
      {checked
      ? `bg-[#BA24D5] ${focused ? 'ring-4' : ''} ring-[#9E77ED3D]`
      : 'border bg-[#f9fafb] ring-[#9E77ED3D] hover:border-[#BA24D5]  hover:bg-[#BA24D5]'}"
  >
    <input
      bind:this={checkboxRef}
      type="checkbox"
      {value}
      class="absolute inset-0 z-10 h-4 w-4 cursor-pointer opacity-0"
      on:focus={() => (focused = true)}
      on:blur={() => (focused = false)}
    />
    {#if checked}
      <IconCheck color="white" size="14" />
    {/if}
  </button>

  <div
    class={twMerge(
      "flex w-full items-center justify-between text-sm font-medium text-[#111928] md:justify-normal md:gap-1",
      $$props.class,
    )}
    on:click={handleTextClick}
  >
    <slot />
    {text}
  </div>
</button>
