<script>
  import Modal from "$components/Base/Modal/Modal.svelte";

  export let modal;
  export let onDelete;
</script>

<Modal bind:this={modal}>
  <div class="px-6 py-6">
    <h1 class="text-lg font-semibold text-[#101828]">
      Are you sure you want to delete?
    </h1>

    <div class="flex gap-3 pt-11">
      <div class="">
        <button
          on:click={() => {
            modal.hide();
          }}
          class="cbtn text-base h-[44px] w-[170px] bg-white px-[18px] py-[10px] font-normal text-gray-700"
          >Cancel</button
        >
      </div>
      <div class="">
        <button
          on:click={() => {
            onDelete();
          }}
          class="abtn text-base hover:bg-[#B42318] h-[44px] w-[170px] bg-[#D92D20] px-[18px] py-[10px] font-semibold text-white"
          >Delete</button
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
    border: 1px solid var(--Primary-600, #d92d20);
    box-shadow: 0px 1px 2px 0px rgba(16, 24, 40, 0.05);
  }
</style>
