<script>
  import { page } from "$app/stores";
  import Text from "$components/Base/Typography/Text.svelte";
  import { IconChevronRight, IconHome } from "@tabler/icons-svelte";
  import { breadcrumbStore } from "./store";

  $: pathname = $page.url.pathname;

  function getPathTree(pathname) {
    let crumb = [];
    const path = pathname?.split("/");

    crumb = path?.filter((elm) => elm !== "") || [];

    return crumb;
  }

  function getPath(path, idx) {
    let trailingPath = "";

    const fullPath = pathname?.split("/");

    if (fullPath[idx] === "services") {
      trailingPath = "/control/services";
    } else {
      for (let i = 0; i < fullPath.length; i++) {
        trailingPath += fullPath[i] + "/";

        if (fullPath[i] === path) break;
      }
    }

    return trailingPath;
  }

  function determinePathAlias(path, prefix) {
    let pathWithoutControl = path.replace("control", "");
    let pathAlias;

    prefix = prefix ?? "";
    pathAlias = $breadcrumbStore.pathLookUp[prefix + pathWithoutControl];

    return pathAlias || pathWithoutControl;
  }

  $: pathTree = getPathTree(pathname, $breadcrumbStore);
</script>

{#if pathname !== "/"}
  <div class="flex w-full items-center gap-3 overflow-hidden text-gray-500">
    <a href="/home" class="min-w-[20px]"><IconHome size={20} /></a>

    {#each pathTree as path, idx}
      {#if path !== "control"}
        <IconChevronRight size={17} class={"text-gray-300"} />

        <a
          href={getPath(path, idx)}
          class={idx === pathTree.length - 1 ? "pointer-events-none" : ""}
        >
          <Text
            class="text-sm font-medium text-gray-600 first-letter:uppercase {getPathTree(
              pathname,
            ).length -
              1 ===
            idx
              ? 'rounded-md bg-gray-50 px-2 py-1 font-semibold text-gray-700'
              : ''}"
          >
            {determinePathAlias(path, pathTree[idx - 1])}
          </Text>
        </a>
      {/if}
    {/each}
  </div>
{/if}
