<script>
  import { goto } from "$app/navigation";
  import Button from "$components/Base/Buttons/Button.svelte";
</script>

<Button onClick={() => goto("/commuter/login")}>Login as a commuter</Button>
