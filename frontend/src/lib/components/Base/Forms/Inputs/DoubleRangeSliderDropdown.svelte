<script lang="ts">
  import DropDown from "./DropDown.svelte";
  export let value: any = undefined;
</script>

<DropDown {...$$props} extractValue={true} bind:value />
