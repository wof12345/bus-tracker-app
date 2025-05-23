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

  $: reservations = data?.reservations;

  let reservationCreateForm = {
    name: undefined,
    description: undefined,
  };

  let selectedReservation;
  let selectedReservationRef;

  let createModal;
  let editModal;

  function selectItem(item) {
    selectedReservation = item;
    selectedReservationRef = JSON.parse(JSON.stringify(item));
  }

  async function create() {
    let form = new FormData();

    if (!validateInput(reservationCreateForm, ["driver"])) {
      reservationCreateForm = reservationCreateForm;

      showToaster("Empty required fields");
      return;
    }

    form.append("name", reservationCreateForm.name);
    form.append("description", reservationCreateForm.description);
    form.append("license", reservationCreateForm.license);
    form.append("driver", reservationCreateForm.driver);
    form.append("coordinates", JSON.stringify([]));

    const response = await fetch(`?/create`, {
      method: "POST",
      body: form,
    });

    const data = deserialize(await response.text());

    if (!validateApiResponse(data)) {
      return;
    }

    createModal.hide();
    showToaster("Reservation added");
    await invalidateAll();
  }

  async function edit() {
    let form = new FormData();

    if (
      !validateInput(selectedReservationRef, ["driver", "current_coordinates"])
    ) {
      selectedReservationRef = selectedReservationRef;
      showToaster("Empty required fields");
      return;
    }

    form.append("_id", selectedReservationRef._id);
    form.append("name", selectedReservationRef.name);
    form.append("description", selectedReservationRef.description);
    form.append("license", selectedReservationRef.license);
    form.append("driver", selectedReservationRef.driver);
    form.append(
      "coordinates",
      JSON.stringify(selectedReservationRef.current_coordinates),
    );

    const response = await fetch(`?/update`, {
      method: "POST",
      body: form,
    });

    const data = deserialize(await response.text());

    if (!validateApiResponse(data)) {
      return;
    }

    editModal.hide();
    showToaster("Reservation updated");
    await invalidateAll();
  }
</script>

<Section class="flex flex-col gap-0 h-full">
  <TableHeader
    class="mb-3"
    title="Reservationes"
    subtitle="Manage reservations"
  >
    <div slot="below-head">
      <Button
        onClick={() => {
          createModal.show();
        }}>+ Add new reservation</Button
      >
    </div>
  </TableHeader>

  <Table>
    <TableFrame>
      <TableBody>
        <TableHeaderRow>
          <TableBodyHeader class="col-span-1">Name</TableBodyHeader>
          <TableBodyHeader class="col-span-1">Description</TableBodyHeader>
          <TableBodyHeader class="col-span-1"></TableBodyHeader>
        </TableHeaderRow>

        {#each reservations?.data || [] as item}
          <TableRow
            onClick={() => {
              goto(`/buses/${item._id}`);
            }}
            class="items-center hover:cursor-pointer hover:bg-gray-100"
          >
            <TableCell
              class="col-span-1 flex gap-3 font-normal text-sm text-[#475467]"
              >{item.name}</TableCell
            >
            <TableCell
              class="col-span-1 flex gap-3 font-normal text-sm text-[#475467]"
              >{item.description}</TableCell
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

                  showToaster("Reservatiom deleted");
                  await invalidateAll();
                }}><IconTrash /></TableButton
              ></TableCell
            >
          </TableRow>
        {/each}
      </TableBody>
    </TableFrame>
    <TableFooter>
      <Pagination
        totalItems={reservations?.total || 0}
        onPageChange={() => {}}
      />
    </TableFooter>
  </Table>
</Section>

<Modal bind:this={createModal}>
  <ModalHeader>
    <Title class="text-lg md:text-lg">Add reservation</Title>
    <Paragraph>Add a new reservation to the system</Paragraph>
  </ModalHeader>

  <ModalBody class="gap-2">
    <InputGroup flow="col">
      <FormFieldLabel>Name*</FormFieldLabel>
      <Input
        bind:value={reservationCreateForm.name}
        placeholder="Reservation name"
      />
    </InputGroup>

    <InputGroup flow="col">
      <FormFieldLabel>Description*</FormFieldLabel>
      <Input
        bind:value={reservationCreateForm.description}
        placeholder="Reservation description"
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
    <Title class="text-lg md:text-lg">Editreservation</Title>
    <Paragraph>Edit areservation from the system</Paragraph>
  </ModalHeader>

  <ModalBody class="gap-2">
    <InputGroup flow="col">
      <FormFieldLabel>Name*</FormFieldLabel>
      <Input
        bind:value={selectedReservationRef.name}
        placeholder="Reservation name"
      />
    </InputGroup>

    <InputGroup flow="col">
      <FormFieldLabel>Description*</FormFieldLabel>
      <Input
        bind:value={selectedReservationRef.description}
        placeholder="Reservation description"
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
