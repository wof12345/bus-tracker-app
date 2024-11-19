<script lang="ts">

  import Paragraph from "$components/Base/Typography/Paragraph.svelte";
  import Modal from "$components/Base/Modal/Modal.svelte";
  import ModalBody from "$components/Base/Modal/ModalBody.svelte";

  import ModalHeader from "$components/Base/Modal/ModalHeader.svelte";

  import Button from "$components/Base/Buttons/Button.svelte";
  import Form from "$components/Base/Forms/Components/Form.svelte";
  import TableFooter from "$components/Base/Table/TableFooter.svelte";

  import SubHeading from "$components/Base/Typography/SubHeading.svelte";
  import CheckBox from "$components/Base/Forms/Inputs/CheckBox.svelte";

  export let modal: Modal;

  let selectedFilters = {};
</script>

<Modal bind:this={modal} class="h-max min-h-max">
  <ModalHeader>
    <div>
      <SubHeading class="">Courses</SubHeading>
      <Paragraph class="md:text-sm">Filter by courses you teach.</Paragraph>
    </div>
  </ModalHeader>

  <ModalBody>
    <Form bind:formData={selectedFilters}>
      <div class="flex flex-wrap items-start justify-start gap-3">
        {#each Array(30) as elm}
          <CheckBox value={"chemistry"}>Chemistry</CheckBox>
        {/each}
      </div>

      <TableFooter class="flex justify-start gap-5 border-none px-0 pb-2 pt-2">
        <Button on:click={() => {}} class="max-w-28">Apply filter</Button>
        <Button
          on:click={() => modal.hide()}
          class="max-w-28 "
          variant={"secondary"}>Reset</Button
        >
      </TableFooter>
    </Form>
  </ModalBody>
</Modal>
