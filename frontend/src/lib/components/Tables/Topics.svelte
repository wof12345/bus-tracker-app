<script lang="ts">
  export let courses: any;
  export let total: number;

  import Modal from "$components/Base/Modal/Modal.svelte";
  import { page } from "$app/stores";
  import { browser } from "$app/environment";
  import { onMount } from "svelte";

  import Table from "$components/Base/Table/Table.svelte";
  import TableHeaderRow from "$components/Base/Table/TableHeaderRow.svelte";
  import TableBodyHeader from "$components/Base/Table/TableBodyHeader.svelte";
  import TableBody from "$components/Base/Table/TableBody.svelte";
  import TableRow from "$components/Base/Table/TableRow.svelte";
  import TableCell from "$components/Base/Table/TableCell.svelte";
  import TableFooter from "$components/Base/Table/TableFooter.svelte";
  import Paragraph from "$components/Base/Typography/Paragraph.svelte";
  import Button from "$components/Base/Buttons/Button.svelte";
  import Pagination from "$components/Base/Table/Components/Pagination.svelte";
  import TableHeader from "./Components/TableHeader.svelte";
  import TableFrame from "$components/Base/Table/TableFrame.svelte";
  import FilterModal from "./Components/Modals/FilterModal.svelte";
  import TableButton from "$components/Base/Table/Components/TableButton.svelte";

  let data: DataCollection = [];

  type DataCollection = Teacher[];

  let pageSize = 5;
  let totalItems: number = 0;
  $: skip = $page.url.searchParams.get("skip") || "0";
  $: limit = $page.url.searchParams.get("limit") || pageSize + "";

  async function fetchData(skip: string = "0") {
    if (!browser) return;

    const res = await user.get_all_by_role("teacher", skip, limit);

    if (res.data) {
      data = res.data.data;
      totalItems = res.data.total;
    }
  }

  let refer: Teacher | undefined;
  $: lastRefer = refer;

  // async function delete_action(id: number | undefined) {
  // 	if (!id) return;

  // 	const res = await user.delete_one(id);

  // 	if (res.status === 204) {
  // 		lastRefer = undefined;
  // 		fetchData();
  // 	}
  // }

  $: fetchData(skip);

  onMount(async () => {
    fetchData();
  });

  let editModal: Modal;
  let deleteModal: Modal;
  let createModal: Modal;
  let filterModal: FilterModal;

  let users = [
    {
      name: "Physics",
      enroll: "4",
      earnings: "AED 450",
      average: "4.3",
    },
    {
      name: "Chemistry",
      enroll: "4",
      earnings: "AED 450",
      average: "4.3",
    },
    {
      name: "Math",
      enroll: "4",
      earnings: "AED 450",
      average: "4.3",
    },
    {
      name: "English",
      enroll: "4",
      earnings: "AED 450",
      average: "4.3",
    },
    {
      name: "Bangla",
      enroll: "4",
      earnings: "AED 450",
      average: "4.3",
    },
  ];
</script>

<div class="flex flex-col justify-between md:flex-row">
  <TableHeader title={"Topics"} subtitle={"Manage your topics efficiently."}>
    <div
      slot="below-head"
      class="flex flex-row flex-wrap items-start justify-between gap-2 md:items-center"
    ></div>
  </TableHeader>

  <Button class="w-48 gap-2">
    <img class="h-3 w-3" src="/plus.svg" alt="/" />
    <Paragraph class="font-semibold text-white md:text-sm"
      >Teach a topc</Paragraph
    >
  </Button>
</div>
<Table class="mt-6">
  <TableFrame>
    <TableBody>
      <TableHeaderRow>
        <TableBodyHeader class="col-span-2 md:col-span-4">Name</TableBodyHeader>
        <TableBodyHeader class=" col-span-2">Enrolled students</TableBodyHeader>
        <TableBodyHeader class="col-span-2 ">Total earnings</TableBodyHeader>
        <TableBodyHeader class="col-span-2 ">Average ratings</TableBodyHeader>
        <TableBodyHeader class="col-span-1"></TableBodyHeader>
      </TableHeaderRow>
      {#each courses as item}
        <TableRow class="items-center ">
          <TableCell
            class="col-span-2 flex gap-3 text-md font-medium text-[#101828] md:col-span-4"
          >
            {item.title}
          </TableCell>

          <TableCell class="col-span-2 text-sm font-normal text-[#475467]"
            >{item?.enroll ? item.enroll : "N/A"}</TableCell
          >
          <TableCell class="col-span-2"
            >{item?.earnings ? item.earnings : "N/A"}</TableCell
          >
          <TableCell class="col-span-2">
            {item?.average ? item.average : "N/A"}
          </TableCell>

          <TableCell class="col-span-1 flex justify-end gap-2">
            <TableButton src={"/message.png"}></TableButton>
            <TableButton src={"/eye.png"}></TableButton>
          </TableCell>
        </TableRow>
      {/each}
    </TableBody>
  </TableFrame>

  <TableFooter
    ><Pagination
      totalItems={total}
      onPageChange={(page) => {
        fetchData(page);
      }}
    /></TableFooter
  >
</Table>

<!-- <DeleteModal
	bind:modal={deleteModal}
	onDelete={() => {
		deleteModal.hide();
		delete_action(lastRefer?.id);
	}}
/>

<EditModal
	bind:modal={editModal}
	bind:item={lastRefer}
	onSave={() => {
		editModal.hide();
		fetchData();
	}}
/>

<CreateModal
	bind:modal={createModal}
	onAdd={() => {
		fetchData();
	}}
/> -->
