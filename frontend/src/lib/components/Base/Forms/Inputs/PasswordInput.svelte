<script lang="ts">
  import { twMerge } from "tailwind-merge";

  export let value: any = "";
  export let name: string = "";
  export let placeholder: string = "password";
  export let variant: string = "default";
  export let disabled: boolean = false;
  export let fixStyle: boolean = false;
  export let required: boolean = true;
  export let type;
  export let advancedValidation: boolean = true;
  export let title;
  export let onInput = (e) => {};

  export let error: any = undefined;

  $: flow = variant === "default" ? "flex-row" : "flex-col";

  function handleInput(e: any) {
    value = e.target?.value;
    onInput(e);
  }

  function errorValidation(value) {
    if (value?.error) error = value.error;
    else error = "";
  }

  $: errorValidation(value);
</script>

<div
  class="gap-form-field flex flex-col items-start {fixStyle
    ? 'gap-6'
    : 'justify-between'}  lg:{flow}"
>
  <label
    for="password"
    class="text-sm text-gray-700 {fixStyle
      ? 'w-full max-w-[280px] font-semibold'
      : 'font-medium'} ">{title}</label
  >

  <div class={twMerge(` relative w-full max-w-lg`, $$props.class)}>
    <div class="flex h-full w-full flex-col">
      <input
        class={twMerge(
          "focus:shadow-input-focus shadow-input-blur flex w-full items-center justify-center rounded-lg border-[1px] border-gray-300 bg-white px-[14px] py-[10px] outline-none focus-within:border-[#EEAAFD] focus-within:ring-4 focus-within:ring-[#9E77ED3D]",
          $$props.inputClass,
        )}
        {placeholder}
        {type}
        on:input={handleInput}
        {name}
        autocomplete="off"
        value={value.error ? value.value : value}
        {disabled}
      />
    </div>
  </div>
</div>
