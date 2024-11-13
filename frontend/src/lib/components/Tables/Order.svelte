<script lang="ts">
  import { page } from "$app/stores";
  import { browser } from "$app/environment";
  import { onMount } from "svelte";

  export let orders: any;
  export let total: number;

  import Table from "$components/Base/Table/Table.svelte";
  import TableHeaderRow from "$components/Base/Table/TableHeaderRow.svelte";
  import TableBodyHeader from "$components/Base/Table/TableBodyHeader.svelte";
  import TableBody from "$components/Base/Table/TableBody.svelte";
  import TableRow from "$components/Base/Table/TableRow.svelte";
  import TableCell from "$components/Base/Table/TableCell.svelte";
  import TableFooter from "$components/Base/Table/TableFooter.svelte";
  import Pagination from "$components/Base/Table/Components/Pagination.svelte";
  import TableHeader from "./Components/TableHeader.svelte";
  import TableFrame from "$components/Base/Table/TableFrame.svelte";
  import FilterModal from "./Components/Modals/FilterModal.svelte";
  import Avatar from "$components/Base/Avatar.svelte";

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

  async function delete_action(id: number | undefined) {
    if (!id) return;

    const res = await user.delete_one(id);

    if (res.status === 204) {
      lastRefer = undefined;
      fetchData();
    }
  }

  $: fetchData(skip);

  onMount(async () => {
    fetchData();
  });
  let filterModal: FilterModal;

  let users = [
    {
      order: "1234",
      name: "Physics with Olivia",
      username: "@olivia232",
      teacher: "Olivia Rhye",
      date: "Jan 6, 2022",
      imgUrl: "/secAvatar.svg",
    },
    {
      order: "1234",
      name: "Physics with Olivia",
      username: "@olivia232",
      teacher: "Olivia Rhye",
      date: "Jan 6, 2022",
      imgUrl: "/secAvatar.svg",
    },
    {
      order: "1234",
      name: "Physics with Olivia",
      username: "@olivia232",
      teacher: "Olivia Rhye",
      date: "Jan 6, 2022",
      imgUrl: "/secAvatar.svg",
    },
    {
      order: "1234",
      name: "Physics with Olivia",
      username: "@olivia232",
      teacher: "Olivia Rhye",
      date: "Jan 6, 2022",
      imgUrl: "/secAvatar.svg",
    },
  ];
</script>

<TableHeader title={"Orders"} subtitle={"Manage your orders efficiently."}
></TableHeader>

<Table class="mt-6">
  <TableFrame>
    <TableBody>
      <TableHeaderRow>
        <TableBodyHeader class="col-span-2">Orders</TableBodyHeader>
        <TableBodyHeader class="col-span-2 md:col-span-4">Name</TableBodyHeader>
        <TableBodyHeader class=" col-span-3">Teacher</TableBodyHeader>
        <TableBodyHeader class="col-span-2 ">First session</TableBodyHeader>
        <TableBodyHeader class="col-span-1"></TableBodyHeader>
      </TableHeaderRow>
      {#each users as item}
        <a href={`/orders/${item.order}`}>
          <TableRow class="items-center ">
            <TableCell
              class="col-span-2 flex gap-3 font-medium text-[#101828] "
            >
              <a href={`/orders/${item.order}`}>#{item.order}</a>
            </TableCell>
            <TableCell
              class="text-md col-span-2 flex gap-3 font-medium text-[#101828] md:col-span-4"
            >
              {item.name}
            </TableCell>

            <TableCell
              class="col-span-3 flex gap-x-2 text-sm font-normal text-[#475467]"
            >
              <Avatar class="h-11 w-11 p-0" src={item.imgUrl} />
              <div>
                <div class="text-md flex gap-3 font-medium text-[#101828]">
                  {item.teacher}
                </div>
                <div class="text-sm font-normal text-gray-600">
                  {item.username}
                </div>
              </div>
            </TableCell>
            <TableCell class="col-span-2">{item.date}</TableCell>
            <a href={`/students/${item.name}`}>
              <TableCell
                class="col-span-1   overflow-visible text-sm font-semibold text-gray-600  "
              >
                <div
                  class="hover:rounded-lg hover:bg-white hover:px-1 hover:py-1 hover:text-gray-800"
                >
                  Cancel
                </div>
              </TableCell>
            </a>
          </TableRow>
        </a>
      {/each}
    </TableBody>
  </TableFrame>

  <TableFooter
    ><Pagination
      totalItems={users.length}
      onPageChange={(page) => {
        fetchData(page);
      }}
    /></TableFooter
  >
</Table>

<!-- 
<DeleteModal
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

<FilterModal bind:modal={filterModal} />
