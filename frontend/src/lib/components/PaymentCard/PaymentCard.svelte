<script>
  import { deserialize } from "$app/forms";
  import { invalidateAll } from "$app/navigation";
  import Button from "$components/Base/Buttons/Button.svelte";
  import Paragraph from "$components/Base/Typography/Paragraph.svelte";
  import { validateApiResponse } from "$components/utils/validateApiResponse";
  import { showSpinner } from "$lib/store/spinner";
  import { IconArrowRight, IconBook } from "@tabler/icons-svelte";
  export let mainData;
  export let role;
  $: status = mainData?.order?.status;
  $: orderId = mainData?.order?.id;

  async function updateOrderStatus(status) {
    const formData = new FormData();

    formData.append("order_id", orderId);
    formData.append("status", status);

    const response = await showSpinner(
      fetch("messages?/updateOrderStatus", {
        method: "POST",
        body: formData,
      }),
    );

    const result = deserialize(await response.text());
    if (!validateApiResponse(result)) {
      return;
    }
    await invalidateAll();
  }
</script>

<div class="w-full max-w-[436px] bg-white">
  <div
    class="flex flex-col md:flex-row justify-between w-full md:items-center gap-2 border-b-2 p-4"
  >
    <Paragraph class="font-medium text-lg leading-7"
      >{mainData?.service?.category_name || " "}</Paragraph
    >
    <div class="flex flex-row space-x-2 items-center">
      <Paragraph class="font-medium text-md leading-6"
        >AED {mainData?.order?.price || ""}</Paragraph
      >

      <Paragraph>{mainData?.service?.medium || ""}</Paragraph>
    </div>
  </div>
  <div class="p-4">
    <div
      class="bg-rose-50 text-center text-xs rounded-xl max-w-24 font-semibold text-rose-700 border-2 border-rose-200"
    >
      {status || ""}
    </div>
    <div
      class="my-4 flex md:flex-row flex-col gap-y-2 md:gap-y-0 md:space-x-3 md:items-center"
    >
      <Paragraph class="text-md font-medium text-gray-700"
        >Offer includes:
      </Paragraph>
      <Paragraph class="text-md text-gray-700 flex gap-x-1   "
        ><IconBook class="h-5 w-5 text-gray-500" />
        {mainData?.total_sessions || ""} lessons</Paragraph
      >
    </div>
    <Paragraph class="text-md text-rose-600 font-semibold mb-2 cursor-pointer"
      >View schedule</Paragraph
    >
  </div>
  {#if role === "teacher" && status === "Pending"}
    <div class="p-4 flex gap-x-4 border-t-2">
      <Button
        onClick={() => updateOrderStatus("Rejected")}
        class="bg-white text-gray-600 border-gray-300 hover:bg-rose-500 hover:text-white"
        >Decline</Button
      >
      <Button
        onClick={() => updateOrderStatus("Approved")}
        class="text-gray-600 bg-rose-400 hover:bg-rose-500 hover:text-white"
        >Accept</Button
      >
    </div>
  {:else if role === "student" && status === "Pending"}
    <div class="p-4 border-t-2">
      <Button
        onClick={() => updateOrderStatus("FullRefund")}
        class="bg-white text-gray-600 border-gray-300 hover:bg-rose-500 hover:text-white"
        >Withdraw offer</Button
      >
    </div>
  {:else if role === "student" && status === "Failed"}
    <div class="p-4 text-md font-semibold border-t-2">
      <Paragraph class="text-md font-semibold flex">
        <span class="md:whitespace-nowrap">Click here to pay manually:</span>
        <span class="text-rose-600 ml-1">
          <a href="https://stripe.com" class="break-all"
            >https://buy.stripe.com/test</a
          >
        </span>
      </Paragraph>
    </div>
  {:else if status === "Approved"}
    <a
      href="/orders/{orderId}"
      class="p-4 flex items-center justify-end text-rose-600 text-sm font-semibold gap-x-1 border-t-2"
    >
      Goto order <IconArrowRight />
    </a>
  {/if}
</div>
