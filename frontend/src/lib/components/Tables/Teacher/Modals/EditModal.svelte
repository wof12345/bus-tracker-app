<script lang="ts">
  import Modal from "$components/Base/Modal/Modal.svelte";

  export let modal: Modal;
  export let item: Teacher | undefined;
  export let onSave: () => void;

  const add = async () => {
    if (!item) return;

    const res = await user.update(userData, item.id);

    if (res?.data) {
      modal.hide();
      onSave();

      Object.keys(userData).forEach((key) => {
        (userData as any)[key] = "";
      });
    }
  };

  let userData: UserUpdate = {
    first_name: "",
    last_name: "",
    role: "",
    email: "",
  };

  const populateForm = (item: Teacher | undefined) => {
    userData.first_name = item?.first_name || "";
    userData.last_name = item?.last_name || "";
    userData.role = item?.role || "";
    userData.email = item?.email || "";
  };

  $: populateForm(item);
</script>

<Modal bind:this={modal}>
  <div class="px-6 py-6">
    <h1 class="text-lg font-semibold text-[#101828]">Edit</h1>
    <p class="text-sm text-[#475467]">Teachers help organize projects.</p>
    <div>
      <div
        class="relative mt-5 flex flex-col items-center justify-between gap-2"
      >
        <input
          placeholder="first name"
          class="shadow-input min-w-[370px] rounded-lg border-[1px] border-gray-300 px-6 py-2"
          type="text"
          bind:value={userData.first_name}
        />
        <input
          placeholder="last name"
          class="shadow-input min-w-[370px] rounded-lg border-[1px] border-gray-300 px-6 py-2"
          type="text"
          bind:value={userData.last_name}
        />
        <input
          placeholder="role"
          class="shadow-input min-w-[370px] rounded-lg border-[1px] border-gray-300 px-6 py-2"
          type="text"
          bind:value={userData.role}
        />
        <input
          placeholder="email"
          class="shadow-input min-w-[370px] rounded-lg border-[1px] border-gray-300 px-6 py-2"
          type="email"
          disabled
          bind:value={userData.email}
        />
      </div>
    </div>
    <div class="flex justify-between pt-11">
      <div class="">
        <button
          on:click={() => modal.hide()}
          class="cbtn text-base h-[44px] w-[170px] bg-white px-[18px] py-[10px] font-normal text-gray-700"
          >Cancel</button
        >
      </div>
      <div class="">
        <button
          on:click={add}
          class="abtn text-base h-[44px] w-[170px] bg-[#1570EF] px-[18px] py-[10px] font-semibold text-white"
          >Update</button
        >
      </div>
    </div>
  </div>
</Modal>

<style>
  .cbtn {
    border-radius: 8px;
    border: 1px solid var(--Gray-300, #d0d5dd);
    box-shadow: 0px 1px 2px 0px rgba(16, 24, 40, 0.05);
  }
  .abtn {
    border-radius: 8px;
    border: 1px solid var(--Primary-600, #1570ef);
    box-shadow: 0px 1px 2px 0px rgba(16, 24, 40, 0.05);
  }
</style>
