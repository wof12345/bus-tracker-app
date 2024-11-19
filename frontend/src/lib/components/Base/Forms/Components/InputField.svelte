<script lang="ts">
  import { twMerge } from "tailwind-merge";
  import InputContainer from "./InputContainer.svelte";
  import InputFrame from "./InputFrame.svelte";
  import { v4 as uuidv4 } from "uuid";

  const id = uuidv4();

  export let value: any = "";
  export let label: string = "Label";
  export let type: string = "text";
  export let placeholder: any = undefined;
  export let disabled: boolean = false;
  export let error: any = undefined;
  export let name: any = `${type}-${id}`;
  export let required: boolean = true;
  export let formData: any = {};

  function handleInput(e: any) {
    value = e.target?.value;
  }

  $: value = formData[name] || "";
</script>

<InputContainer {disabled} bind:error {value}>
  <InputFrame {error} {name}>
    <slot />

    <input
      class={twMerge(
        `w-full outline-none ${disabled ? "cursor-not-allowed" : ""}`,
        $$props.class,
      )}
      {name}
      {type}
      on:input={handleInput}
      {disabled}
      autocomplete="off"
      value={value.error ? value.value : value}
      placeholder={placeholder || label}
      {required}
    />
  </InputFrame>
</InputContainer>
