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

<!-- $toasterStore.state && visible -->
{#if $toasterStore.state && visible}
  <div
    class="fixed w-max left-0 right-0 m-auto z-[500] top-10 max-w-full rounded-lg border border-gray-100 bg-white px-4 py-2 text-sm text-gray-600 shadow-md"
    transition:fade={{ duration: 200 }}
    class:service-toast-width={isServicePage}
    class:serviceDetails-toast-width={isServiceDetailsPage}
    class:md:left-80={isAuthenticated}
    class:auth-toaster-width={!isAuthenticated}
  >
    <div class="flex items-center justify-center">
      <div class="min-w-0 flex-grow">
        <div class="mr-3 flex-shrink-0 sm:hidden"></div>

        {$toasterStore.title}
      </div>

      <button
        class=" ml-3 flex-shrink-0 text-gray-400 hover:text-gray-600"
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
