<script lang="ts">
  import { twMerge } from "tailwind-merge";
  import InputFrame from "../Components/InputFrame.svelte";
  import InputContainer from "../Components/InputContainer.svelte";
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
  export let editable: boolean = true;
  export let maxLength: boolean = true;
  export let minLength: boolean = true;
  export let onInput = (e) => {};

  let max = maxLength ? "100" : "";
  let min = minLength ? "25" : "";

  function handleInput(e: any) {
    value = formData[name] = e.target?.value;

    onInput(e);
  }

  function formatValue(value) {
    if (typeof value === "object") return value.value;

    return value;
  }
</script>

<InputContainer {disabled} bind:error {value}>
  <InputFrame class={$$props.class} {error} {name} {disabled}>
    <slot />

    <input
      class={twMerge(
        `w-full bg-transparent outline-none ${disabled ? "cursor-not-allowed" : ""}`,
        $$props.inputClass,
      )}
      {name}
      on:input={handleInput}
      {disabled}
      autocomplete="off"
      {max}
      {min}
      value={formatValue(value)}
      readonly={!editable}
      placeholder={placeholder || label}
      {required}
    />
  </InputFrame>

  <slot name="below-head" />
</InputContainer>
