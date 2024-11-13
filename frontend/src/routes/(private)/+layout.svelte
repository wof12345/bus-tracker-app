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

  $: changeBannerState(true, data);

  function handleBannerText() {
    if (!$authStore?.userInfo?.photo) {
      return {
        text: "Update your profile photo",
        redirect: "/settings",
      };
    }

    if (!$authStore?.user?.role != "tutor") {
      return;
    }

    if (!$authStore?.tutor?.application?.approved_at) {
      return {
        text: "Your application for tutor approval is pending",
        redirect: "",
      };
    }

    if (!$authStore?.tutor?.bank) {
      return {
        text: "Update your payout info",
        redirect: "/settings",
      };
    }

    return null;
  }

  onMount(async () => {
    await handleUserAndTutorStoreInfo(
      data,
      authStore,
      deserialize,
      pathName,
      validateApiResponse,
      goto,
    );
  });
</script>

<div class="relative flex h-full min-h-screen flex-col md:flex-row">
  <Nav notificationData={notifications} />

  <div class="scroll-body relative h-screen w-full overflow-auto bg-white">
    {#if handleBannerText() && show && isTeacher($authStore)}
      <div
        class="sticky top-0 z-50 flex h-[0px] w-full items-center justify-center overflow-visible"
      >
        <Banner bannerData={handleBannerText()} closeFn={changeBannerState} />
      </div>
    {/if}

    <slot />
  </div>
</div>
