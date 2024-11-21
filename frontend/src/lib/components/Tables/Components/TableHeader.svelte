<script>
  import Header from "$components/Base/Typography/Header.svelte";
  import Paragraph from "$components/Base/Typography/Paragraph.svelte";

  export let title;
  export let subtitle;
</script>

<div class="flex md:flex-row flex-col mb-4">
  <div
    class="flex md:flex-row flex-col justify-between md:items-center gap-6 w-full"
  >
    <div>
      <Header class="font-bold md:text-3xl">{title}</Header>
      <Paragraph class="text-md font-normal text-[#475467]"
        >{subtitle}</Paragraph
      >
    </div>

    <slot name="below-head" />
  </div>

  <slot />
</div>
