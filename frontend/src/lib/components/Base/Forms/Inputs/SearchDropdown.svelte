<script lang="ts">
  import DropDown from "./DropDown.svelte";
  export let value: any = "";
  export const options: any[] = [];
  export let icon: boolean = false;
  export let extractValue: boolean = false;
  export let relativeScrollElement;
  export let placeholder = "";
  export let areaDropDown;
  export let showIconX;
  export let disabled = false;

  let originalPlaceholder = placeholder;
  let lastValue;
  let menuOpen = false;

  let filteredOptions: string[] | object[] | undefined = undefined;

  function recordValue(value) {
    if (!value || value == lastValue) return;

    lastValue = value;
  }

  $: recordValue(value);

  function filter(e: InputEvent) {
    let keyword = e?.target?.value || value;

    if (!menuOpen) {
      placeholder = keyword;
      if (value != lastValue && lastValue && !value) value = lastValue;

      keyword = "";
    }

    if (!keyword || keyword == "") {
      filteredOptions = undefined;

      return;
    }

    filteredOptions = $$props.options.filter((elm: any) =>
      (elm.view_name || elm.name || elm)
        .toLowerCase()
        .includes(keyword.toLowerCase()),
    );
  }

  $: filter(menuOpen);
</script>

{#if $$slots.menu_items}
  <DropDown
    {...$$props}
    onInput={filter}
    options={filteredOptions || $$props.options}
    editable={true}
    {disabled}
    extractValue={true}
    bind:open={menuOpen}
    bind:placeholder
    {relativeScrollElement}
    bind:value
    on:change
  >
    <div slot="menu_items">
      <slot name="menu_items" />
    </div>
  </DropDown>
{:else}
  <!-- TODO: it may be needs for dropdown control -->
  <DropDown
    {...$$props}
    onInput={filter}
    options={filteredOptions || $$props.options}
    editable={true}
    {disabled}
    extractValue={true}
    bind:placeholder
    bind:open={menuOpen}
    bind:value
    bind:areaDropDown
    bind:showIconX
    {relativeScrollElement}
  ></DropDown>
{/if}
