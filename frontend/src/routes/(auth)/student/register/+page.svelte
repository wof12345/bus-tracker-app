<script>
  import { goto } from "$app/navigation";
  import { showToaster } from "$lib/store/toaster.ts";
  import Form from "$components/Base/Forms/Components/Form.svelte";
  import Logo from "$lib/components/Nav/Logo.svelte";
  import Text from "$components/Base/Typography/Text.svelte";

  import Title from "$components/Base/Typography/Title.svelte";

  import Button from "$components/Base/Buttons/Button.svelte";
  import Input from "$components/Base/Forms/Inputs/Input.svelte";
  import Paragraph from "$components/Base/Typography/Paragraph.svelte";
  import PasswordInput from "$components/Base/Forms/Inputs/PasswordInput.svelte";

  export let form;

  function showError(error) {
    if (!error) return;

    if (typeof error === "string") {
      return error;
    }

    return "Something went wrong";
  }

  $: error = showError(form?.detail || form?.error);

  let formData = {};
</script>

<div class="flex h-full flex-col justify-between overflow-auto">
  <div
    class="mx-auto flex flex-col max-h-full w-full my-auto max-w-[360px] items-center justify-start gap-8 h-max px-1"
  >
    <Logo alt={false} />
    <div class="grid gap-3 text-center">
      <Title class="text-2xl">Create a student account</Title>
      <Text class=" text-base font-normal text-[#475467]"
        >Create an account to get started.</Text
      >
    </div>

    <Form
      formActionSuccess={() => {
        showToaster("Successfully registered!");
        goto("/student/login");
      }}
      {error}
      action="/student/register?/register"
      class="grid gap-6 w-full"
    >
      <div class="flex items-start gap-4">
        <div class=" w-full max-w-[172px] grid gap-1">
          <Text class="text-left text-sm font-medium text-[#344054]"
            >First name*</Text
          >
          <Input
            class="w-full max-w-[360px] font-normal text-base"
            label="Hammad"
            name="first_name"
            bind:formData
          />
        </div>
        <div class=" w-full max-w-[172px] grid gap-1">
          <Text class="text-left text-sm font-medium text-[#344054]"
            >Last name*</Text
          >
          <Input
            class="w-full max-w-[360px] font-normal text-base"
            label="Al-Fulan"
            name="last_name"
            bind:formData
          />
        </div>
      </div>

      <div class=" w-full grid gap-1">
        <Text class="text-left text-sm font-medium text-[#344054]">Email*</Text>
        <Input
          class="w-full max-w-[360px] font-normal text-base"
          label="Enter your email"
          name="email"
          bind:formData
        />
      </div>

      <div class=" w-full grid gap-1">
        <PasswordInput
          title="Password*"
          variant={"flex-col"}
          name="password"
          type="password"
          placeholder="Enter your password"
        />
      </div>

      <Button type="submit">Get Started</Button>
      <div class="flex justify-center gap-1">
        <Paragraph class="text-[#475467]">Already have an account?</Paragraph>
        <a href="/student/login">
          <Paragraph class="font-semibold text-[#6941C6]">Log in</Paragraph>
        </a>
      </div>
    </Form>
  </div>
</div>
