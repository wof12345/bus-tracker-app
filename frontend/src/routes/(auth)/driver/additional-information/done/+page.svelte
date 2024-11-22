<script>
  import Text from "$components/Base/Typography/Text.svelte";
  import Title from "$components/Base/Typography/Title.svelte";
</script>

<div class="flex h-full flex-col justify-between mt-28">
  <div
    class="mx-auto flex flex-col max-h-full w-full max-w-[360px] items-center justify-start gap-8 overflow-auto"
  >
    <div class="grid gap-6">
      <div class="mx-auto">
        <img src="/thankslogo.svg" alt="logomark" />
      </div>

      <div class="grid gap-3 text-center">
        <Title class="md:text-3xl text-2xl">Thank you</Title>
        <Text class="text-base font-normal text-[#475467]"
          >We would like to thank you for registering at LearnYourWay.ai <br />
          We will review your application and will send you our feedback within coming
          7 days.</Text
        >
      </div>
    </div>

    <a href="/" class="flex gap-1.5">
      <img src="/arrayleft.svg" alt="" />
      <Text class="text-sm font-semibold text-[#475467]"
        >Back to Landing page
      </Text>
    </a>
  </div>
</div>
