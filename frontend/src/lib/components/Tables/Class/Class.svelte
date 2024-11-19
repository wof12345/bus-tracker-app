<script lang="ts">
  import IconButton from "$components/Base/Buttons/IconButton.svelte";

  import DeleteModal from "./Modals/DeleteModal.svelte";
  import EditModal from "./Modals/EditModal.svelte";
  import Modal from "$components/Base/Modal/Modal.svelte";
  import CreateModal from "./Modals/CreateModal.svelte";
  import { page } from "$app/stores";
  import { browser } from "$app/environment";
  import { onMount } from "svelte";
  import TextIconButton from "$components/Base/Buttons/Button.svelte";

  import Pagination from "$components/Base/Table/Components/Pagination.svelte";

  let data: DataCollection = [];

  type DataCollection = CourseResponse[];

  let pageSize = 5;
  let totalItems: number = 0;
  $: skip = $page.url.searchParams.get("skip") || "0";
  $: limit = $page.url.searchParams.get("limit") || pageSize + "";

  async function fetchData(skip: string = "0") {
    if (!browser) return;

    const res = await course.get_all(skip, limit);

    if (res.data) {
      data = res.data.data;
      totalItems = res.data.total;
    }
  }

  let refer: CourseResponse | undefined;
  $: lastRefer = refer;

  async function delete_action(id: number | undefined) {
    if (!id) return;

    const res = await course.delete_one(id);

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
</script>

<div class="my-5 flex justify-between">
  <div class="flex flex-col gap-y-1">
    <h1 class="text-3xl font-semibold leading-9 text-[#101828]">Classes</h1>
    <p class="text-base font-normal text-[#475467]">
      Efficiently Manage and Organize Classes
    </p>
  </div>
  <div>
    <TextIconButton
      src={"/table/plus.svg"}
      text={"Add Class"}
      onClick={() => createModal.show()}
    />
  </div>
</div>

<div
  class="mb-24 rounded-lg border-[1px] border-gray-200 shadow-table-container"
>
  <div
    class={` flex items-center justify-between rounded-t-lg border-y  bg-white px-6 py-3  `}
  >
    <p class="w-full flex-1 text-xs font-medium text-[#475467]">Title</p>
    <p class="w-full flex-1 text-xs font-medium text-[#475467]">Description</p>
    <p class="w-full flex-1 text-xs font-medium text-[#475467]"></p>
  </div>

  {#each data as item, idx}
    <div
      class={`flex items-center justify-between border-y px-6  py-4 ${
        (idx + 1) % 2 == 0 && "bg-gray-50"
      } ${(idx + 1) % 2 == 0 && "bg-white"}`}
    >
      <p class="w-full flex-1 text-sm text-[#475467]">{item.title}</p>
      <p class="w-full flex-1 text-sm text-[#475467]">{item.description}</p>

      <div class="flex w-40 flex-1 justify-end">
        <IconButton
          className="w-9 p-2"
          src={"/delete.svg"}
          onClick={() => {
            deleteModal.show();
            lastRefer = item;
          }}
        />
        <IconButton
          className="w-9 p-2"
          src={"/edit.svg"}
          onClick={() => {
            editModal.show();
            lastRefer = item;
          }}
        />
      </div>
    </div>
  {/each}
  <Pagination {totalItems} {pageSize} onPageChange={(page) => {}} />
</div>

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
