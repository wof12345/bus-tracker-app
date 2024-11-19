<script>
  import Logo from "../../components/Assets/Logo.svelte";
  import LogoAlternative from "../../components/Assets/LogoAlternative.svelte";
  import LogoMobile from "$components/Assets/LogoMobile.svelte";
  import LogoAlternativeMobile from "$components/Assets/LogoAlternativeMobile.svelte";
  import { authStore } from "$lib/store/auth";
  import { goto } from "$app/navigation";

  export let alt = false;

  function go() {
    if ($authStore.isAuthenticated) {
      goto("/home");
    } else {
      goto("/");
    }
  }
</script>

<div class="h-10 w-10" on:click={go}>
  {#if alt}
    <div class="hidden md:block cursor-pointer h-full w-full">
      <img src="/logo.svg" alt="" />
    </div>
    <div class="md:hidden cursor-pointer">
      <LogoAlternativeMobile />
    </div>
  {:else}
    <div class="hidden md:block cursor-pointer w-full">
      <Logo />
    </div>
    <div class="md:hidden cursor-pointer">
      <LogoMobile />
    </div>
  {/if}
</div>
