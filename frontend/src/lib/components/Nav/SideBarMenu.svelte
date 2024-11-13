<script lang="ts">
  import { page } from "$app/stores";
  import IconButton from "../Base/Buttons/IconButton.svelte";
  import Logo from "./Logo.svelte";
  import {
    isAdmin,
    isTeacher,
    isStudent,
    authStore,
    logout,
  } from "$lib/store/auth";
  import navAdmin from "$lib/data/admin_nav.json";
  import navTeacher from "$lib/data/teachers_nav.json";
  import navStudent from "$lib/data/students_nav.json";
  import Text from "../Base/Typography/Text.svelte";

  import Avatar from "../Base/Avatar.svelte";
  import Paragraph from "../Base/Typography/Paragraph.svelte";
  import { onMount } from "svelte";
  import { fly } from "svelte/transition";
  import BackgroundCover from "$components/Base/BackgroundCover.svelte";
  import { IconLogout, IconX } from "@tabler/icons-svelte";
  import Modal from "$lib/components/Base/Modal/Modal.svelte";
  import ModalHeader from "$lib/components/Base/Modal/ModalHeader.svelte";
  import ModalBody from "$lib/components/Base/Modal/ModalBody.svelte";

  import Title from "$components/Base/Typography/Title.svelte";

  import { getPathNameFromString } from "$lib/components/utils/routeValidation";
  import { twMerge } from "tailwind-merge";

  export let visible: any = undefined;
  export let navItems;
  export let notificationData;

  let mobile = false;
  let badge = notificationData?.filter((e) => e.read_at == null).length;

  $: pathName = $page.route.id;

  $: navItems = isAdmin($authStore)
    ? navAdmin
    : isTeacher($authStore)
      ? navTeacher
      : navStudent;

  export function show() {
    document.body.classList.add("overflow-hidden");
    visible = true;
  }

  export function hide() {
    document.body.classList.remove("overflow-hidden");
    visible = false;
  }
  const marksAsRead = async () => {
    if (badge < 0) {
      return;
    }
    const res = await fetch("/api/notification?/markAsRead", {
      method: "POST",
      body: {},
    });
    const data = await res.json();
  };

  function handleNotification() {
    marksAsRead();
    badge = 0;
    const screenWidth = window.innerWidth;
    if (screenWidth <= 768) {
      visible = false;
      notificationModal.show();
      mobile = true;
    } else {
      visible = true;
      mobile = false;
      notificationModal.show();
    }
  }

  function handleSettings() {
    const screenWidth = window.innerWidth;
    if (screenWidth <= 768) {
      visible = false;

      mobile = true;
    } else {
      visible = true;
      mobile = false;
    }
  }

  function getHref(item) {
    return item.href;
  }

  function determineScreen() {
    const screenWidth = window.innerWidth;

    if (screenWidth <= 767) {
      visible = false;
      mobile = true;
    } else {
      visible = true;
      mobile = false;
    }
  }

  function getFirstLetter(name) {
    const regex = /^[A-Za-z]/;
    const match = name.match(regex);
    return match ? match[0] : "";
  }

  let notificationModal;

  onMount(() => {
    determineScreen();

    window.addEventListener("resize", (e) => {
      determineScreen();
    });
  });

  function handleBadge() {
    badge = 0;
  }
</script>

{#if visible === true || visible === undefined}
  <BackgroundCover class="md:hidden" {hide} {visible}></BackgroundCover>
  <IconButton
    class="fixed right-3 top-5 z-[60] w-9 p-2 text-black md:hidden"
    on:click={() => hide()}
  >
    <IconX />
  </IconButton>

  <div
    transition:fly={{ x: -200 }}
    class="fixed left-0 top-0 z-50 {visible === true
      ? 'flex'
      : 'hidden'} max-h-screen min-h-screen md:sticky md:flex"
  >
    <div class="z-10 flex h-screen w-max min-w-[280px] bg-[#821890] p-4">
      <div
        class="relative z-10 flex max-h-screen w-full max-w-[311px] flex-col justify-between overflow-hidden font-semibold"
      >
        <div
          class="flex max-h-full w-full flex-col gap-2 self-start overflow-auto"
        >
          <div class="mb-6 mt-8">
            <Logo alt={true} />
          </div>

          {#each navItems as item}
            <button
              on:click={handleBadge}
              class="flex items-center justify-center"
            >
              <a
                class="flex w-full gap-3 rounded-md px-3 py-2 transition duration-150 ease-linear hover:bg-[#9F1AB1]"
                class:bg-[#9F1AB1]={pathName?.includes(
                  getPathNameFromString(item.href),
                )}
                on:click={() => {
                  if (mobile) visible = false;
                }}
                href={getHref(item)}
              >
                {#if item?.name === "Services" && isStudent($authStore)}
                  <div class="flex w-full items-center justify-between">
                    <div class="flex gap-3">
                      <img src={`/${item.icon}`} alt="" />
                      <Text class="text-md text-gray-100">
                        {item?.name}
                      </Text>
                    </div>

                    <div>
                      <img class=" h-4 w-4" src="/services_side.svg" />
                    </div>
                  </div>
                {:else}
                  <img src={`/${item.icon}`} alt="" />
                  <Text class="text-md text-gray-100">
                    {item?.name}
                  </Text>
                {/if}

                {#if item?.name == "Order" || item?.name == "Message"}
                  <div class="absolute right-4">
                    {#if badge > 0}
                      <div
                        class="-mt-1 grid h-7 w-7 items-center justify-center rounded-full border-[1px] bg-[#F9FAFB] px-2 py-[2px] text-sm font-medium text-[#344054]"
                      >
                        {badge}
                      </div>
                    {/if}
                  </div>
                {/if}
              </a>
            </button>
          {/each}
        </div>

        <div class="flex w-full flex-col gap-4 justify-self-end">
          <button
            on:click={handleNotification}
            class:bg-[#9F1AB1]={pathName?.includes("/notification")}
            class={twMerge(
              "flex w-full items-end gap-4 rounded-md px-3 py-2 text-sm hover:bg-[#9F1AB1] ",
              $$props.class,
            )}
          >
            <div class="flex w-full items-center gap-3">
              <img class="w-6" src={"/notification.svg"} alt="" />
              <Text class="text-white">Notifications</Text>
            </div>
            <div class="pt-[2]">
              {#if badge > 0}
                <div
                  class="-mt-1 grid h-6 w-6 items-center justify-center rounded-full border-[1px] bg-[#F9FAFB] px-2 py-[2px] text-sm font-medium text-[#344054]"
                >
                  {badge}
                </div>
              {/if}
            </div>
          </button>

          <button
            on:click={handleSettings}
            class:bg-[#9F1AB1]={pathName?.includes("/settings")}
            class={twMerge(
              "flex w-full flex-col items-start gap-4 rounded-md px-3 py-2 text-sm hover:bg-[#9F1AB1]",
              $$props.class,
            )}
          >
            <a class="flex w-full items-center gap-3" href="/settings">
              <img class="w-6" src={"/setting.svg"} alt="" />
              <Text class="text-white">Settings</Text>
            </a>
          </button>

          <div
            class="flex w-full items-center justify-between gap-2 border-t border-white px-3 py-2 pt-6"
          >
            <Avatar
              class="h-10 w-10 p-0"
              src={$authStore?.userInfo?.photo?.path || undefined}
            />

            <div class=" w-[160px]">
              <Paragraph
                class="truncate text-sm font-semibold text-white md:text-sm"
                >{($authStore?.user?.first_name || "") +
                  " " +
                  ($authStore?.user?.last_name || "")}</Paragraph
              >

              <Paragraph
                class="truncate text-sm font-normal text-gray-100 md:text-sm"
                >{$authStore?.user?.email || ""}</Paragraph
              >
            </div>

            <IconButton
              on:click={logout}
              class="-mt-2 ml-auto h-9 w-9 self-start p-0 text-white"
            >
              <IconLogout size={18} />
            </IconButton>
          </div>
        </div>
      </div>
    </div>
  </div>
{/if}

{#if visible == false}
  <div class="bg-brand-700 mt-0 flex items-center justify-between px-4 py-3">
    <Logo alt="false" />
    <IconButton on:click={() => show()}>
      <img class="flex justify-end" src="/ThreeBar.svg" alt="" /></IconButton
    >
  </div>
{/if}

<Modal
  notificationModal="true"
  bind:this={notificationModal}
  class="no-scrollbar  absolute left-0 mx-4 h-auto max-h-[480px] w-[480px] max-w-[320px] overflow-hidden shadow-xl md:left-80"
>
  <ModalHeader
    class=" mt-4 justify-start border-b-0 py-0 text-center text-lg font-semibold text-gray-900"
  >
    <Title class="py-4 md:text-xl">Notifications</Title>
  </ModalHeader>

  <ModalBody class="grid h-auto  gap-4 border-b-0 p-0">
    <div class="flex h-full items-center">
      <div>
        {#if !notificationData || notificationData.length <= 0}
          <p class="px-5 py-4 text-center">No notifications yet</p>
        {:else}
          {#each notificationData || [] as item, idx}
            {#if item?.read_at == null}
              <div
                class="flex w-full items-start justify-between border-b border-slate-200 bg-[#F2F4F7] px-4 py-2"
              >
                <div class="flex items-start gap-3">
                  <div class=" inline-block">
                    <div
                      class="flex h-12 w-12 items-center justify-center overflow-hidden rounded-full border-2 border-white bg-indigo-300"
                    >
                      {#if item?.related_user?.info == null}
                        <span class="text-center text-2xl"
                          >{getFirstLetter(
                            item?.related_user?.first_name,
                          )}</span
                        >
                      {:else}
                        <img
                          src="/pic.jpg?height=48&width=48"
                          alt="User avatar"
                          class="h-full w-full object-cover"
                        />
                      {/if}
                    </div>
                  </div>

                  <div>
                    <h4 class="text-sm font-medium text-[#344054]">
                      {item.name ||
                        item?.related_user?.first_name +
                          " " +
                          item?.related_user?.last_name}
                    </h4>
                    <p class="text-sm font-normal text-[#475467]">
                      {item.details || item?.message}
                      <span class="block font-medium text-[#6941C6]"
                        >{item.additional_data?.order_id
                          ? "#Order " + item.additional_data?.order_id
                          : ""}</span
                      >
                    </p>
                  </div>
                </div>
              </div>
            {:else}
              <div
                class="flex w-full items-start justify-between border-b border-slate-100 px-4 py-2"
              >
                <div class="flex items-start gap-3">
                  <div class=" inline-block">
                    <div
                      class="flex h-12 w-12 items-center justify-center overflow-hidden rounded-full border-2 border-white bg-indigo-300"
                    >
                      {#if item?.related_user?.info == null}
                        <span class="text-center text-2xl"
                          >{getFirstLetter(
                            item?.related_user?.first_name,
                          )}</span
                        >
                      {:else}
                        <img
                          src="/pic.jpg?height=48&width=48"
                          alt="User avatar"
                          class="h-full w-full object-cover"
                        />
                      {/if}
                    </div>
                  </div>

                  <div>
                    <h4 class="text-sm font-medium text-[#344054]">
                      {item.name ||
                        item?.related_user?.first_name +
                          " " +
                          item?.related_user?.last_name}
                    </h4>
                    <p class="text-sm font-normal text-[#475467]">
                      {item?.message}
                      <span class="block font-medium text-[#6941C6]"
                        >{item?.additional_data?.order_id
                          ? "#Order " + item?.additional_data?.order_id
                          : ""}</span
                      >
                    </p>
                  </div>
                </div>
              </div>
            {/if}
          {/each}
        {/if}
      </div>
    </div>
  </ModalBody>
</Modal>

<style>
  .hide-scrollbar {
    scrollbar-width: none;
    -ms-overflow-style: none;
  }

  .hide-scrollbar::-webkit-scrollbar {
    display: none;
  }
</style>
