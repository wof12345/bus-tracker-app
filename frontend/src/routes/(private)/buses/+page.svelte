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
  import { authStore, isAdmin, isCommuter, isManager } from "$lib/store/auth";
  import { digitizeNumber } from "$components/utils/textMethods.js";
  import Tab from "$components/Base/Tab/Tab.svelte";
  import TabHeader from "$components/Base/Tab/TabHeader.svelte";
  import TabHeaders from "$components/Base/Tab/TabHeaders.svelte";
  import TabPanel from "$components/Base/Tab/TabPanel.svelte";
  import { onMount } from "svelte";
  import { page } from "$app/stores";

  export let data;

  $: buses = data?.vehicles;
  $: reservations = data?.reservations?.data || [];

  $: selected = $page.url.searchParams.get("selected");

  let busCreateForm = {
    name: undefined,
    description: undefined,
    driver: undefined,
    license: undefined,
  };

  let selectedBus;
  let selectedBusRef;

  let createModal;
  let editModal;
  let detailModal;

  let reservationMap = {};

  function selectItem(item) {
    const newQuery = new URLSearchParams({
      selected: item._id,
    });

    goto(`?${newQuery.toString()}`, {
      replaceState: true,
      invalidateAll: false,
      keepFocus: true,
    });

    selectedBus = item;
    selectedBusRef = JSON.parse(JSON.stringify(item));
  }

  function openDriverDetails() {
    detailModal.show();
  }

  function formatTime(time) {
    if (!time) return;

    let str = time.split(":");

    let timeStr = str[0] + ":" + digitizeNumber(str[1]) + " " + str[2];

    return timeStr;
  }

  async function create() {
    let form = new FormData();

    if (!validateInput(busCreateForm, ["driver"])) {
      busCreateForm = busCreateForm;

      showToaster("Empty required fields");
      return;
    }

    form.append("name", busCreateForm.name);
    form.append("description", busCreateForm.description);
    form.append("license", busCreateForm.license);
    form.append("driver", busCreateForm.driver);
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
    showToaster("Bus added");
    await invalidateAll();
  }

  async function edit() {
    let form = new FormData();

    if (
      !validateInput(selectedBusRef, [
        "driver",
        "helper",
        "route",
        "reservation",
        "starting_point",
        "current_coordinates",
        "time",
        "in_campus",
        "status",
      ])
    ) {
      selectedBusRef = selectedBusRef;
      showToaster("Empty required fields");
      return;
    }

    form.append("_id", selectedBusRef._id);
    form.append("name", selectedBusRef.name);
    form.append("description", selectedBusRef.description);
    form.append("license", selectedBusRef.license);
    form.append(
      "coordinates",
      JSON.stringify(selectedBusRef.current_coordinates),
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
    showToaster("Bus updated");
    await invalidateAll();
  }

  onMount(() => {
    reservations?.forEach((elm, idx) => {
      reservationMap[idx] = elm.name;
    });
  });
</script>

<Section class="flex flex-col gap-0 h-full">
  <TableHeader class="mb-3" title="Buses" subtitle="Manage registered buses">
    <div slot="below-head">
      {#if isAdmin($authStore) || isManager($authStore)}
        <Button
          onClick={() => {
            createModal.show();
          }}>+ Add new bus</Button
        >
      {/if}
    </div>
  </TableHeader>

  <Tab invokeLoadOnTabChange={true}>
    {#if reservations?.length > 0}
      <TabHeaders>
        <TabHeader>All</TabHeader>
        {#each reservations as reservation}
          <TabHeader value={reservation._id}>{reservation.name}</TabHeader>
        {/each}
      </TabHeaders>
    {/if}

    {#each [...reservations, ""] as reservation}
      <TabPanel>
        <Table>
          <TableFrame>
            <TableBody>
              <TableHeaderRow>
                <TableBodyHeader class="col-span-1">Name</TableBodyHeader>
                {#if isAdmin($authStore) || isManager($authStore)}
                  <TableBodyHeader class="col-span-1">License</TableBodyHeader>
                  <TableBodyHeader class="col-span-1">Driver</TableBodyHeader>
                {/if}

                <TableBodyHeader class="col-span-1">Reservation</TableBodyHeader
                >
                <TableBodyHeader class="col-span-1">Time</TableBodyHeader>

                <TableBodyHeader class="col-span-1">Status</TableBodyHeader>
                {#if isCommuter($authStore)}
                  <TableBodyHeader class="col-span-1">Route</TableBodyHeader>
                {/if}
                <TableBodyHeader class="col-span-1"></TableBodyHeader>
              </TableHeaderRow>

              {#each buses?.data || [] as item}
                <TableRow
                  onClick={() => {
                    if (isAdmin($authStore) || isManager($authStore))
                      goto(`/buses/${item._id}`);
                    else {
                      selectItem(item);
                      openDriverDetails();
                    }
                  }}
                  class="items-center hover:cursor-pointer hover:bg-gray-100 {selected ===
                  item._id
                    ? 'bg-gray-100'
                    : ''}"
                >
                  <TableCell
                    class="col-span-1 flex gap-3 font-normal text-sm text-[#475467]"
                    >{item.name}</TableCell
                  >
                  {#if isAdmin($authStore) || isManager($authStore)}
                    <TableCell
                      class="col-span-1 flex gap-3 font-normal text-sm text-[#475467]"
                      >{item.license}</TableCell
                    >
                    <TableCell
                      class="col-span-1 flex gap-3 font-normal text-sm text-[#475467]"
                      >{item.driver?.first_name || "Not assigned"}</TableCell
                    >
                  {/if}

                  <TableCell
                    class="col-span-1 flex gap-3 font-normal text-sm text-[#475467]"
                    >{item.reservation?.name || "Not assigned"}</TableCell
                  >
                  <TableCell
                    class="col-span-1 flex gap-3 font-normal text-sm text-[#475467]"
                    >{formatTime(item.time) || "Not assigned"}</TableCell
                  >

                  <TableCell
                    class="col-span-1 flex gap-3 font-normal text-sm text-[#475467]"
                    >{item.status ?? "Stopped"}</TableCell
                  >

                  {#if isCommuter($authStore)}
                    <TableCell class="col-span-1">
                      <Button
                        class="p-0 px-2 text-xs w-max rounded-xl max-w-full"
                        onClick={(e) => {
                          if (item.route?._id)
                            goto(`/routes/${item.route?._id}/edit`);

                          e.stopPropagation();
                        }}
                      >
                        {item.route?.name || "Not assigned"}
                      </Button>
                    </TableCell>
                  {/if}

                  <TableCell
                    class="col-span-1 flex justify-end gap-3 font-normal text-sm text-[#475467]"
                  >
                    {#if item.route && item.driver}
                      <TableButton
                        onClick={(e) => {
                          goto(`/live/${item._id}`);
                          e.stopPropagation();
                        }}><IconLiveView /></TableButton
                      >
                    {/if}

                    {#if isAdmin($authStore) || isManager($authStore)}
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

                          showToaster("Bus deleted");
                          await invalidateAll();
                        }}><IconTrash /></TableButton
                      >
                    {/if}
                  </TableCell>
                </TableRow>
              {/each}
            </TableBody>
          </TableFrame>
          <TableFooter>
            <Pagination
              totalItems={buses?.total || 0}
              onPageChange={() => {}}
            />
          </TableFooter>
        </Table>
      </TabPanel>
    {/each}
  </Tab>
</Section>

<Modal bind:this={createModal}>
  <ModalHeader>
    <Title class="text-lg md:text-lg">Add bus</Title>
    <Paragraph>Add a new bus to the system</Paragraph>
  </ModalHeader>

  <ModalBody class="gap-2">
    <InputGroup flow="col">
      <FormFieldLabel>Name*</FormFieldLabel>
      <Input bind:value={busCreateForm.name} placeholder="Bus name" />
    </InputGroup>

    <InputGroup flow="col">
      <FormFieldLabel>Description*</FormFieldLabel>
      <Input
        bind:value={busCreateForm.description}
        placeholder="Bus description"
      />
    </InputGroup>

    <InputGroup flow="col">
      <FormFieldLabel>License*</FormFieldLabel>
      <Input bind:value={busCreateForm.license} placeholder="Plate text" />
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
    <Title class="text-lg md:text-lg">Edit bus</Title>
    <Paragraph>Edit a bus from the system</Paragraph>
  </ModalHeader>

  <ModalBody class="gap-2">
    <InputGroup flow="col">
      <FormFieldLabel>Name*</FormFieldLabel>
      <Input bind:value={selectedBusRef.name} placeholder="Bus name" />
    </InputGroup>

    <InputGroup flow="col">
      <FormFieldLabel>Description*</FormFieldLabel>
      <Input
        bind:value={selectedBusRef.description}
        placeholder="Bus description"
      />
    </InputGroup>

    <InputGroup flow="col">
      <FormFieldLabel>License*</FormFieldLabel>
      <Input bind:value={selectedBusRef.license} placeholder="Plate text" />
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

<Modal class="min-w-[300px]" bind:this={detailModal}>
  <ModalHeader>
    <Title class="text-lg md:text-lg">Bus details</Title>
    <Paragraph>Check out bus details for {selectedBusRef.name}</Paragraph>
  </ModalHeader>

  <ModalBody class="gap-3">
    <InputGroup flow="col">
      <FormFieldLabel>Driver detals</FormFieldLabel>

      {#if selectedBusRef.driver}
        <div class="flex justify-between w-full">
          <p class="font-semibold text-xs">Name :</p>

          <p class="text-xs">
            {selectedBusRef.driver.first_name +
              " " +
              selectedBusRef.driver.last_name}
          </p>
        </div>

        <div class="flex justify-between w-full">
          <p class="font-semibold text-xs">Phone :</p>

          <p class="text-xs">
            {selectedBusRef.driver.phone}
          </p>
        </div>
      {:else}
        <div class="flex justify-between w-full">
          <p class="text-xs">Driver not assigned yet</p>
        </div>
      {/if}
    </InputGroup>

    <InputGroup flow="col">
      <FormFieldLabel>Helper detals</FormFieldLabel>

      {#if selectedBusRef.helper}
        <div class="flex justify-between w-full">
          <p class="font-semibold text-xs">Name :</p>

          <p class="text-xs">
            {selectedBusRef.helper.first_name +
              " " +
              selectedBusRef.helper.last_name}
          </p>
        </div>

        <div class="flex justify-between w-full">
          <p class="font-semibold text-xs">Phone :</p>

          <p class="text-xs">
            {selectedBusRef.helper.phone}
          </p>
        </div>
      {:else}
        <div class="flex justify-between w-full">
          <p class="text-xs">Helper not assigned yet</p>
        </div>
      {/if}
    </InputGroup>

    <InputGroup flow="col">
      <FormFieldLabel>Description</FormFieldLabel>

      <div class="flex justify-between w-full">
        <p class="text-xs">
          {selectedBusRef.description}
        </p>
      </div>
    </InputGroup>

    <InputGroup flow="col">
      <FormFieldLabel>License text</FormFieldLabel>

      <div class="flex justify-between w-full">
        <p class="text-xs">
          {selectedBusRef.license}
        </p>
      </div>
    </InputGroup>
  </ModalBody>

  <ModalFooter class="gap-2">
    <Button
      onClick={() => {
        detailModal.hide();
      }}>Close</Button
    >
  </ModalFooter>
</Modal>
