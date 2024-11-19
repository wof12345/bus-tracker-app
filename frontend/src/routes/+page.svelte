<script>
  import { goto } from "$app/navigation";
  import Button from "$components/Base/Buttons/Button.svelte";
</script>

<Button onClick={goto("/student/login")}>Login as a student</Button>
