<div
  class=" h-full flex flex-col overflow-hidden rounded-xl border-gray-200 bg-white shadow-sm lg:border-[1px]"
>
  <div class="col-span-6 p-4">
    <div class="h-14 bg-gray-200 rounded mb-4" />
    <div class="space-y-4">
      {#each Array(10) as _}
        <div class="flex items-start gap-4 mb-4">
          <div class="w-10 h-10 rounded-full bg-gray-200" />
          <div class="flex-1">
            <div class="h-4 bg-gray-200 rounded w-3/4 mb-2" />
            <div class="h-4 bg-gray-200 rounded w-1/2" />
          </div>
        </div>
      {/each}
    </div>
  </div>
</div>

<style>
  @keyframes pulse {
    0%,
    100% {
      opacity: 1;
    }
    50% {
      opacity: 0.5;
    }
  }
</style>
