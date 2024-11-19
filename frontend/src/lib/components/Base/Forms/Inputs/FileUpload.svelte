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

  const id = uuidv4();

  let attachment;

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
  export let uploading;
  export let value;

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
    value = file;

    let fileUpload = await onSelect(file);

    uploading = false;
  }
</script>

<div class="relative flex h-full w-full flex-col">
  {#if !image}
    <InputContainer {disabled} bind:error {value}>
      <InputFrame
        fileHover="true"
        {error}
        {name}
        class="flex-col items-center justify-center {file ? 'hidden' : ''}"
      >
        <FileInput {file} {name} accept={"*"} {required} {handleInput}>
          {#if fileTitle}
            <p class="px-6 py-4 text-sm text-[#475467]">
              <span class="w-full text-sm font-semibold text-[#6941C6]"
                >Click to upload</span
              >
              <span class={videoFile ? "font-normal text-[#475467]" : ""}
                >or drag and drop</span
              >
              {#if !videoFile}
                files
              {:else}
                <p class="mt-1 text-center text-xs font-normal text-[#475467]">
                  video file
                </p>
              {/if}
            </p>
          {:else}
            <p
              class="w-full max-w-72 px-6 py-4 text-center text-sm text-[#475467]"
            >
              <span class=" text-sm font-semibold text-[#175CD3]"
                >Click to upload</span
              > or drag and drop files pdf, doc or image files
            </p>
          {/if}
        </FileInput>
      </InputFrame>

      {#if file}
        <Attachment
          {attachment}
          class="border-[#EAECF0]"
          handleFile={() => handleInput(undefined)}
          {file}
          handleRemove={() => handleInput(undefined)}
        />
      {/if}
    </InputContainer>
  {/if}

  {#if image}
    <InputContainer
      class={twMerge("items-center", $$props.class)}
      {disabled}
      bind:error
      {value}
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
                class="w-full text-center text-sm font-semibold text-[#175CD3]"
                >Click to upload</span
              > or drag and drop pdf, doc or image files
            </p>
          {/if}
        </FileInput>
      </InputFrame>

      <slot />
    </InputContainer>
  {/if}

  <div class="top-[-2px] w-[40px] self-center bg-transparent">
    {#if uploading}
      <Spinner class="relative  top-0 w-full bg-transparent" show={true} />
    {:else if uploading === false}
      <IconCircleCheck class="relative top-0 mt-2 w-full" color="green" />
    {/if}
  </div>
</div>
