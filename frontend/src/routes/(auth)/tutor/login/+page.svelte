<script>
  import Text from "$components/Base/Typography/Text.svelte";

  import Title from "$components/Base/Typography/Title.svelte";

  import Button from "$components/Base/Buttons/Button.svelte";
  import Input from "$components/Base/Forms/Inputs/Input.svelte";
  import { goto } from "$app/navigation";
  import { showToaster } from "$lib/store/toaster.ts";
  import Paragraph from "$components/Base/Typography/Paragraph.svelte";
  import { authStore } from "$lib/store/auth.ts";
  import { setCache } from "$components/utils/localstorage.js";
  import { browser } from "$app/environment";
  import Logo from "$components/Nav/Logo.svelte";
  import Form from "$components/Base/Forms/Components/Form.svelte";
  import PasswordInput from "$components/Base/Forms/Inputs/PasswordInput.svelte";

  export let form;

  $: error =
    form?.detail || form?.error ? form?.detail || form?.error : undefined;

  let formData = {};

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

<div class="container">
  <div class="box">
    <div class="heading">
      <Logo alt={false} />
      <div class="heading-text-box">
        <Title class="mx-auto w-full text-[23px] md:max-w-[260px]"
          >Log in to your tutor account</Title
        >
        <Text class=" text-base font-normal text-gray-600"
          >Welcome back! Please enter your details.</Text
        >
      </div>
    </div>

    <Form {error} action="/tutor/login?/login" class="mt-6 grid w-full gap-6">
      <div class="grid gap-5">
        <div class=" grid w-full gap-1">
          <Text class="text-left text-sm font-medium text-[#344054]">Email</Text
          >
          <Input
            inputClass="placeholder:text-[#98a2b3] placeholder:font-normal placeholder:text-base"
            class="w-full text-base font-normal"
            label="Enter your email"
            name="email"
            bind:formData
          />
        </div>

        <PasswordInput
          variant={"flex-col"}
          title={"Password"}
          type={"password"}
          name="password_login"
          placeholder="Enter your password"
          bind:value
        />

        <Text class=" text-center text-sm font-normal text-gray-600">
          Forgot your password?
          <a href="/forgot-password">
            <span class=" font-semibold text-[#6941C6]">Reset password</span>
          </a>
        </Text>

        <Button type="submit">Sign in</Button>

        <div class="footer-text-box">
          <Paragraph class="text-gray-600">
            Don’t have an account?
            <a href="/tutor/register">
              <span class="font-semibold text-[#6941C6]"> Sign up </span>
            </a>
          </Paragraph>

          <Paragraph class="text-gray-600">
            Not a tutor?
            <a href="/student/login">
              <span class="font-semibold text-[#6941C6]">
                Login as a student
              </span>
            </a>
          </Paragraph>
        </div>
      </div>
    </Form>
  </div>
</div>

<style>
  .container {
    @apply flex h-full flex-col justify-between px-4 md:px-0;
  }
  .box {
    @apply mx-auto my-auto flex max-h-full w-full max-w-[360px] flex-col items-center justify-start gap-0 overflow-auto px-1 md:max-w-[375px];
  }
  .heading {
    @apply flex w-full flex-col items-center gap-6 text-center;
  }
  .heading-text-box {
    @apply grid gap-2 text-center md:w-[320px] md:gap-3;
  }
  .footer-text-box {
    @apply mt-2 flex flex-col items-center justify-center gap-5;
  }
</style>
