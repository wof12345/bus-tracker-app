<script lang="ts">
  import { twMerge } from "tailwind-merge";
  import Error from "./Error.svelte";
  import { v4 as uuidv4 } from "uuid";

  const uuid = uuidv4();

  export let disabled: boolean = false;
  export let value: any;
  export let error: string = "";

  let group;

  function errorValidation(value: any) {
    if (value?.error) error = value.error;
    else error = "";
  }

  $: errorValidation(value);
</script>

<div
  bind:this={group}
  class={twMerge(
    `input-container grouped-input-${uuid} relative flex h-full w-full flex-1 flex-col items-start justify-center gap-1 text-gray-700`,
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
