<script lang="ts">
  import Modal from "$components/Base/Modal/Modal.svelte";

  export let modal: Modal;
  export let onAdd: () => void;

  const add = async () => {
    const res = await user.create(userData);

    if (res?.data) {
      modal.hide();
      onAdd();

      Object.keys(userData).forEach((key) => {
        (userData as any)[key] = "";
      });
    }
  };

  let userData: User = {
    first_name: "",
    last_name: "",
    role: "",
    email: "",
    password: "",
  };
</script>

<Modal bind:this={modal}>
  <div class="px-6 py-6">
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
          bind:value={userData.email}
        />
        <input
          placeholder="password"
          class="shadow-input min-w-[370px] rounded-lg border-[1px] border-gray-300 px-6 py-2"
          type="text"
          bind:value={userData.password}
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
          >Add</button
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
