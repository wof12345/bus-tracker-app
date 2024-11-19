<script lang="ts">
  import { page } from "$app/stores";
  import { goto } from "$app/navigation";
  import { IconArrowLeft, IconArrowRight } from "@tabler/icons-svelte";
  import { handleRouteGroup } from "$components/utils/handleRouteGroup";
  import { addSeachParamToURL } from "$components/utils/routeValidation";

  export let pageSize = 10;
  export let totalItems: any;
  export let currentItems: any = 0;
  export let onPageChange = (pageNumber: number) => {};
  export let skip = 0;
  export let noReload = false;

  $: totalPages = Math.ceil(totalItems / pageSize);

  $: pathname = handleRouteGroup($page.route.id);

  $: currentPage =
    Number($page.url.searchParams.get("page")) ||
    Number($page.url.searchParams.get("skip") || 0) / pageSize + 1;

  function handleEmptyPage(currentItems) {
    if (currentItems <= 0 && currentPage > 1) {
      goToPage(currentPage - 1);
    }
  }

  $: handleEmptyPage(currentItems);

  let visiblePages: (number | "...")[] = [];

  function goToPreviousPage() {
    if (currentPage > 1) {
      goto(`${pathname}?skip=${(currentPage - 2) * pageSize}`);
      onPageChange(currentPage - 1);
    }
  }

  function goToNextPage() {
    if (currentPage < totalPages) {
      goto(`${pathname}?skip=${currentPage * pageSize}`);
      onPageChange(currentPage + 1);
    }
  }

  function goToPage(pageNumber) {
    let newUrl = addSeachParamToURL({
      key: "page",
      value: pageNumber,
    });

    if (!noReload) goto(newUrl);
    else skip = pageNumber;
  }

  function getVisiblePages() {
    if (totalPages <= 5) {
      visiblePages = Array.from({ length: totalPages }, (_, i) => i + 1);

      return visiblePages;
    }

    if (currentPage <= 3) {
      visiblePages = [1, 2, 3, 4, "...", totalPages];
    } else if (currentPage > 3 && currentPage < totalPages - 2) {
      visiblePages = [
        1,
        "...",
        currentPage - 1,
        currentPage,
        currentPage + 1,
        "...",
        totalPages,
      ];
    } else {
      visiblePages = [
        1,
        "...",
        totalPages - 3,
        totalPages - 2,
        totalPages - 1,
        totalPages,
      ];
    }

    return visiblePages;
  }

  $: (totalPages || currentPage) && getVisiblePages();
</script>

{#if totalItems > 0}
  <div class="pagination w-full">
    <button
      class="nav-button"
      on:click={goToPreviousPage}
      class:disabled={currentPage === 1}
    >
      <IconArrowLeft size={20} />
      <span class="hidden text-sm font-semibold text-gray-700 sm:block"
        >Previous</span
      >
    </button>

    <div class="flex items-center gap-x-1">
      {#each visiblePages as page}
        {#if page === "..."}
          <span class="dot-button">...</span>
        {:else}
          <button
            class="aspect-square w-8 border-none"
            on:click={() => goToPage(+page)}
            class:active={currentPage === page}
          >
            {page}
          </button>
        {/if}
      {/each}
    </div>

    <button
      class="nav-button"
      on:click={goToNextPage}
      class:disabled={currentPage === totalPages}
    >
      <span class="hidden text-sm font-semibold text-gray-700 sm:block"
        >Next</span
      >
      <IconArrowRight size={20} />
    </button>
  </div>
{:else}
  <div class="w-full p-4 text-center text-sm leading-6">No data available</div>
{/if}

<style>
  .pagination {
    @apply flex items-center justify-between gap-2 rounded-xl bg-white;
  }

  .pagination button {
    @apply flex cursor-pointer items-center justify-center gap-2 rounded-lg border border-gray-300 bg-white text-[14px] font-medium text-gray-600  shadow-xs hover:bg-gray-100 focus:outline-none disabled:cursor-not-allowed  disabled:opacity-50;
  }

  .pagination button.disabled {
    @apply cursor-not-allowed opacity-50;
  }

  .pagination button.active {
    @apply bg-gray-100 font-bold;
  }

  .dot-button {
    @apply cursor-not-allowed rounded px-2  py-1 text-gray-600;
  }

  .nav-button {
    @apply h-[36px] px-3.5 py-2;
  }
</style>
