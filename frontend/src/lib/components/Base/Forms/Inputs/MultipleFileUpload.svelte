<script>
  // @ts-nocheck
  import InputFrame from "../Components/InputFrame.svelte";
  import { v4 as uuidv4 } from "uuid";
  import InputContainer from "../Components/InputContainer.svelte";
  import FileInput from "../Components/FileInput.svelte";
  import Attachment from "$components/Base/Attachment/Attachment.svelte";
  import CloseButton from "$components/Assets/CloseButton.svelte";
  import { twMerge } from "tailwind-merge";
  import Spinner from "$components/Base/Spinner.svelte";
  import { IconCircleCheck } from "@tabler/icons-svelte";
  import MultipleFileAttachment from "./MultipleFileAttachment.svelte";
  export let uploading;
  import { createEventDispatcher } from "svelte";

  const id = uuidv4();

  let attachment;
  let index;

  export let name = `file-${id}`;
  export let file = undefined;
  export let required;
  export let disabled = false;
  export let error = undefined;
  export let url = undefined;
  export let crossButton = true;
  export let fileTitle = true;
  export let videoFile = false;
  export let formData = {};
  export let onSelect = async (file) => {};
  const dispatch = createEventDispatcher();

  $: attachmentArray = [];
  let attachmentId = [];

  $: file = formData[name] || undefined;

  let image = false;

  $: uploading = file ? uploading : undefined;

  async function handleInput(e) {
    if (
      e?.target?.files[0]?.type === "image/png" ||
      e?.target?.files[0]?.type === "image/jpeg" ||
      e?.target?.files[0]?.type === "image/svg" ||
      e?.target?.files[0]?.type === "image/jpg"
    ) {
      file = e?.target?.files[0];
      image = true;
    } else {
      file = e?.target?.files[0];
      attachment = file;
    }

    uploading = true;

    let fileUpload = await onSelect(file);

    attachmentArray = [...attachmentArray, { file: file, id: fileUpload?.id }];

    uploading = false;
  }

  function handleRemove(id) {
    const index = attachmentArray.findIndex((file) => file?.id === id);

    if (index !== -1) {
      attachmentArray.splice(index, 1);
      dispatch("fileUploaded", id);
      attachmentArray = [...attachmentArray];
    }
  }
</script>

<div class="w-full h-full relative flex flex-col">
  {#if !image}
    <InputContainer {disabled} bind:error value={file}>
      <InputFrame
        fileHover="true"
        {error}
        {name}
        class="flex-col items-center justify-center "
      >
        <FileInput {file} {name} accept={"*"} {required} {handleInput}>
          {#if fileTitle}
            <p class="px-6 py-4 text-sm text-[#475467]">
              <span class="w-full text-sm font-semibold text-[#6941C6]"
                >Click to upload</span
              >
              <span class={videoFile ? "text-[#475467] font-normal" : ""}
                >or drag and drop</span
              >
              {#if !videoFile}
                files
              {:else}
                <p class="text-[#475467] font-normal text-xs text-center mt-1">
                  video file
                </p>
              {/if}
            </p>
          {:else}
            <p
              class="px-6 py-4 w-full max-w-72 text-center text-sm text-[#475467]"
            >
              <span class=" text-sm font-semibold text-[#175CD3]"
                >Click to upload</span
              > or drag and drop files pdf, doc or image files
            </p>
          {/if}
        </FileInput>
      </InputFrame>

      {#each attachmentArray as item}
        <MultipleFileAttachment
          attachment={item?.file}
          class="border-[#EAECF0]"
          handleFile={() => handleInput(undefined)}
          {handleRemove}
          id={item?.id}
        />
      {/each}
    </InputContainer>
  {/if}

  {#if image}
    <InputContainer
      class={twMerge("items-center", $$props.class)}
      {disabled}
      bind:error
      value={file}
    >
      {#if (file?.value && file?.value !== "") || (file && file !== "" && !file.error) || url}
        <div class="flex h-max w-max flex-col items-center justify-center">
          <img
            class="h-max max-h-[300px] w-max max-w-[300px] object-contain"
            src={url || URL.createObjectURL(file)}
            alt=""
          />
          <p class="text-xs">{file?.name || ""}</p>
        </div>

        {#if crossButton}
          <CloseButton
            onClick={() => {
              file = undefined;
              image = false;
            }}
            class="absolute right-0 top-0 rounded-md bg-transparent text-gray-400 hover:bg-gray-100 hover:text-gray-500 focus:bg-gray-100"
          />
        {/if}
      {/if}

      <InputFrame
        {error}
        {name}
        class="flex-col items-center justify-center {(file?.value &&
          file?.value !== '') ||
        (file && file !== '' && !file.error) ||
        url
          ? 'hidden'
          : ''}"
      >
        <FileInput
          {file}
          {name}
          accept={".png, .svg, .jpeg .jpg"}
          {required}
          {handleInput}
        >
          {#if fileTitle}
            <p class="px-6 py-4 text-sm text-[#475467]">
              <span class="w-full text-sm font-semibold text-[#175CD3]"
                >Click to upload</span
              > or drag and drop files
            </p>
          {:else}
            <p class="px-6 py-4 text-sm text-[#475467]">
              <span
                class="w-full text-sm text-center font-semibold text-[#175CD3]"
                >Click to upload</span
              > or drag and drop pdf, doc or image files
            </p>
          {/if}
        </FileInput>
      </InputFrame>

      <slot />
    </InputContainer>
  {/if}

  <div class="self-center w-[40px] top-[-2px] bg-transparent">
    {#if uploading}
      <Spinner class="relative  top-0 w-full bg-transparent" show={true} />
    {:else if uploading === false}
      <!-- <IconCircleCheck class="w-full relative top-0 mt-2" color="green" /> -->
    {/if}
  </div>
</div>
