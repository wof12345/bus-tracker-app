<script>
  import SearchDropdown from "$components/Base/Forms/Inputs/SearchDropdown.svelte";
  import FormFieldLabel from "$components/Base/Forms/Components/FormFieldLabel.svelte";
  import InputGroup from "$components/Base/Forms/Components/InputGroup.svelte";
  import Section from "$components/Base/Layout/Section.svelte";
  import Tab from "$components/Base/Tab/Tab.svelte";
  import TabBody from "$components/Base/Tab/TabBody.svelte";
  import TabHeader from "$components/Base/Tab/TabHeader.svelte";
  import TabPanel from "$components/Base/Tab/TabPanel.svelte";
  import TabHeaders from "$components/Base/Tab/TabHeaders.svelte";
  import Table from "$components/Base/Table/Table.svelte";
  import TableHeaderRow from "$components/Base/Table/TableHeaderRow.svelte";
  import TableBodyHeader from "$components/Base/Table/TableBodyHeader.svelte";
  import TableBody from "$components/Base/Table/TableBody.svelte";
  import TableRow from "$components/Base/Table/TableRow.svelte";
  import TableCell from "$components/Base/Table/TableCell.svelte";
  import TableFooter from "$components/Base/Table/TableFooter.svelte";
  import TableFrame from "$components/Base/Table/TableFrame.svelte";
  import Pagination from "$components/Base/Table/Components/Pagination.svelte";

  import Paragraph from "$components/Base/Typography/Paragraph.svelte";

  import Text from "$components/Base/Typography/Text.svelte";
  import Input from "$components/Base/Forms/Inputs/Input.svelte";
  import TextArea from "$components/Base/Forms/Inputs/TextArea.svelte";
  import Button from "$components/Base/Buttons/Button.svelte";
  import { onMount } from "svelte";

  export let data;

  $: vehicle = data.vehicle;

  $: routes = data.routes.data;

  $: hotspots = data.hotspots.data;

  let hotspotOptions;
  let driverOptions;
  let routeOptions;
  let reservationOptions;
  let helperOptions;

  let editState = false;

  let busForm = {
    description: "Select one",
    starting_point: "Select one",
    route: "Select one",
    reservation: "Select one",
    driver: "Select one",
    helper: "Select one",
    name: "Select one",
    license: "Select one",
    time: "Select one",
  };

  function populateData(data) {
    if (!data) return;

    busForm.description = vehicle.description;
    busForm.name = vehicle.name;
    busForm.license = vehicle.license;

    hotspotOptions = hotspots.map(
      (elm) =>
        new Object({
          ...elm,
          value: elm._id,
          name: elm.name + ` - (${elm.location_name})`,
        }),
    );
    routeOptions = routes.map((elm) => new Object({ ...elm, value: elm._id }));
    reservationOptions = hotspots.map(
      (elm) => new Object({ ...elm, value: elm._id }),
    );
    driverOptions = hotspots.map(
      (elm) => new Object({ ...elm, value: elm._id }),
    );
    helperOptions = hotspots.map(
      (elm) => new Object({ ...elm, value: elm._id }),
    );
  }

  $: populateData(data);
  onMount(() => {});
</script>

<Section class="flex flex-col gap-0">
  <div class="w-full">
    <h1 class="font-semibold text-[#101828] text-3xl">
      {vehicle.name} <span class=" pl-2 text-xs">({vehicle._id})</span>
    </h1>
    <p class="font-normal text-[#475467] text-base mt-1">
      View the details of bus {vehicle.name}
    </p>
  </div>

  <Tab class="mt-6">
    <TabHeaders>
      <TabHeader>Information</TabHeader>
      <TabHeader>Extra</TabHeader>
    </TabHeaders>

    <TabBody>
      <TabPanel>
        <div class="w-full mx-auto grid grid-cols-2 lg:gap-x-28 gap-4 mt-6">
          <InputGroup flow="col" class="col-span-1">
            <FormFieldLabel>Name</FormFieldLabel>
            <Input disabled={!editState} bind:value={busForm.name} />
          </InputGroup>

          <InputGroup flow="col" class="col-span-1">
            <FormFieldLabel>License</FormFieldLabel>
            <Input disabled={!editState} bind:value={busForm.license} />
          </InputGroup>

          <InputGroup flow="col" class="col-span-2">
            <FormFieldLabel>Description</FormFieldLabel>
            <TextArea disabled={!editState} bind:value={busForm.description} />
          </InputGroup>

          <InputGroup flow="col">
            <FormFieldLabel>Starting point</FormFieldLabel>
            <SearchDropdown
              disabled={!editState}
              bind:value={busForm.starting_point}
              options={hotspotOptions}
            />
          </InputGroup>

          <InputGroup flow="col">
            <FormFieldLabel>Starting time</FormFieldLabel>
            <SearchDropdown
              disabled={!editState}
              bind:value={busForm.helper}
              options={helperOptions}
            />
          </InputGroup>

          <InputGroup flow="col">
            <FormFieldLabel>Route</FormFieldLabel>
            <SearchDropdown
              disabled={!editState}
              bind:value={busForm.route}
              options={routeOptions}
            />
          </InputGroup>

          <InputGroup flow="col">
            <FormFieldLabel>Reservation</FormFieldLabel>
            <SearchDropdown
              disabled={!editState}
              bind:value={busForm.reservation}
              options={reservationOptions}
            />
          </InputGroup>

          <InputGroup flow="col">
            <FormFieldLabel>Driver</FormFieldLabel>
            <SearchDropdown
              disabled={!editState}
              bind:value={busForm.driver}
              options={driverOptions}
            />
          </InputGroup>

          <InputGroup flow="col">
            <FormFieldLabel>Helper</FormFieldLabel>
            <SearchDropdown
              disabled={!editState}
              bind:value={busForm.helper}
              options={helperOptions}
            />
          </InputGroup>
        </div>

        <div class="flex gap-4 justify-end mt-5">
          {#if !editState}
            <Button
              onClick={() => {
                editState = true;
              }}
              class="w-max">Edit</Button
            >
          {:else}
            <Button onClick={() => {}} class="w-max">Update</Button>

            <Button
              onClick={() => {
                editState = false;
              }}
              class="w-max">Cancel</Button
            >
          {/if}
        </div>
      </TabPanel>

      <TabPanel>
        <Table>
          <TableFrame>
            <TableBody>
              <TableHeaderRow>
                <TableBodyHeader class="col-span-1">Date</TableBodyHeader>
                <TableBodyHeader class="col-span-1">Time</TableBodyHeader>
                <TableBodyHeader class="col-span-1">Amount</TableBodyHeader>
              </TableHeaderRow>

              {#each [] as item}
                <TableRow class="items-center ">
                  <TableCell
                    class="col-span-1 flex gap-3 font-normal text-sm text-[#475467]"
                    >{item.date}</TableCell
                  >
                  <TableCell
                    class="col-span-1 flex gap-3 font-normal text-sm text-[#475467]"
                    >{item.time}</TableCell
                  >
                  <TableCell
                    class="col-span-1 flex gap-3 font-normal text-sm text-[#475467]"
                    >{item.amount}</TableCell
                  >
                </TableRow>
              {/each}
            </TableBody>
          </TableFrame>
          <TableFooter>
            <Pagination totalItems={4} onPageChange={() => {}} />
          </TableFooter>
        </Table>
      </TabPanel>
    </TabBody>
  </Tab>
</Section>
