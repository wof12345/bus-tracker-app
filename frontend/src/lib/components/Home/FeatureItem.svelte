<script>
  export let title = "";
  export let image = { webp: "", png: "" };
  export let description = "";
  export let reversed = false;
  export let bgColorClass = { primary: "", secondary: "" };
</script>

<div class="relative h-[40rem] w-full sm:h-[36rem]">
  <div
    class="mPcraed:gap-8 relative z-10 mx-auto grid h-full w-full max-w-7xl bg-transparent px-4 sm:gap-4 md:grid-cols-2 lg:gap-20 xl:gap-60"
  >
    <div
      class="flex flex-col items-start justify-center gap-4 text-white md:items-center md:gap-6"
      class:md:order-2={reversed}
    >
      <h3
        class="text-2xl font-medium leading-7 sm:text-3xl sm:leading-9 md:text-4xl md:leading-[2.8rem] lg:text-5xl lg:leading-[3.5rem]"
      >
        {title}
      </h3>
      <p class=" text-md py-0 font-light leading-6 lg:text-lg lg:leading-7">
        {description}
      </p>
    </div>
    <div class="flex h-full items-center justify-center">
      <img class="max-h-56 md:max-h-[30rem]" src={image.png} alt="" />
    </div>
  </div>

  <div class="absolute right-0 top-0 z-0 grid h-full w-full md:grid-cols-2">
    <div class={bgColorClass.primary} class:md:order-2={reversed}></div>
    <div class={bgColorClass.secondary}></div>
  </div>
</div>
