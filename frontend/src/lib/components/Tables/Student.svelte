<script>
  import Modal from "$components/Base/Modal/Modal.svelte";
  import Table from "$components/Base/Table/Table.svelte";
  import TableHeaderRow from "$components/Base/Table/TableHeaderRow.svelte";
  import TableBodyHeader from "$components/Base/Table/TableBodyHeader.svelte";
  import TableBody from "$components/Base/Table/TableBody.svelte";
  import TableRow from "$components/Base/Table/TableRow.svelte";
  import TableCell from "$components/Base/Table/TableCell.svelte";
  import TableFooter from "$components/Base/Table/TableFooter.svelte";
  import InputGroup from "$components/Base/Forms/Components/InputGroup.svelte";
  import Input from "$components/Base/Forms/Inputs/Input.svelte";
  import InputIcon from "$components/Base/Forms/Components/InputIcon.svelte";
  import Pagination from "$components/Base/Table/Components/Pagination.svelte";
  import TableHeader from "./Components/TableHeader.svelte";
  import TableBadge from "$components/Base/Table/Components/TableBadge.svelte";
  import TableFrame from "$components/Base/Table/TableFrame.svelte";
  import Filter from "../Base/Table/Components/Filter.svelte";
  import FilterModal from "./Components/Modals/FilterModal.svelte";
  import TableButton from "$components/Base/Table/Components/TableButton.svelte";

  export let students = [];

  let editModal;
  let deleteModal;
  let createModal;
  let filterModal;

  let users = [
    {
      name: "Adnan",
      email: "arafadnan10@gmail.com",
      date: "Jan 6, 2022",
      courses: ["Marketing", "CSE"],
    },
  ];
</script>

<TableHeader title={"Students"} subtitle={""}>
  <div
    slot="below-head"
    class="flex flex-row flex-wrap items-start justify-between gap-2 md:items-center"
  >
    <Filter onClick={() => filterModal.show()} />

    <InputGroup class="xs:max-w-sm w-full bg-white">
      <Input name={"data1"} label={"Search for a student"}>
        <InputIcon class="ml-1" src="/search.png" />
      </Input>
    </InputGroup>
  </div>
</TableHeader>

<Table class="mt-6">
  <TableFrame>
    <TableBody>
      <TableHeaderRow>
        <TableBodyHeader class="col-span-2 md:col-span-4">Name</TableBodyHeader>
        <TableBodyHeader class=" col-span-3">Email address</TableBodyHeader>
        <TableBodyHeader class="col-span-2 ">Enrolled</TableBodyHeader>
        <TableBodyHeader class="col-span-2 ">Course</TableBodyHeader>
        <TableBodyHeader class="col-span-1"></TableBodyHeader>
      </TableHeaderRow>
      {#each students as item}
        <TableRow class="items-center ">
          <TableCell
            class="text-md col-span-2 flex gap-3 font-medium text-[#101828] md:col-span-4"
          >
            <a href={`/students/${item.id}`}
              >{item.first_name + " " + item.last_name}</a
            >
          </TableCell>

          <TableCell class="col-span-3 text-sm font-normal text-[#475467]"
            >{item.email}</TableCell
          >
          <TableCell class="col-span-2"
            >{item?.date ? item.date : "N/A"}</TableCell
          >
          <TableCell class="col-span-2">
            <TableBadge class="" text={"Design"} />
          </TableCell>

          <TableCell class="col-span-1 flex justify-end gap-2 overflow-visible">
            <TableButton src={"/message.png"}></TableButton>
            <TableButton src={"/eye.png"}></TableButton>
          </TableCell>
        </TableRow>
      {/each}
    </TableBody>
  </TableFrame>

  <TableFooter
    ><Pagination
      totalItems={users.length}
      onPageChange={(page) => {}}
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
