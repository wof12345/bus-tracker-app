<script lang="ts">
  import { twMerge } from "tailwind-merge";
  import Error from "./Error.svelte";

  export let disabled: boolean = false;
  export let value: any;
  export let error: string = "";

  function errorValidation(value: any) {
    if (value?.error) error = value.error;
    else error = "";
  }

  $: errorValidation(value);
</script>

<div
  class={twMerge(
    `input-container relative flex h-full w-full flex-1 flex-col items-start justify-center gap-1 text-gray-700 `,
    $$props.class,
  )}
>
  <slot />

  {#if !disabled && error && error != ""}
    <Error>
      {error || ""}
    </Error>
  {/if}
</div>
