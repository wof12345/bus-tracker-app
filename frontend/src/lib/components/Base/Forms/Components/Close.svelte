<script lang="ts">
  import IconButton from "$components/Base/Buttons/IconButton.svelte";
  import { IconX } from "@tabler/icons-svelte";

  export let onClick: any;
</script>

<IconButton
  className="aspect-square w-5 p-1 hover:cursor-pointer  bg-opacity-30 bg-gray-200 absolute top-2 right-2"
  on:click={onClick}
>
  <IconX />
</IconButton>
