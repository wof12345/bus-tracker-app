<script>
  export let bannerData;
  export let closeFn;

  $: placeholder = bannerData?.text;
</script>

{#if bannerData}
  <div
    class="h-[70px] mt-24 w-full md:w-4/5 z-50 rounded-lg bg-gray-25 border-[1px] text-white font-semibold px-6 md:px-12 py-4 text-center lg:flex md:flex justify-center sm:mx-2 md:mx-1 animate-fadeUp hidden items-center relative shadow-lg"
  >
    <div class="flex gap-x-2 md:gap-x-4 items-center justify-center">
      <img
        height="10px"
        class="p-1 md:p-2 bg-white rounded-md lg:block md:block hidden border-[1px] border-gray-200"
        src="/bannerFlag.svg"
        alt="flag"
      />
      <p class="text-sm md:text-base text-black">{placeholder}</p>
      {#if bannerData?.redirect != null}
        <span class="text-sm md:text-base font-normal text-gray-600"
          >Navigate to <a
            on:click={() => closeFn()}
            class="underline"
            href="/settings">settings</a
          ></span
        >
      {/if}
    </div>
    <button
      on:click={() => closeFn()}
      class="h-4 w-4 md:h-10 md:w-10 p-1 md:p-2 absolute z-50 top-3 right-1"
    >
      <img height="10px" width="10px" src="/Icon@2x.svg" alt="" />
    </button>
  </div>

  <div
    class="flex justify-center items-center lg:hidden md:hidden bg-gray-25 border-[1px]"
  >
    <div
      class="h-[70px] w-[90%] absolute rounded-lg bg-white text-white font-semibold px-6 py-4 mt-24 animate-fadeUp border-[1px] border-gray-200 shadow-lg"
    >
      <p class="text-sm md:text-base text-black">{placeholder}</p>
      {#if bannerData?.redirect != null}
        <span class="text-sm md:text-base font-normal text-gray-600"
          >Navigate to <a
            on:click={() => closeFn()}
            class="underline"
            href="/settings">settings</a
          ></span
        >
      {/if}
      <button
        on:click={() => closeFn()}
        class="h-4 w-4 md:h-10 md:w-10 p-1 md:p-2 absolute z-50 top-6 right-3"
      >
        <img height="14px" width="14px" src="/Icon@2x.svg" alt="" />
      </button>
    </div>
  </div>
{/if}
