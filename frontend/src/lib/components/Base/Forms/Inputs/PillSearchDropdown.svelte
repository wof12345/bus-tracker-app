<script lang="ts">
  import { v4 as uuidv4 } from "uuid";
  import { clickOutside } from "$components/utils/clickOutside";
  import { IconCaretDown } from "@tabler/icons-svelte";

  export let selectedValue: string[] = [];
  export let label: string;
  export let options: any[] = [];
  export let value: any;
  export let extraName: string;

  export let variant: string = "default";
  export let placeholderText = false;
  export let valueIcon = false;

  let filteredOptions = [];

  $: filteredOptions = options;
  let isExpanded = false;

  const id = uuidv4();

  const handleInput = (e: any) => {
    const value = e.target.value;

    filteredOptions = options.filter((item: string | number) =>
      (item.name || item)
        .toString()
        .toLowerCase()
        .includes(value.toLowerCase()),
    );

    if (value === "") {
      filteredOptions = options;
    }

    return filteredOptions;
  };

  function removeItem(selectedValue, item) {
    let has = false;
    for (let i = 0; i < selectedValue.length; i++) {
      if ((selectedValue[i].id || selectedValue[i]) === (item.id || item)) {
        selectedValue.splice(i, 1);
        has = true;
        break;
      }
    }
    return selectedValue;
  }

  function hasItem(selectedValue, item) {
    let has = false;

    for (let i = 0; i < selectedValue.length; i++) {
      if ((selectedValue[i].id || selectedValue[i]) === (item.id || item)) {
        has = true;
        break;
      }
    }

    return has;
  }

  const clickHandler = (item: string | number) => {
    isExpanded = true;
    placeholderText = true;

    if (!hasItem(selectedValue, item)) {
      selectedValue = [...selectedValue, item];
      value = "";
    } else {
      selectedValue = removeItem(selectedValue, item);
    }

    if (selectedValue.length === 0) {
      value = 0;
    }
  };

  const removeSelectedValue = (itemToRemove) => {
    selectedValue = removeItem(selectedValue, itemToRemove);

    if (selectedValue.length === 0) {
      value = 0;
    }
  };

  const clearAllSelected = () => {
    selectedValue = [];
    value = 0;
  };
</script>

<div
  use:clickOutside={() => {
    isExpanded = false;
  }}
>
  <button
    class="relative w-full rounded-lg focus-within:ring-4 focus-within:ring-[#9E77ED3D]"
    on:click={() => (isExpanded = !isExpanded)}
  >
    <div
      class="shadow-xs ::-webkit-scrollbar flex max-h-16 w-full flex-wrap items-center gap-2 overflow-auto rounded-lg border border-gray-300 px-3.5 py-2.5 text-base font-medium text-gray-900 outline-none placeholder:text-base placeholder:font-normal placeholder:text-gray-400
      {isExpanded ? 'shadow-input-focus' : ''} focus-within:border-[#EEAAFD]"
    >
      {#if selectedValue.length === 0}
        <div class="flex justify-between">
          <input
            class="w-full cursor-pointer font-normal leading-6 outline-none placeholder:text-base placeholder:text-gray-900"
            type="text"
            on:input={handleInput}
            placeholder={options[0]?.name ?? label}
            value={value?.name || (typeof value === "string" ? value : "")}
            autocomplete="off"
            required
          />
          <IconCaretDown class="absolute right-3 top-3" />
        </div>
      {/if}

      {#if selectedValue.length > 0}
        <div class="flex w-full flex-wrap gap-2">
          {#each selectedValue as item, index}
            <div
              class="item flex items-center justify-center gap-1 rounded-md border-[1px] border-gray-300 px-1 text-sm font-medium text-gray-700"
            >
              <p>
                {item.name ?? item}
              </p>
              <button
                class="w-2.5"
                on:click={(e) => {
                  e.stopPropagation();
                  removeSelectedValue(item);
                }}
              >
                <img class="min-h-1.5 min-w-1.5" src="/close.svg" alt="" />
              </button>
            </div>
          {/each}
        </div>
      {/if}
    </div>

    {#if isExpanded}
      <div
        class="absolute my-1.5 flex w-full flex-col dropdown-container-{id} z-50 max-h-[250px] overflow-auto rounded-lg bg-white py-1.5 shadow-md"
      >
        {#if selectedValue.length > 0}
          <button
            class=" flex py-2.5 pl-3 text-[16px] font-medium text-[#101828] hover:bg-gray-100"
            on:click={(e) => {
              e.stopPropagation();
              clearAllSelected();
            }}
          >
            {extraName}
          </button>
        {/if}

        {#each filteredOptions as option, index}
          <button
            on:click={(e) => {
              e.preventDefault();
              e.stopPropagation();
              clickHandler(option);
            }}
            class="my-0.5 flex items-center justify-between pl-3 text-start hover:bg-gray-100 {selectedValue.includes(
              option,
            )
              ? 'hovered'
              : ''} "
          >
            <div class="flex items-center gap-2">
              {#if valueIcon}
                <svelte:component this={option?.icon} />
              {/if}

              {#if !(option.value === 0)}
                <button class=" py-2.5 text-[16px] font-medium text-[#101828]">
                  {option.name || index + 1}
                </button>
              {/if}
            </div>

            <img
              class="flex justify-end pr-1"
              src={selectedValue.includes(option) ? "/select.svg" : ""}
              alt=""
            />
          </button>
        {/each}
      </div>
    {/if}
  </button>
</div>

<style>
  .hovered {
    background-color: #f3f4f6;
  }
</style>
