<script>
  import Toaster from "$components/Base/Toaster.svelte";
  import Spinner from "$components/Base/Spinner.svelte";
  import "../app.pcss";
  import { navigating, page } from "$app/stores";
  import { browser } from "$app/environment";
  import { showSpinner } from "$lib/store/spinner.js";
  import { authStore } from "$lib/store/auth.js";

  let id = $page.params.id;

  $: {
    if (browser && navigating) {
      showSpinner($navigating?.complete, true);
    }
  }

  export let data;

  async function handleAuthStateChange(data) {
    if (!browser) return;

    const user = data?.user;

    authStore.set({
      ...$authStore,
      ...user,
      isAuthenticated: user ? true : false,
    });
  }

  $: handleAuthStateChange(data);
</script>

<Toaster {id} />

<Spinner />

<div
  class="scroll-body relative flex h-full min-h-screen flex-col overflow-auto md:flex-row"
>
  <div class="h-screen min-h-full w-full bg-white">
    <slot />
  </div>
</div>
