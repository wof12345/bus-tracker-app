<script>
  import IconButton from "$components/Base/Buttons/IconButton.svelte";

  export let src = undefined;
  export let onClick = () => {};
</script>

<IconButton on:click={onClick} class="h-9 w-9 min-w-max rounded-full" {src}
  ><slot /></IconButton
>
