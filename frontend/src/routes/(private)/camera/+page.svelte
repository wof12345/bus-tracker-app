<script>
  import { showSpinner } from "$lib/store/spinner.js";
  import Section from "$components/Base/Layout/Section.svelte";

  import TableHeader from "$components/Tables/Components/TableHeader.svelte";
  import FileUpload from "$components/Base/Forms/Inputs/FileUpload.svelte";
  import InputGroup from "$components/Base/Forms/Components/InputGroup.svelte";
  import FormFieldLabel from "$components/Base/Forms/Components/FormFieldLabel.svelte";
  import Button from "$components/Base/Buttons/Button.svelte";
  import { validateInput } from "$components/utils/validation/validation";
  import { deserialize } from "$app/forms";
  import { validateApiResponse } from "$components/utils/validateApiResponse";
  import { invalidateAll } from "$app/navigation";
  import Header from "$components/Base/Typography/Header.svelte";
  import Paragraph from "$components/Base/Typography/Paragraph.svelte";

  export let data;

  let vehicles = [];

  let urlForm = {
    url: undefined,
    file: undefined,
  };

  function handleVideoUrl(file) {
    urlForm.url = undefined;

    if (!file) return;

    urlForm.url = URL.createObjectURL(file);
  }

  async function process() {
    let form = new FormData();

    if (!validateInput(urlForm, ["file"])) {
      userCreateForm = userCreateForm;

      showToaster("Empty required fields");
      return;
    }

    form.append("file", urlForm.file);

    const response = await showSpinner(
      fetch(`?/process`, {
        method: "POST",
        body: form,
      }),
    );

    const data = deserialize(await response.text());

    if (!validateApiResponse(data)) {
      return;
    }
    vehicles = data.data;

    await invalidateAll();
  }

  $: handleVideoUrl(urlForm.file);
</script>

<Section class="flex flex-col gap-3 h-full">
  <TableHeader
    class="mb-3"
    title="Camera feed"
    subtitle="When integrated with an actual camera, the video will be streamed as bytes from camera to the backend and from backend to frontend via websocket. This is just a demo with a fixed video upload method."
  />

  <div class="grid grid-cols-2 gap-2 h-full items-center content-center">
    <video class="mx-auto max-h-[400px]" src={urlForm.url} controls>
      <track kind="captions" />
    </video>

    <div class="max-w-[400px] mx-auto flex flex-col gap-2">
      <InputGroup flow="col">
        <FormFieldLabel
          >Upload a video file to run the tracking process on:</FormFieldLabel
        >
        <FileUpload bind:file={urlForm.file} />
      </InputGroup>

      <Paragraph class="text-xs">
        <span class="font-bold">
          Pre-trained model for Object Detection <a
            href="https://docs.ultralytics.com/">YOLOv8</a
          >. <br />
          OCR used paddle-ocr with paddle-paddle cpu instance model <br />
          Current image processing methods to extract license plates from images
          are :
        </span>

        <ul style="list-style-type:circle" class="pt-2">
          <li>CLAHE (Contrast Limited Adaptive Histogram Equalization)</li>
          <li>Gray scale</li>
          <li>Otsu Threshold</li>
          <li>Erosion (Single iteration of 3x3 kernal based)</li>
          <li>Dilation (Single iteration of 3x3 kernal based)</li>
        </ul>
      </Paragraph>

      <Button onClick={() => process()} class="w-max">Process</Button>
    </div>
  </div>

  {#if vehicles?.length > 0}
    <div class="flex flex-col gap-3">
      <Header>Buses detected that is in records:</Header>

      <div class="flex flex-col gap-3">
        {#each vehicles as vehicle}
          <div class="flex gap-2 justify-between hover:bg-gray-100">
            <div>Name : {vehicle.name}</div>
            <div>License : {vehicle.license}</div>
            <div>In-campus : {vehicle.in_campus ? "Yes" : "No"}</div>
            <div>Status : {vehicle.status}</div>
          </div>
        {/each}
      </div>
    </div>
  {/if}
</Section>
