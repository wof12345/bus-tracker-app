<script>
  import Text from "$components/Base/Typography/Text.svelte";

  import Title from "$components/Base/Typography/Title.svelte";

  import Button from "$components/Base/Buttons/Button.svelte";
  import Input from "$components/Base/Forms/Inputs/Input.svelte";
  import { goto } from "$app/navigation";
  import { showToaster } from "$lib/store/toaster.ts";
  import Paragraph from "$components/Base/Typography/Paragraph.svelte";
  import { authStore } from "$lib/store/auth.js";
  import { setCache } from "$components/utils/localstorage.js";
  import { browser } from "$app/environment";
  import Logo from "$components/Nav/Logo.svelte";
  import Form from "$components/Base/Forms/Components/Form.svelte";
  import PasswordInput from "$components/Base/Forms/Inputs/PasswordInput.svelte";

  export let form;
  let formData = {};
  $: error =
    form?.detail || form?.error ? form?.detail || form?.error : undefined;

  function handleForm() {
    if (!browser) return;

    if (form?.error || !form || !("token" in form)) return;

    showToaster("Logged in");

    let userInfo = { ...form };
    delete userInfo.token;

    authStore.set({ isAuthenticated: true, user: userInfo });

    setCache("user", JSON.stringify(userInfo));

    goto("/home");
  }

  $: handleForm(form);
  let value;
</script>

<div class="flex h-full flex-col justify-between">
  <div
    class="mx-auto my-auto flex max-h-full w-full max-w-[375px] flex-col items-center justify-start gap-8 overflow-auto px-4 md:px-1"
  >
    <div class="flex w-full flex-col items-center gap-6 text-center">
      <Logo alt={false} />
      <div class="grid gap-2 text-center md:w-[320px] md:gap-3">
        <Title class="text-[23px]">Log in to your admin account</Title>
        <Text class=" text-base font-normal text-[#475467]"
          >Welcome back! Please enter your details.</Text
        >
      </div>
    </div>

    <Form {error} action="/admin/login?/login" class="grid w-full gap-6">
      <div class="grid gap-5">
        <div class=" grid w-full gap-1">
          <Text class="text-left text-sm font-medium text-[#344054]">Email</Text
          >
          <Input
            inputClass="placeholder:text-[#667085] placeholder:font-normal placeholder:text-base"
            class="w-full max-w-[360px] text-base font-normal"
            label="Enter your email"
            name="email"
            bind:formData
          />
        </div>

        <div class=" grid w-full gap-1">
          <PasswordInput
            class="w-full max-w-[360px]"
            inputClass="placeholder:text-[#667085] placeholder:font-normal placeholder:text-base"
            variant={"flex-col"}
            title={"Password"}
            type={"password"}
            name="password_login"
            placeholder="Enter your password"
            bind:value
          />
        </div>
      </div>

      <!-- <Text class=" text-sm font-normal text-[#475467]">
        Forgot your password?
        <a href="/forgot-password">
          <span class=" font-semibold text-[#6941C6]">Reset password</span>
        </a>
      </Text> -->

      <Button class="w-full max-w-[360px]" type="submit">Sign in</Button>
    </Form>
  </div>
</div>
