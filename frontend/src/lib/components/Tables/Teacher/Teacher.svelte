<script lang="ts">
  // import ButtonVariant from '$components/Base/Buttons/ButtonVariant.svelte';
  import IconButton from "$components/Base/Buttons/IconButton.svelte";

  import DeleteModal from "./Modals/DeleteModal.svelte";
  import EditModal from "./Modals/EditModal.svelte";
  import CreateModal from "./Modals/CreateModal.svelte";
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
  import Header from "$components/Base/Typography/Header.svelte";
  import Paragraph from "$components/Base/Typography/Paragraph.svelte";
  import Button from "$components/Base/Buttons/Button.svelte";
  import InputGroup from "$components/Base/Forms/Components/InputGroup.svelte";

  import Input from "$components/Base/Forms/Inputs/Input.svelte";
  import InputIcon from "$components/Base/Forms/Components/InputIcon.svelte";
  import Pagination from "$components/Base/Table/Components/Pagination.svelte";
  import TableHeader from "../Components/TableHeader.svelte";
  import TableBadge from "$components/Base/Table/Components/TableBadge.svelte";
  import TableFrame from "$components/Base/Table/TableFrame.svelte";

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

  let editModal: Modal;
  let deleteModal: Modal;
  let createModal: Modal;

  let users = [
    {
      name: "Adnan Araf",
      email: "arafadnan10@gmail.com",
      date: "11/11/2024",
      courses: ["Marketing", "CSE"],
    },
  ];
</script>

<TableHeader
  title={"Teachers"}
  subtitle={"Efficiently manage and organise your teaching staffs."}
>
  <div slot="below-head">
    <InputGroup>
      <Input name={"data1"} label={"Search for a teacher"}>
        <InputIcon class="ml-1" src="/search.png" />
      </Input>
    </InputGroup>
  </div>

  <div class="flex gap-3">
    <Button src={"/upload.png"} variant={"secondary"} type={"button"}
      >Import</Button
    >
    <Button variant={"primary"} src={"/plus.png"} type={"button"}
      >Add teacher</Button
    >
  </div>
</TableHeader>

<Table>
  <TableFrame>
    <TableBody>
      <TableHeaderRow>
        <TableBodyHeader class="col-span-4">Name</TableBodyHeader>
        <TableBodyHeader class=" col-span-3">Email address</TableBodyHeader>
        <TableBodyHeader class="col-span-2 ">Date joined</TableBodyHeader>
        <TableBodyHeader class="col-span-2 ">Courses</TableBodyHeader>
        <TableBodyHeader class="col-span-1"></TableBodyHeader>
      </TableHeaderRow>
      {#each users as item}
        <TableRow class="items-center ">
          <TableCell class="col-span-4 flex gap-3 font-medium text-[#101828]">
            {item.name}
          </TableCell>

          <TableCell class="col-span-3  text-sm font-normal text-[#475467] "
            >{item.email}</TableCell
          >
          <TableCell class="col-span-2  text-sm font-normal text-[#475467] "
            >{item.date}</TableCell
          >

          <TableCell
            class="col-span-2 gap-1 rounded-2xl px-0.5 py-2 text-xs font-normal "
          >
            <TableBadge class="bg-[#EEF4FF]" text={"CSE"} />
            <TableBadge class="" text={"Design"} />
          </TableCell>

          <TableCell class="col-span-1 flex justify-end gap-3">
            <IconButton src={"/Delete.png"}></IconButton>
            <IconButton src={"/Icon (1).svg"}></IconButton>
          </TableCell>
        </TableRow>
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
/>
