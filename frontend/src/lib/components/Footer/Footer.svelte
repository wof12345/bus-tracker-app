<script>
  import IconButton from "$components/Base/Buttons/IconButton.svelte";
  import Paragraph from "$components/Base/Typography/Paragraph.svelte";
  import Logo from "$components/Nav/Logo.svelte";
</script>

<div class="bg-[#821890] py-12">
  <div class="mx-auto flex w-full max-w-7xl flex-col gap-8 px-4">
    <div class="flex justify-center">
      <Logo alt={true} />
    </div>

    <Paragraph
      class="m-auto w-full max-w-[280px] text-center text-base text-base font-light text-[#EAECF0]  md:text-base"
    >
      We provide tutoring experiences that create more happiness to the world.
    </Paragraph>

    <div class="flex flex-col">
      <div
        class="sm:px-auto flex justify-center gap-16 px-4 sm:gap-8 md:m-auto"
      >
        <div class="grid gap-4 sm:flex md:gap-8">
          <a class="text-lg font-medium text-[#EAECF0]" href="/about"
            >Who we are</a
          >
          <a class="text-lg font-medium text-[#EAECF0]" href="/">Legal Centre</a
          >
        </div>

        <div class="grid gap-4 sm:flex sm:gap-8">
          <a class="text-lg font-medium text-[#EAECF0]" href="/"
            >Privacy policy</a
          >
          <a class="text-lg font-medium text-[#EAECF0]" href="/"
            >Cookie policy</a
          >
        </div>
      </div>

      <hr class="my-12 border-t border-[#BA24D5]" />
      <div
        class="flex flex-col items-center gap-4 md:flex-row md:justify-between md:gap-0"
      >
        <Paragraph class="text-base text-[#EEAAFD] md:text-base"
          >© 2024 LearnYourWay.ai</Paragraph
        >
        <div>
          <div class="flex gap-4">
            <IconButton><img src="/Twitter.svg" alt="" /></IconButton>
            <IconButton><img src="/linkedin.svg" alt="" /></IconButton>
            <IconButton><img src="/fb.svg" alt="" /></IconButton>
            <IconButton><img src="/instragram.svg" alt="" /></IconButton>
            <IconButton><img src="/snapchat.svg" alt="" /></IconButton>
            <IconButton><img src="/tiktok.svg" alt="" /></IconButton>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
