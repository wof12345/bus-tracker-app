<script>
  import Nav from "$lib/components/Nav/Nav.svelte";
  import { authStore, isCommuter } from "$lib/store/auth.js";
  import { onMount } from "svelte";

  import { page } from "$app/stores";

  export let data;

  $: pathName = $page?.route?.id;

  const notifications = data?.userNotifications?.data;
  let show = false;

  const changeBannerState = (flag = false) => {
    show = flag;
  };

  onMount(async () => {});
</script>

<div class="relative flex h-full min-h-screen flex-col md:flex-row">
  <Nav notificationData={notifications} />

  <div class="scroll-body relative h-screen w-full overflow-auto bg-white">
    <slot />
  </div>
</div>
