<script lang="ts">
  import { twMerge } from "tailwind-merge";
  import InputContainer from "../Components/InputContainer.svelte";
  import InputFrame from "../Components/InputFrame.svelte";
  import { createEventDispatcher } from "svelte";

  import { v4 as uuidv4 } from "uuid";

  const id = uuidv4();
  const dispatch = createEventDispatcher();

  export let value: any = "";
  export let label: string = "Label";
  export let type: string = "text";
  export let placeholder: any = undefined;
  export let disabled: boolean = false;
  export let error: any = undefined;
  export let name: any = `${type}-${id}`;
  export let required: boolean = true;
  export let formData: any = {};
  export let editable = true;

  export let rows = 4;
  export let cols = 20;

  export let onInput = (e: Event) => {};

  let textarea: HTMLTextAreaElement;

  function handleInput(e: Event) {
    const target = e.target as HTMLTextAreaElement;
    value = target.value;
    formData[name] = value;
    onInput(e);
    dispatch("input", { value });
  }

  function clearTextarea() {
    if (textarea) {
      textarea.value = "";
      value = "";
      formData[name] = "";
      dispatch("input", { value: "" });
    }
  }

  function formatValue(value) {
    if (typeof value === "object") return value.value;

    return value;
  }

  $: if (value === "") {
    clearTextarea();
  }
</script>

<InputContainer {disabled} bind:error {value}>
  <InputFrame {error} {name}>
    <textarea
      bind:this={textarea}
      class={twMerge(
        `w-full resize-none outline-none ${disabled ? "cursor-not-allowed" : ""}`,
        $$props.class,
      )}
      {disabled}
      {required}
      {name}
      on:input={handleInput}
      {cols}
      {rows}
      maxlength="300"
      readonly={!editable}
      placeholder={placeholder || label}
      value={formatValue(value)}
    />
    <slot />
  </InputFrame>

  <slot name="below-head" />
</InputContainer>
