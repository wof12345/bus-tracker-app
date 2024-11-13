<script lang="ts">
  import Button from "$components/Base/Buttons/Button.svelte";
  import { onMount } from "svelte";
  import CloseButton from "$components/Assets/CloseButton.svelte";
  import { authStore, logout } from "$lib/store/auth";

  import Menu from "$components/Base/Menu/Menu.svelte";
  import Paragraph from "$components/Base/Typography/Paragraph.svelte";
  import Text from "$components/Base/Typography/Text.svelte";
  import { twMerge } from "tailwind-merge";
  import Divider from "$components/Base/Divider.svelte";
  import IconButton from "$components/Base/Buttons/IconButton.svelte";
  import Avatar from "$components/Base/Avatar.svelte";
  import { clickOutside } from "../utils/clickOutside";
  import Logo from "$components/Nav/Logo.svelte";

  let isMobile = false;
  export let showSidebar = false;
  export let landingPage = false;

  function windowSize() {
    if (window.innerWidth <= 1024) {
      isMobile = true;
    } else {
      isMobile = false;
      showSidebar = false;
    }
  }

  function handleClick(event) {
    event.stopPropagation();
    showSidebar = true;

    let threeBar = document.querySelector("#threebar");
    if (threeBar) {
      threeBar.style.display = "none";
    }
  }

  function close() {
    showSidebar = false;
    let threeBar = document.querySelector("#threebar");
    if (threeBar && isMobile) {
      threeBar.style.display = "block";
    }
  }

  let image = false;

  onMount(() => {
    windowSize();
    window.addEventListener("resize", windowSize);
  });

  let profileMenu: Menu;
  let profileMenuVisible = false;

  function toggleMenuVisibility() {
    profileMenuVisible = !profileMenuVisible;
  }

  function handleProfileMenu() {
    toggleMenuVisibility();
    if (profileMenuVisible) {
      profileMenu.show();
    } else {
      profileMenu.hide();
    }
  }
</script>

<div class="py-0 lg:relative">
  <div class="flex items-center justify-between">
    <div class="flex items-center gap-10">
      <Logo alt={false} />

      <a href="/services">
        <Button
          variant="borderless"
          class="hidden p-0 text-base font-semibold text-gray-600  hover:text-gray-700 lg:block"
          >Look for tutors
        </Button>
      </a>

      <a href="/tutor/register">
        <Button
          variant="borderless"
          class="hidden justify-start p-0 text-base font-semibold text-gray-600 hover:text-gray-700 lg:block"
          >Join as a tutor
        </Button>
      </a>
    </div>
    <div class="hidden md:block">
      <div class="flex items-center gap-3">
        {#if $authStore.isAuthenticated === false}
          <a class="font-semibold" href="/student/login">
            <Button
              variant="hover"
              class="border-none px-4 {landingPage
                ? 'text-gray-600 xl:text-white'
                : 'text-gray-600'}  hover:text-gray-700"
            >
              Log in
            </Button>
          </a>
          <a href="/student/register">
            <Button class="border-none px-4" varriant="primary">Sign up</Button>
          </a>
        {:else if $authStore.isAuthenticated === true}
          <div
            class={twMerge(
              "relative  items-center gap-4 text-sm md:flex ",
              $$props.class,
            )}
          >
            <Menu
              class=" absolute right-0 top-12 mt-1.5 border"
              bind:this={profileMenu}
              bind:visible={profileMenuVisible}
            >
              <div class="border-1 flex gap-3 p-4">
                <Avatar
                  class="h-11 w-11"
                  src={$authStore?.userInfo?.photo?.path}
                />

                <div>
                  <Paragraph class="text-sm font-semibold text-[#344054]"
                    >{$authStore?.user?.first_name ||
                      "" + $authStore?.user?.last_name ||
                      ""}</Paragraph
                  >
                  <Paragraph>{$authStore?.user?.email || ""}</Paragraph>
                </div>
              </div>

              <Divider />
              <a href="/home">
                <button
                  class="flex w-full cursor-pointer items-center gap-2 p-4 hover:bg-slate-100"
                >
                  <img src="/dashBoard.svg" alt="" />
                  <Paragraph class="  pt-1 font-medium text-gray-700"
                    >Dashboard</Paragraph
                  >
                </button>
              </a>
              <div class="flex flex-col gap-1">
                <Divider />
              </div>

              <button
                class="flex w-full cursor-pointer items-center gap-2 p-4 hover:bg-slate-100"
                on:click={() => {
                  logout();
                  profileMenu.hide();
                }}
              >
                <img src="/logOut (2).svg" alt="Logout Icon" />
                <Paragraph class="  font-medium text-gray-700"
                  >Log out</Paragraph
                >
              </button>
            </Menu>

            <IconButton
              on:click={handleProfileMenu}
              class="{profileMenuVisible
                ? 'bg-opacity-25'
                : 'hover:bg-none'}  profile-menu aspect-square  rounded-full border-[5px] border-[#f4ebff] object-cover object-center  p-0 hover:bg-white"
            >
              <Avatar
                class="h-10 w-10 "
                src={$authStore?.userInfo?.photo?.path}
              /></IconButton
            >
          </div>

          <div
            class={twMerge(
              "flex w-full flex-col items-start gap-4 p-2 text-sm md:hidden",
              $$props.class,
            )}
          >
            <a class="flex w-full gap-2" href="#">
              <img src={"/settings.svg"} alt="" />
              <Text class="text-white">Settings</Text>
            </a>
          </div>
        {/if}
      </div>
    </div>
  </div>

  {#if isMobile && !showSidebar}
    <button id="threebar" class="hamburger-img-box" on:click={handleClick}>
      <img class="hamburger-img" src="/sidebar.svg" alt="" />
    </button>
  {/if}

  <div
    use:clickOutside={() => (showSidebar = false)}
    class:sidebar={true}
    class:sidebar-visible={showSidebar}
    class:sidebar-hidden={!showSidebar}
  >
    <div class="sidebar-container">
      <div class="nav-container">
        <Logo alt={false} />
        <CloseButton onClick={() => close()} />
      </div>

      <div class="others-container">
        <div class="title-box">
          <a class="title-text" href="/services">Look for tutors</a>
          <a class="title-text" href="/tutor/register">Join as a tutor</a>

          {#if $authStore.isAuthenticated}
            <a class="title-text" href="/home">Go to dashboard</a>
          {/if}
        </div>

        <div class="box">
          <div class="text-box">
            <a class="text" href="/">Who we are</a>
            <a class="text" href="/">Privacy policy</a>
          </div>

          <div class="text-box">
            <a class="text" href="/">Legal centre</a>
            <a class="text" href="/">Cookie policy</a>
          </div>
        </div>

        {#if $authStore.isAuthenticated === false}
          <div class="btn-box">
            <a href="/student/register"><Button>Sign up</Button></a>
            <a class="font-semibold" href="/student/login">
              <Button class="min-w-full" variant="secondary">Log in</Button>
            </a>
          </div>
        {/if}
        {#if $authStore.isAuthenticated === true}
          <div class="pro-container">
            <div class="pro-box">
              <div class="pro-img-box">
                <img
                  class="pro-img"
                  src={$authStore?.userInfo?.photo?.path}
                  alt=""
                />
              </div>

              <div>
                <Paragraph class="text-base font-semibold text-gray-900"
                  >{$authStore?.user?.first_name ||
                    "" + $authStore?.user?.last_name ||
                    ""}</Paragraph
                >
                <Paragraph class="text-base text-gray-600"
                  >{$authStore?.user?.email || ""}</Paragraph
                >
              </div>
            </div>

            <Button
              onClick={logout}
              variant="secondary"
              class="text-base font-semibold">Log out</Button
            >
          </div>
        {/if}
      </div>
    </div>
  </div>
</div>

<style>
  .hamburger-img-box {
    @apply block md:hidden;
  }
  .hamburger-img {
    @apply absolute right-4 -mt-9;
  }
  .sidebar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: auto;
    background-color: transparent;
    z-index: 1000;
    transition: transform 0.3s ease-in-out;
  }

  .sidebar-hidden {
    transform: translateX(-100%);
  }

  .sidebar-visible {
    transform: translateX(0);
  }

  .sidebar-container {
    @apply block bg-white pt-2 shadow-lg md:hidden;
  }

  .nav-container {
    @apply flex items-center justify-between bg-[#FFFFFF] pl-4 pr-1 pt-2.5;
  }

  .others-container {
    @apply mt-16 flex flex-col gap-2 bg-[#FFFFFF];
  }

  .title-box {
    @apply mb-6 flex flex-col gap-8 px-4;
  }

  .title-text {
    @apply text-[16px] font-semibold text-gray-900;
  }

  .box {
    @apply flex justify-between gap-5 border-t px-4 py-5;
  }

  .text-box {
    @apply flex w-full flex-col gap-3;
  }

  .text {
    @apply text-[16px] font-semibold text-gray-600;
  }
  .btn-box {
    @apply xs:grid-cols-2 grid gap-3 px-4 pb-6;
  }

  .pro-container {
    @apply flex flex-col gap-6 px-4 pb-6;
  }
  .pro-box {
    @apply flex items-center gap-3;
  }
  .pro-img-box {
    @apply h-12 w-12 rounded-full bg-gray-100;
  }
</style>
