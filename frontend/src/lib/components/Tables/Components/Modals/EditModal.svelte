<script lang="ts">
  import Button from "$components/Base/Buttons/Button.svelte";
  import Modal from "$components/Base/Modal/Modal.svelte";
  import ModalBody from "$components/Base/Modal/ModalBody.svelte";
  import ModalFooter from "$components/Base/Modal/ModalFooter.svelte";
  import ModalHeader from "$components/Base/Modal/ModalHeader.svelte";
  import Form from "$components/Base/Forms/Components/Form.svelte";

  export let modal: Modal;
  export let context: string = "";

  export let form: any = {};
  export let action;

  export let onAdd = () => {};
</script>

<Modal
  bind:this={modal}
  class="max-h-[70vh] min-w-[300px] max-w-[500px] sm:min-w-[400px] md:w-[30vw]"
>
  <ModalHeader>Edit {context}</ModalHeader>
  <Form
    bind:values={form}
    class="gap-1"
    {action}
    formActionSuccess={() => modal.hide()}
  >
    <ModalBody>
      <div class="flex h-max flex-col gap-3">
        <slot />
      </div>
    </ModalBody>

    <ModalFooter class="flex-col sm:flex-row gap-3">
      <Button on:click={() => modal.hide()} variant="secondary">Cancel</Button>
      <Button>Update</Button>
    </ModalFooter>
  </Form>
</Modal>
