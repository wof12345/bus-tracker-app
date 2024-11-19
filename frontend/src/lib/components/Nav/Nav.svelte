<script lang="ts">
  import Logo from "./Logo.svelte";

  import IconButton from "../Base/Buttons/IconButton.svelte";

  import HamBurger from "./HamBurger.svelte";
  import SideBarMenu from "./SideBarMenu.svelte";
  import Button from "$components/Base/Buttons/Button.svelte";

  export let nav: boolean = false;

  let sideBarMenu: SideBarMenu;
  let sideMenuVisible: boolean;
  export let notificationData;
</script>

{#if nav}
  <nav
    class="sticky top-0 z-40 mx-auto flex h-[72px] w-full items-center justify-between py-4 xl:pr-[60px]"
  >
    <div class="flex items-center justify-center gap-8">
      <Logo />
      <div class="flex justify-start gap-8">
        <a
          href="/landing"
          class="hidden text-base font-semibold text-[#475467] md:block"
        >
          Find tutors
        </a>
        <a
          href="/landing"
          class="hidden text-base font-semibold text-[#475467] md:block"
        >
          Find tutors
        </a>
      </div>
    </div>

    <div class="flex gap-4">
      <Button
        class="hidden w-full max-w-[129px] py-3 text-base font-semibold text-[#475467] md:block"
        variant="borderless"
      >
        Log in
      </Button>
      <Button
        class="hidden w-full max-w-[129px] py-3 text-base  font-semibold md:block"
        variant="primary"
      >
        Sign up
      </Button>
    </div>

    {#if !sideMenuVisible}
      <IconButton
        class="flex p-1  md:hidden "
        on:click={() => {
          sideBarMenu.show();
        }}
      >
        <HamBurger />
      </IconButton>
    {/if}
  </nav>
{:else}
  <SideBarMenu
    {notificationData}
    bind:this={sideBarMenu}
    bind:visible={sideMenuVisible}
  />
{/if}
