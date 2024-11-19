<script lang="ts">
  import { twMerge } from "tailwind-merge";
  import FileInput from "../Components/FileInput.svelte";
  import InputContainer from "../Components/InputContainer.svelte";
  import InputFrame from "../Components/InputFrame.svelte";
  import { v4 as uuidv4 } from "uuid";
  import CloseButton from "$components/Assets/CloseButton.svelte";

  const id = uuidv4();

  export let name: any = `file-${id}`;
  export let file: any;
  export let url: any = undefined;
  export let required: boolean = true;
  export let disabled: boolean = false;
  export let imgTitle: boolean = false;
  export let error: any = undefined;
  export let crossButton: boolean = true;
  export let formData: any = {};
  export let onSelect: any = (file: File) => {};

  export let backupUrl = url;

  $: file = formData[name] || undefined;

  function handleInput(e: any) {
    file = e?.target?.files[0];

    onSelect(file);
  }
</script>

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
          backupUrl = url;

          url = "";
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
    fileHover="true"
  >
    <FileInput
      {file}
      {name}
      accept={".png, .svg, .jpeg .jpg"}
      {required}
      {handleInput}
    >
      <p
        class="px-6 py-4 text-sm text-[#475467] text-center {imgTitle
          ? 'font-normal'
          : ''} "
      >
        <span class="w-full text-sm font-semibold text-[#175CD3]"
          >Click to upload</span
        >
        or drag and drop
        {#if !imgTitle}
          files
        {:else}
          <br />
          <span class="text-[#475467] font-normal text-xs">
            SVG, PNG, JPG or GIF (max. 800x400px)
          </span>
        {/if}
      </p>
    </FileInput>
  </InputFrame>

  <slot />
</InputContainer>
