<script>
  import { validateInput } from "$components/utils/validation/validation.js";
  import Title from "$components/Base/Typography/Title.svelte";
  import Paragraph from "$components/Base/Typography/Paragraph.svelte";

  import Input from "$components/Base/Forms/Inputs/Input.svelte";
  import FormFieldLabel from "$components/Base/Forms/Components/FormFieldLabel.svelte";
  import InputGroup from "$components/Base/Forms/Components/InputGroup.svelte";
  import ModalFooter from "$components/Base/Modal/ModalFooter.svelte";
  import ModalBody from "$components/Base/Modal/ModalBody.svelte";
  import ModalHeader from "$components/Base/Modal/ModalHeader.svelte";
  import Modal from "$components/Base/Modal/Modal.svelte";
  import Button from "$lib/components/Base/Buttons/Button.svelte";
  import { goto, invalidateAll } from "$app/navigation";
  import { showToaster } from "$lib/store/toaster.ts";
  import { validateApiResponse } from "$components/utils/validateApiResponse";
  import { deserialize } from "$app/forms";
  import TableButton from "$components/Base/Table/Components/TableButton.svelte";
  import { IconTrash, IconEdit, IconLiveView } from "@tabler/icons-svelte";
  import Section from "$components/Base/Layout/Section.svelte";
  import TableHeader from "$components/Tables/Components/TableHeader.svelte";

  import Table from "$components/Base/Table/Table.svelte";
  import TableHeaderRow from "$components/Base/Table/TableHeaderRow.svelte";
  import TableBodyHeader from "$components/Base/Table/TableBodyHeader.svelte";
  import TableBody from "$components/Base/Table/TableBody.svelte";
  import TableRow from "$components/Base/Table/TableRow.svelte";
  import TableCell from "$components/Base/Table/TableCell.svelte";
  import TableFooter from "$components/Base/Table/TableFooter.svelte";
  import TableFrame from "$components/Base/Table/TableFrame.svelte";
  import Pagination from "$components/Base/Table/Components/Pagination.svelte";

  export let data;

  $: users = data?.users;

  let userCreateForm = {
    email: undefined,
    first_name: undefined,
    last_name: undefined,
    address: undefined,
    phone: undefined,
  };

  let selectedUser;
  let selectedUserRef;

  let createModal;
  let editModal;

  function selectItem(item) {
    selectedUser = item;
    selectedUserRef = JSON.parse(JSON.stringify(item));
  }

  async function create() {
    let form = new FormData();

    if (
      !validateInput(userCreateForm, [
        "phone",
        "address",
        "first_name",
        "last_name",
      ])
    ) {
      userCreateForm = userCreateForm;

      showToaster("Empty required fields");
      return;
    }

    form.append("phone", userCreateForm.phone);
    form.append("email", userCreateForm.email);
    form.append("first_name", userCreateForm.first_name);
    form.append("last_name", userCreateForm.last_name);
    form.append("address", userCreateForm.address);

    const response = await fetch(`?/create`, {
      method: "POST",
      body: form,
    });

    const data = deserialize(await response.text());

    console.log(data);

    if (!validateApiResponse(data)) {
      return;
    }

    createModal.hide();
    showToaster("User added");
    await invalidateAll();
  }

  async function edit() {
    let form = new FormData();

    if (
      !validateInput(selectedUserRef, [
        "phone",
        "address",
        "first_name",
        "last_name",
        "is_verified",
      ])
    ) {
      selectedUserRef = selectedUserRef;
      console.log(selectedUserRef);
      showToaster("Empty required fields");
      return;
    }

    form.append("_id", selectedUserRef._id);
    form.append("phone", selectedUserRef.phone);
    form.append("email", selectedUserRef.email);
    form.append("first_name", selectedUserRef.first_name);
    form.append("last_name", selectedUserRef.last_name);
    form.append("address", selectedUserRef.address);

    const response = await fetch(`?/update`, {
      method: "POST",
      body: form,
    });

    const data = deserialize(await response.text());

    console.log(data);

    if (!validateApiResponse(data)) {
      return;
    }

    editModal.hide();
    showToaster("User updated");
    await invalidateAll();
  }
</script>

<Section class="flex flex-col gap-0 h-full">
  <TableHeader class="mb-3" title="Commuters" subtitle="Manage commuters">
    <div slot="below-head">
      <Button
        onClick={() => {
          createModal.show();
        }}>+ Add new commuter</Button
      >
    </div>
  </TableHeader>

  <Table>
    <TableFrame>
      <TableBody>
        <TableHeaderRow>
          <TableBodyHeader class="col-span-1">Name</TableBodyHeader>
          <TableBodyHeader class="col-span-1">Phone</TableBodyHeader>
          <TableBodyHeader class="col-span-1">Email</TableBodyHeader>
          <TableBodyHeader class="col-span-1"></TableBodyHeader>
        </TableHeaderRow>

        {#each users?.data || [] as item}
          <TableRow
            onClick={() => {}}
            class="items-center hover:cursor-pointer hover:bg-gray-100"
          >
            <TableCell
              class="col-span-1 flex gap-3 font-normal text-sm text-[#475467]"
              >{(item.first_name ?? " ") +
                " " +
                (item.last_name ?? " ")}</TableCell
            >
            <TableCell
              class="col-span-1 flex gap-3 font-normal text-sm text-[#475467]"
              >{item.phone}</TableCell
            >
            <TableCell
              class="col-span-1 flex gap-3 font-normal text-sm text-[#475467]"
              >{item.email}</TableCell
            >

            <TableCell
              class="col-span-1 flex justify-end gap-3 font-normal text-sm text-[#475467]"
            >
              <TableButton
                onClick={(e) => {
                  selectItem(item);
                  editModal.show();
                  e.stopPropagation();
                }}><IconEdit /></TableButton
              >
              <TableButton
                onClick={async (e) => {
                  e.stopPropagation();

                  let form = new FormData();

                  form.append("_id", item._id);

                  const response = await fetch(`?/delete`, {
                    method: "POST",
                    body: form,
                  });

                  const data = deserialize(await response.text());

                  if (!validateApiResponse(data)) {
                    return;
                  }

                  showToaster("User deleted");
                  await invalidateAll();
                }}><IconTrash /></TableButton
              ></TableCell
            >
          </TableRow>
        {/each}
      </TableBody>
    </TableFrame>
    <TableFooter>
      <Pagination totalItems={users?.total || 0} onPageChange={() => {}} />
    </TableFooter>
  </Table>
</Section>

<Modal bind:this={createModal}>
  <ModalHeader>
    <Title class="text-lg md:text-lg">Add commuter</Title>
    <Paragraph>Add a new commuter to the system</Paragraph>
  </ModalHeader>

  <ModalBody class="gap-2">
    <div class="flex gap-2">
      <InputGroup flow="col">
        <FormFieldLabel>First name</FormFieldLabel>
        <Input bind:value={userCreateForm.first_name} placeholder="John" />
      </InputGroup>

      <InputGroup flow="col">
        <FormFieldLabel>Last name</FormFieldLabel>
        <Input bind:value={userCreateForm.last_name} placeholder="Doe" />
      </InputGroup>
    </div>
    <InputGroup flow="col">
      <FormFieldLabel>Email*</FormFieldLabel>
      <Input bind:value={userCreateForm.email} placeholder="joe@email.com" />
    </InputGroup>

    <InputGroup flow="col">
      <FormFieldLabel>Phone</FormFieldLabel>
      <Input bind:value={userCreateForm.phone} placeholder="+0872516211" />
    </InputGroup>

    <InputGroup flow="col">
      <FormFieldLabel>Address</FormFieldLabel>
      <Input
        bind:value={userCreateForm.address}
        placeholder="2/A House, 36no Road"
      />
    </InputGroup>
  </ModalBody>

  <ModalFooter class="gap-2">
    <Button
      onClick={() => {
        create();
      }}>Add</Button
    >

    <Button
      onClick={() => {
        createModal.hide();
      }}>Cancel</Button
    >
  </ModalFooter>
</Modal>

<Modal bind:this={editModal}>
  <ModalHeader>
    <Title class="text-lg md:text-lg">Edit commuter</Title>
    <Paragraph>Edit a commuter from the system</Paragraph>
  </ModalHeader>

  <ModalBody class="gap-2">
    <div class="flex gap-2">
      <InputGroup flow="col">
        <FormFieldLabel>First name</FormFieldLabel>
        <Input bind:value={selectedUserRef.first_name} placeholder="John" />
      </InputGroup>

      <InputGroup flow="col">
        <FormFieldLabel>Last name</FormFieldLabel>
        <Input bind:value={selectedUserRef.last_name} placeholder="Doe" />
      </InputGroup>
    </div>
    <InputGroup flow="col">
      <FormFieldLabel>Email*</FormFieldLabel>
      <Input bind:value={selectedUserRef.email} placeholder="joe@email.com" />
    </InputGroup>

    <InputGroup flow="col">
      <FormFieldLabel>Phone</FormFieldLabel>
      <Input bind:value={selectedUserRef.phone} placeholder="+0872516211" />
    </InputGroup>

    <InputGroup flow="col">
      <FormFieldLabel>Address</FormFieldLabel>
      <Input
        bind:value={selectedUserRef.address}
        placeholder="2/A House, 36no Road"
      />
    </InputGroup>
  </ModalBody>

  <ModalFooter class="gap-2">
    <Button
      onClick={() => {
        edit();
      }}>Save</Button
    >

    <Button
      onClick={() => {
        editModal.hide();
      }}>Cancel</Button
    >
  </ModalFooter>
</Modal>
