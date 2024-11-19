<script lang="ts">
  import { twMerge } from "tailwind-merge";
  import { invalidateAll } from "$app/navigation";
  import { showToaster } from "$lib/store/toaster";
  import Alert from "$components/Base/Alerts/Alert.svelte";
  import { enhance } from "$app/forms";
  import { showSpinner } from "$lib/store/spinner";

  export let values: any = {};
  export let formActionSuccess = () => {};
  export let method = "POST";

  export let error: any = undefined;

  let form: HTMLFormElement;

  export let handleSubmit = async () => {
    values = {};

    const inputs = form?.querySelectorAll("input");
    const textareas = form?.querySelectorAll("textarea");

    const formElements = [...inputs, ...textareas];

    for (let elm of formElements) {
      const tagName = elm.tagName.toLowerCase();

      if (tagName === "input" || tagName === "textarea") {
        if (elm.type === "file") {
          values[elm.name] = elm?.files[0];
        } else {
          values[elm.name] = elm?.value;
        }
      }
    }

    return;

    if (res?.status !== 200 && res?.status !== 201) {
      if (typeof res?.detail === "string") {
        error = res?.detail || res?.message || "";
      } else {
        error = "Something went wrong";
      }

      showToaster(error);
    }
  };
</script>

{#if method}
  <form
    {...$$props}
    on:submit|preventDefault={handleSubmit}
    class={twMerge("col-auto grid w-full gap-3", $$props.class)}
    bind:this={form}
    {method}
    use:enhance={() => {
      return async ({ update }) => {
        await showSpinner(update());

        await invalidateAll();

        if (!error) formActionSuccess();
        else showToaster("Error", "Something went wrong!", "error");
      };
    }}
  >
    {#if error}
      {#if $$slots.error}
        <slot name="error" />
      {/if}
    {/if}

    <slot />
  </form>
{:else}
  <form
    {...$$props}
    on:submit|preventDefault={handleSubmit}
    class={twMerge("col-auto grid w-full gap-3", $$props.class)}
    bind:this={form}
    {method}
  >
    {#if error}
      {#if $$slots.error}
        <slot name="error" />
      {/if}
    {/if}

    <slot />
  </form>
{/if}
