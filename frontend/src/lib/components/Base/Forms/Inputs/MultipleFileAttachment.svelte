<script lang="ts">
  import Text from "$components/Base/Typography/Text.svelte";
  import { twMerge } from "tailwind-merge";
  import { IconFile } from "@tabler/icons-svelte";
  import CloseButton from "$components/Assets/CloseButton.svelte";

  export let handleRemove: (file: any) => void = () => {};
  export let attachment: any;
  export let closebtn: boolean = true;
  export let isOpen: boolean = false;
  export let id;

  let size = +Math.fround(attachment?.size / 1000).toPrecision(5);
</script>

<div
  class={twMerge(
    "relative max-h-full w-full max-w-lg rounded-xl border border-[#BA24D5] bg-[#FFF]",
    $$props.class,
  )}
>
  <div class="flex max-w-[85%] items-start gap-4 overflow-hidden px-4 py-4">
    <div
      class="rounded-7 flex aspect-square w-11 min-w-[30px]
                  items-center justify-center overflow-hidden rounded-full bg-brand-100 border-[5px] text-[#BA24D5] border-brand-50 bg- p-1"
    >
      <IconFile size={17} />
    </div>

    <div class="w-full overflow-hidden">
      {#if isOpen}
        <a
          href={attachment?.path}
          target="_blank"
          class="block w-full overflow-hidden text-sm font-medium text-[#344054]"
        >
          {attachment?.name || "File"}
        </a>
      {:else}
        <Text class="w-full overflow-hidden text-sm font-medium text-[#344054]">
          {attachment?.name || "File"}
        </Text>
      {/if}
      <p class="font-normal text-sm text-[#475467]">
        {isNaN(size) ? 200 : size} KB
      </p>
    </div>
  </div>

  {#if closebtn}
    <CloseButton
      onClick={() => handleRemove(id)}
      class="absolute text-gray-400 right-2 top-2 h-7 w-7 p-1"
    />
  {/if}
</div>
