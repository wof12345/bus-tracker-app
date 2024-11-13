<script lang="ts">
  import Button from "$components/Base/Buttons/Button.svelte";
  import Modal from "$components/Base/Modal/Modal.svelte";
  import ModalBody from "$components/Base/Modal/ModalBody.svelte";
  import ModalFooter from "$components/Base/Modal/ModalFooter.svelte";
  import ModalHeader from "$components/Base/Modal/ModalHeader.svelte";
  import Header from "$components/Base/Typography/Header.svelte";
  import Paragraph from "$components/Base/Typography/Paragraph.svelte";
  import Form from "$components/Base/Forms/Components/Form.svelte";
  import { deserialize } from "$app/forms";
  import { showSpinner } from "$lib/store/spinner";
  import { invalidateAll } from "$app/navigation";
  import { validateApiResponse } from "$components/utils/validateApiResponse";
  import { showToaster } from "$lib/store/toaster";

  export let modal: Modal;
  export let subtitle: string = "";
  export let title: string = "";
  export let button: boolean = true;
  export let actionAlias = "Delete";
  export let cancelText = "Cancel";
  export let deleteId;

  export let showOnlySubTitle: boolean = false;

  export let action;

  async function handleDelete() {
    const data = new FormData();

    data.append("id", deleteId);

    const response = await fetch("?/delete", {
      method: "POST",
      body: data,
    });

    const result = deserialize(await response.text());

    if (validateApiResponse(result)) {
      invalidateAll();
      showToaster("Deleted", "Order deleted successfully");
      modal.hide();
    }
  }
</script>

<Modal class="mx-4" bind:this={modal}>
  <ModalHeader>
    <div class="heading-icon-box">
      <img src="/closeIcon.svg" alt="" />
    </div>

    <Header class="mt-4 text-lg text-[#101828] md:text-lg">{title}</Header>
    {#if showOnlySubTitle}
      <Paragraph class="w-full max-w-sm text-sm text-[#475467] md:text-sm">
        {subtitle}
      </Paragraph>
    {:else}
      <Paragraph class="w-full max-w-sm text-sm text-[#475467] md:text-sm"
        >Are you sure you want to {subtitle}? This action cannot be undone.</Paragraph
      >
    {/if}
  </ModalHeader>

  <ModalBody class="p-0"></ModalBody>

  <ModalFooter>
    <Form
      {action}
      class="flex flex-col-reverse gap-2 xs:flex-row "
      formActionSuccess={() => {
        modal.hide();
      }}
    >
      <div class="absolute m-0 flex h-0 w-0 flex-col gap-3 overflow-hidden p-0">
        <slot />
      </div>
      <Button onClick={() => modal.hide()} variant="secondary"
        >{cancelText}</Button
      >
      {#if button}
        <Button
          onClick={handleDelete}
          class="bg-red-600 ring-[#fbd2cf] hover:bg-red-700 focus:ring-4"
          >{actionAlias}</Button
        >
      {:else}
        <Button type="submit" class="bg-red-600 hover:bg-red-500">Delete</Button
        >
      {/if}
    </Form>
  </ModalFooter>
</Modal>

<style>
  .heading-icon-box {
    @apply inline-block rounded-full border-8 border-error-50 bg-error-100 p-2;
  }
</style>
