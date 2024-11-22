<script lang="ts">
  import Menu from "$lib/components/Base/Menu/Menu.svelte";
  import MenuItems from "$lib/components/Base/Menu/MenuItems.svelte";
  import { twMerge } from "tailwind-merge";
  import Option from "./Option.svelte";
  import DoubleRangeSlider from "$components/Base/Forms/Inputs/DoubleRangeSlider.svelte";

  export let options: any = [];
  export let idClass: string = "";
  export let id: number;
  export let open: boolean = false;
  export let doubleRangeSlide: boolean = false;
  export let relativeScrollElement;

  export let itemMenu: Menu;
  export let menuElement: Menu;

  export let handleClick: any;

  export let start = 0;
  export let end = 1;

  function handleMenuStateChange(open, menu) {
    const handleOptionClick = (e) => {
      let option = e.target;

      if (
        typeof option.className !== "string" ||
        !option?.className?.includes("option")
      ) {
        option = option.closest(".option");
      }

      let value = option.dataset["text"];

      handleClick(0, { value, undefined }, option);
    };

    menu?.removeEventListener("click", handleOptionClick);

    if (!open || !menu || !$$slots.menu_items) return;

    menu?.addEventListener("click", handleOptionClick);
  }

  $: handleMenuStateChange(open, menuElement);
</script>

<Menu
  bind:visible={open}
  bind:this={itemMenu}
  bind:menu={menuElement}
  {relativeScrollElement}
  {id}
  parentWidth={true}
  class={twMerge(
    `${idClass} my-1 max-h-[300px] w-full overflow-auto py-1`,
    $$props.class,
  )}
>
  <MenuItems>
    <!-- {#if !$$slots.menu_items} -->
    {#each options as option, idx}
      <Option
        value={option?.value || option}
        onClick={(value, icon) => {
          handleClick(idx, { value, icon }, option);
        }}
        icon={option.icon}
      >
        {option?.view_name || option?.name || option}
      </Option>
    {/each}
    <!-- TODO: it may be needs for dropdown control -->
    <!-- {:else} -->
    <!-- <slot name="menu_items">
        {#each options as option, idx}
          <Option
            value={option?.value || option}
            onClick={(value, icon) => {

              handleClick(idx, { value, icon });
            }}
            icon={option.icon}
          >
            {option?.name || option}
          </Option>
        {/each}
      </slot>
    {/if} -->
  </MenuItems>

  {#if doubleRangeSlide}
    <DoubleRangeSlider bind:start bind:end />
  {/if}
</Menu>
