<script lang="ts">
  import { twMerge } from "tailwind-merge";

  import { v4 as uuidv4 } from "uuid";
  import InputContainer from "../Components/InputContainer.svelte";
  import InputFrame from "../Components/InputFrame.svelte";

  const id = uuidv4();

  export let value: any = "";
  export let label: string = "Label";

  export let placeholder: any = undefined;
  export let disabled: boolean = false;
  export let error: any = undefined;
  export let name: any = `date-${id}`;
  export let required: boolean = true;
  export let formData: any = {};

  export let formattedDate;

  function handleDateFormat(passedDate) {
    if (!passedDate) return;
  }

  function formatValue(value) {
    if (typeof value === "object") return value.value;

    return value;
  }

  function formatDate(dateValue) {
    if (!dateValue) return;

    const inputDate = new Date(dateValue?.value);

    if (isNaN(inputDate.getTime())) {
      return dateValue.replaceAll("/", "-");
    }

    return dateValue;
  }
</script>

<InputContainer {disabled} bind:error {value}>
  <InputFrame class={$$props.class}>
    <slot />

    <input
      class={twMerge(
        `w-full bg-transparent text-gray-500 outline-none  ${disabled ? "cursor-not-allowed" : ""}`,
        $$props.inputClass,
      )}
      {name}
      on:input={(e) => {
        formattedDate = e.target.value;

        handleDateFormat(formattedDate);
      }}
      {disabled}
      autocomplete="off"
      value={formatDate(formatValue(value))}
      type="date"
      placeholder={placeholder || label}
      {required}
    />
  </InputFrame>

  <slot name="below-head" />
</InputContainer>
