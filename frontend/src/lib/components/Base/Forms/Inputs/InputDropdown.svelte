<script>
  import { twMerge } from "tailwind-merge";
  import { clickOutside } from "../../../utils/clickOutside";

  export let value = "";
  export let placeholder = "";
  export let options = [];
  export let dropIcon = "/src/lib/images/icons/timeselect.svg";

  export let label = undefined;

  let isOpen = false;
</script>

<div
  class={twMerge(
    "relative border px-5 py-4 flex flex-col gap-2 w-full rounded-xl font-normal outline-none text-[#1C1C1C] text-xs shadow-sm",
    $$props.class,
  )}
  use:clickOutside={() => (isOpen = false)}
>
  {#if label}
    <p class="font-normal text-xs text-gray-400">{label}</p>
  {/if}

  <div class="relative">
    <input
      class={twMerge(
        "outline-none w-full  bg-transparent placeholder:text-[#1C1C1C80] placeholder:text-xs",
        $$props.inputClass,
      )}
      type="text"
      {placeholder}
      bind:value
    />
    <button
      class="flex items-center gap-2 text-[#111927] font-semibold text-xs rounded"
      on:click={() => (isOpen = !isOpen)}
    >
      <img class="absolute top-[0] right-[0]" src={dropIcon} alt="" />
    </button>
  </div>

  {#if isOpen}
    <div
      class="absolute right-0 top-[100%] mt-1 w-full h-max min-h-[50px] bg-white rounded-lg shadow-xl z-40"
    >
      {#each options as item, idx}
        <div
          class="flex items-center px-4 gap-2 hover:bg-gray-50 w-full {idx ===
          options.length - 1
            ? ''
            : 'border-b'}"
        >
          <a
            href="/dashboard/feedback"
            class="block w-full py-3 text-[#111927] font-medium text-sm"
          >
            {item}
          </a>
        </div>
      {/each}
    </div>
  {/if}
</div>
