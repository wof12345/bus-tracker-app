<script>
  export let src = "";
</script>

<div
  class="flex aspect-square w-[45px] items-center justify-center overflow-hidden rounded-full"
>
  {#if src !== "" && src}
    <img {src} class="h-full w-full object-cover" alt="/" />
  {:else}
    <div class="h-full w-full bg-gray-400"></div>
  {/if}
</div>
