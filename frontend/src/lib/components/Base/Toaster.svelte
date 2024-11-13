<script>
  import { fade } from "svelte/transition";
  import { toasterStore } from "$lib/store/toaster";
  import { authStore } from "$lib/store/auth";
  import { page } from "$app/stores";

  export let id;

  $: isAuthenticated = $authStore.isAuthenticated;
  $: isServicePage = $page.url.pathname === "/services";
  $: isServiceDetailsPage = $page.url.pathname === `/services/details/${id}`;

  let visible = true;
</script>

{#if $toasterStore.state && visible}
  <div
    class="fixed left-4 right-4 z-[500] mt-20 max-w-full rounded-lg border border-gray-100 bg-white px-4 py-2 text-sm text-gray-600 shadow-md md:bottom-auto md:mx-4 md:mt-8"
    transition:fade={{ duration: 200 }}
    class:service-toast-width={isServicePage}
    class:serviceDetails-toast-width={isServiceDetailsPage}
    class:md:left-80={isAuthenticated}
    class:auth-toaster-width={!isAuthenticated}
  >
    <div class="flex items-start">
      <div class="mr-3 hidden flex-shrink-0 sm:block">
        {#if $toasterStore.status === "success"}
          <svg
            width="38"
            height="38"
            viewBox="0 0 38 38"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <g opacity="0.3">
              <rect
                x="6"
                y="6"
                width="26"
                height="26"
                rx="13"
                stroke="#079455"
                stroke-width="2"
              />
            </g>
            <g opacity="0.1">
              <rect
                x="1"
                y="1"
                width="36"
                height="36"
                rx="18"
                stroke="#079455"
                stroke-width="2"
              />
            </g>
            <g clip-path="url(#clip0_8357_13645)">
              <path
                d="M15.2493 19.0003L17.7493 21.5003L22.7493 16.5003M27.3327 19.0003C27.3327 23.6027 23.6017 27.3337 18.9993 27.3337C14.397 27.3337 10.666 23.6027 10.666 19.0003C10.666 14.398 14.397 10.667 18.9993 10.667C23.6017 10.667 27.3327 14.398 27.3327 19.0003Z"
                stroke="#079455"
                stroke-width="1.66667"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </g>
            <defs>
              <clipPath id="clip0_8357_13645">
                <rect
                  width="20"
                  height="20"
                  fill="white"
                  transform="translate(9 9)"
                />
              </clipPath>
            </defs>
          </svg>
        {:else}
          <svg
            width="38"
            height="38"
            viewBox="0 0 38 38"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <g opacity="0.3">
              <rect
                x="6"
                y="6"
                width="26"
                height="26"
                rx="13"
                stroke="#D92D20"
                stroke-width="2"
              />
            </g>
            <g opacity="0.1">
              <rect
                x="1"
                y="1"
                width="36"
                height="36"
                rx="18"
                stroke="#D92D20"
                stroke-width="2"
              />
            </g>
            <g clip-path="url(#clip0_12_1959)">
              <path
                d="M18.9993 15.667V19.0003M18.9993 22.3337H19.0077M27.3327 19.0003C27.3327 23.6027 23.6017 27.3337 18.9993 27.3337C14.397 27.3337 10.666 23.6027 10.666 19.0003C10.666 14.398 14.397 10.667 18.9993 10.667C23.6017 10.667 27.3327 14.398 27.3327 19.0003Z"
                stroke="#D92D20"
                stroke-width="1.66667"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </g>
            <defs>
              <clipPath id="clip0_12_1959">
                <rect
                  width="20"
                  height="20"
                  fill="white"
                  transform="translate(9 9)"
                />
              </clipPath>
            </defs>
          </svg>
        {/if}
      </div>

      <div class="min-w-0 flex-grow space-y-2 sm:mt-2 sm:space-y-0">
        <div class="mr-3 flex-shrink-0 sm:hidden">
          {#if $toasterStore.status === "success"}
            <svg
              width="38"
              height="38"
              viewBox="0 0 38 38"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <g opacity="0.3">
                <rect
                  x="6"
                  y="6"
                  width="26"
                  height="26"
                  rx="13"
                  stroke="#079455"
                  stroke-width="2"
                />
              </g>
              <g opacity="0.1">
                <rect
                  x="1"
                  y="1"
                  width="36"
                  height="36"
                  rx="18"
                  stroke="#079455"
                  stroke-width="2"
                />
              </g>
              <g clip-path="url(#clip0_8357_13645)">
                <path
                  d="M15.2493 19.0003L17.7493 21.5003L22.7493 16.5003M27.3327 19.0003C27.3327 23.6027 23.6017 27.3337 18.9993 27.3337C14.397 27.3337 10.666 23.6027 10.666 19.0003C10.666 14.398 14.397 10.667 18.9993 10.667C23.6017 10.667 27.3327 14.398 27.3327 19.0003Z"
                  stroke="#079455"
                  stroke-width="1.66667"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </g>
              <defs>
                <clipPath id="clip0_8357_13645">
                  <rect
                    width="20"
                    height="20"
                    fill="white"
                    transform="translate(9 9)"
                  />
                </clipPath>
              </defs>
            </svg>
          {:else}
            <svg
              width="38"
              height="38"
              viewBox="0 0 38 38"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <g opacity="0.3">
                <rect
                  x="6"
                  y="6"
                  width="26"
                  height="26"
                  rx="13"
                  stroke="#D92D20"
                  stroke-width="2"
                />
              </g>
              <g opacity="0.1">
                <rect
                  x="1"
                  y="1"
                  width="36"
                  height="36"
                  rx="18"
                  stroke="#D92D20"
                  stroke-width="2"
                />
              </g>
              <g clip-path="url(#clip0_12_1959)">
                <path
                  d="M18.9993 15.667V19.0003M18.9993 22.3337H19.0077M27.3327 19.0003C27.3327 23.6027 23.6017 27.3337 18.9993 27.3337C14.397 27.3337 10.666 23.6027 10.666 19.0003C10.666 14.398 14.397 10.667 18.9993 10.667C23.6017 10.667 27.3327 14.398 27.3327 19.0003Z"
                  stroke="#D92D20"
                  stroke-width="1.66667"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </g>
              <defs>
                <clipPath id="clip0_12_1959">
                  <rect
                    width="20"
                    height="20"
                    fill="white"
                    transform="translate(9 9)"
                  />
                </clipPath>
              </defs>
            </svg>
          {/if}
        </div>
        <p class="break-words text-sm font-semibold text-gray-700">
          {$toasterStore.title}
        </p>
        {#if $toasterStore.message && $toasterStore.message !== ""}
          <p class="break-words text-sm text-[#475467]">
            {$toasterStore.message}
          </p>
        {/if}
      </div>

      <button
        class=" ml-3 mt-1.5 flex-shrink-0 text-gray-400 hover:text-gray-600"
        on:click={() => (visible = false)}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="lucide lucide-x"
        >
          <path d="M18 6 6 18" />
          <path d="m6 6 12 12" />
        </svg>
      </button>
    </div>
  </div>
{/if}

<style>
  .service-toast-width {
    @apply left-4 max-w-[1264px] md:left-0 md:mr-2 xl:mx-auto 2xl:left-2 2xl:max-w-[1280px];
  }
  .serviceDetails-toast-width {
    @apply left-4 max-w-[1264px] md:left-0 md:mr-2 xl:mx-auto 2xl:left-4;
  }
  .auth-toaster-width {
    @apply mx-auto mt-8 max-w-[360px];
  }
</style>
