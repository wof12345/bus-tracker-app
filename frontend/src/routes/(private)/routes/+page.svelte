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
  import { invalidateAll, goto } from "$app/navigation";
  import { showToaster } from "$lib/store/toaster.ts";
  import { validateApiResponse } from "$components/utils/validateApiResponse";
  import { deserialize } from "$app/forms";
  import TableButton from "$components/Base/Table/Components/TableButton.svelte";
  import { IconTrash, IconEdit, IconEye } from "@tabler/icons-svelte";
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
  import Badge from "$components/Base/Badge.svelte";
  import { authStore, isAdmin, isManager } from "$lib/store/auth";

  export let data;

  $: routes = data?.routes;

  let selectedRoute;
  let selectedRouteRef;

  $: console.log(routes);

  function selectItem(item) {
    selectedRoute = item;
    selectedRouteRef = JSON.parse(JSON.stringify(item));
  }
</script>

<Section class="flex flex-col gap-0 h-full">
  <TableHeader class="mb-3" title="Routes" subtitle="Manage route routes">
    <div slot="below-head">
      {#if isAdmin($authStore) || isManager($authStore)}
        <Button
          onClick={() => {
            goto(`/routes/create`);
          }}>+ Add new route</Button
        >
      {/if}
    </div>
  </TableHeader>

  <Table>
    <TableFrame>
      <TableBody>
        <TableHeaderRow>
          <TableBodyHeader class="col-span-1">Name</TableBodyHeader>
          <TableBodyHeader class="col-span-1">Description</TableBodyHeader>
          <TableBodyHeader class="col-span-1">Hotspots</TableBodyHeader>
          <TableBodyHeader class="col-span-1"></TableBodyHeader>
        </TableHeaderRow>

        {#each routes?.data || [] as item}
          <TableRow
            onClick={() => {}}
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
              class="col-span-1 flex gap-1.5 font-normal text-sm text-[#475467]"
            >
              {#each item.hotspots as hotspot, idx (idx)}
                {#if idx <= 2}
                  <Badge class="bg-primary-500 text-white">
                    {hotspot.name}
                  </Badge>
                {:else}
                  .
                {/if}
              {/each}
            </TableCell>
            <TableCell
              class="col-span-1 flex justify-end gap-3 font-normal text-sm text-[#475467]"
            >
              <TableButton
                onClick={(e) => {
                  selectItem(item);
                  goto(`/routes/${item._id}/edit`);

                  e.stopPropagation();
                }}><IconEye /></TableButton
              >
              {#if isAdmin($authStore) || isManager($authStore)}
                <TableButton
                  onClick={(e) => {
                    selectItem(item);
                    goto(`/routes/${item._id}/edit`);

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

                    showToaster("Hotspot deleted");
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
      <Pagination totalItems={routes?.total || 0} onPageChange={() => {}} />
    </TableFooter>
  </Table>
</Section>
