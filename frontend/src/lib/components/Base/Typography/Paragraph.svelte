<script>
  import { twMerge } from "tailwind-merge";

  export let text = "";
  export let maxLength = 1000;
  export let readmoreUnderline = false;
  export let readmoreGray = false;

  let isExpand = false;

  function handleReadMore() {
    isExpand = !isExpand;
  }
</script>

<div
  class={twMerge(
    `text-sm font-normal text-gray-700 md:text-base`,
    $$props.class,
  )}
>
  <slot />

  <p>
    {#if isExpand}
      {text}
    {:else}
      {text.length > maxLength ? `${text.substring(0, maxLength)}` : text}
    {/if}

    {#if text.length > maxLength}
      <button
        class="text-sm hover:underline {readmoreGray
          ? 'font-medium text-[#475467]'
          : 'font-bold text-gray-900'} "
        on:click={handleReadMore}
      >
        {isExpand ? "read less" : "... read more"}
      </button>
    {/if}
  </p>
</div>
