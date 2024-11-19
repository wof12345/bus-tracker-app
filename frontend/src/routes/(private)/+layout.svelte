<script>
  import Banner from "$components/Banner/Banner.svelte";
  import Nav from "$lib/components/Nav/Nav.svelte";
  import { authStore, isTeacher } from "$lib/store/auth";
  import { onMount } from "svelte";
  import { validateApiResponse } from "$components/utils/validateApiResponse.js";
  import { deserialize } from "$app/forms";
  import { page } from "$app/stores";
  import { goto } from "$app/navigation";
  import { handleUserAndTutorStoreInfo } from "$components/utils/userInfoPopulation.js";

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
