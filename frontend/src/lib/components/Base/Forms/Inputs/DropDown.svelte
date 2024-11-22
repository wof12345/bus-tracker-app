<script lang="ts">
  import { v4 as uuidv4 } from "uuid";
  import { twMerge } from "tailwind-merge";
  import { IconChevronDown, IconX } from "@tabler/icons-svelte";
  import InputContainer from "../Components/InputContainer.svelte";
  import InputFrame from "../Components/InputFrame.svelte";
  import DropDownMenu from "../Components/DropDownMenu.svelte";

  const id = uuidv4();

  export let value: any = "";
  export let label: string = "";
  export let type: string = "string";
  export let placeholder: any = undefined;
  export let disabled: boolean = false;
  export let error: any = undefined;
  export let name: any = `${type}-${id}`;
  export let required: boolean = true;
  export let onSelectCloseMenu: boolean = true;
  export let editable: boolean = false;
  export let doubleRangeSlide: boolean = false;
  export let options: any = [];
  export let active: any = 0;
  export let formData: any = {};
  export let icon: boolean = false;
  export let onInput = () => {};
  export let onSelect = (idx: number, option: any) => {};
  export let open = false;
  export let down: boolean = true;
  export let start = 0;
  export let end = 1;
  export let relativeScrollElement;
  export let areaDropDown = false;
  export let showIconX = false;

  let textColor = false;

  const idClass = `dropdown-instigator-${id}`;
  let itemMenu: Menu;
  let selectedIcon: null;

  let selectedItem;

  const handleClick = (idx: number, option: any, selectedElm: any) => {
    value = formData[name] = option.value || option;

    active = option.value;

    selectedIcon = option.icon;

    if (selectedElm) {
      var tmp = document.createElement("div");
      tmp.appendChild(selectedElm);
      selectedItem = "" + tmp.innerHTML;
    }

    onSelect(idx, option);
    if (onSelectCloseMenu) itemMenu.hide();
    else return;
  };

  function getValue() {
    let optionValue;
    optionValue = options.find(function (elm) {
      return (
        elm.value + "" === value?.value + "" ||
        elm.value + "" === value + "" ||
        elm + "" === value + ""
      );
    });

    selectedIcon = options[active]?.icon;

    if (!optionValue) return formData[name] || value || "";

    return optionValue;
  }

  function handleFocus() {
    textColor = true;
    options.forEach((item) => {
      if (item.value === value) {
        placeholder = item.name;
        textColor = true;
      }
    });
    value = undefined;
  }
</script>

<div
  class={twMerge(
    `input-${id} relative w-full flex-1`,
    $$props.containerParentClass,
  )}
>
  <InputContainer onclass={$$props.containerClass} {value} bind:error>
    <InputFrame
      clickAction={() => {
        if (disabled) return;
        if (!open) itemMenu.show();
        else itemMenu.hide();
      }}
      {itemMenu}
      {id}
      {type}
      class={`hover:cursor-pointer ${$$props.class}`}
      {error}
      {name}
      {disabled}
      {value}
    >
      <div class="flex w-full items-center gap-2">
        <slot />

        {#if !doubleRangeSlide && down}
          {#if selectedIcon}
            <svelte:component this={selectedIcon} />
          {/if}
          <input
            class={twMerge(
              `w-full font-normal text-base overflow-hidden text-ellipsis bg-transparent outline-none ${textColor ? "placeholder:text-gray-400" : "placeholder:text-[#101828]"} ${disabled ? "cursor-not-allowed" : ""}`,
              $$props.inputClass,
            )}
            type={type === "string" ? "text" : type}
            {name}
            placeholder={placeholder ||
              options[active]?.name ||
              options[active] ||
              label + ""}
            value={value?.name ||
              getValue(value)?.name ||
              (typeof value === "string" ? value : undefined) ||
              ""}
            onkeypress={!editable ? "return false" : ""}
            autocomplete="off"
            {disabled}
            style={!editable ? "caret-color: transparent !important;" : ""}
            on:focus={() => handleFocus()}
            on:keypress={() => {
              return false;
            }}
            on:input={onInput}
          />
        {:else}
          <input
            class={twMerge(
              `w-full font-normal text-base overflow-hidden text-ellipsis bg-transparent outline-none ${textColor ? "placeholder:text-gray-400" : "placeholder:text-[#101828]"} hover:cursor-pointer ${disabled ? "cursor-not-allowed" : ""}`,
              $$props.inputClass,
            )}
            type={type === "string" ? "text" : type}
            {name}
            placeholder={placeholder ||
              options[active]?.name ||
              options[active] ||
              label + ""}
            value={value?.name ||
              getValue(value)?.name ||
              (typeof value === "string" ? value : undefined) ||
              ""}
            onkeypress={!editable ? "return false" : ""}
            autocomplete="off"
            {disabled}
            style={!editable ? "caret-color: transparent !important;" : ""}
            on:keypress={() => {
              return false;
            }}
            on:input={onInput}
          />
        {/if}

        {#if showIconX}
          <IconX color="#98A2B3" size={20} />
        {:else if areaDropDown}
          {#if placeholder === "" || placeholder === "Any"}
            <div
              class="-mr-3 flex h-full min-w-[30px] items-center justify-center bg-transparent pt-0.5 transition delay-100 hover:cursor-pointer"
              style={open ? "transform: rotate(-180deg);" : ""}
            >
              {#if !$$slots.icon}
                <IconChevronDown color="#98A2B3" size={20} />
              {:else}
                <slot name="icon" />
              {/if}
            </div>
          {:else}
            <IconX color="#98A2B3" size={20} />
          {/if}
        {:else}
          <div
            class="-mr-3 flex h-full min-w-[30px] items-center justify-center bg-transparent pt-0.5 transition delay-100 hover:cursor-pointer"
            style={open ? "transform: rotate(-180deg);" : ""}
          >
            {#if !$$slots.icon}
              <IconChevronDown color="#98A2B3" size={20} />
            {:else}
              <slot name="icon" />
            {/if}
          </div>
        {/if}
      </div>

      <slot name="pills-container" />
    </InputFrame>
  </InputContainer>

  {#if $$slots.menu_items}
    <DropDownMenu
      class={$$props.menuClass}
      bind:open
      {handleClick}
      {idClass}
      {id}
      bind:itemMenu
      {options}
      {doubleRangeSlide}
      bind:start
      bind:end
      {relativeScrollElement}
    >
      <div slot="menu_items">
        <slot name="menu_items" />
      </div>
    </DropDownMenu>
  {:else}
    <DropDownMenu
      class={$$props.menuClass}
      bind:open
      {handleClick}
      {idClass}
      {id}
      bind:itemMenu
      {options}
      {doubleRangeSlide}
      bind:start
      bind:end
    ></DropDownMenu>
  {/if}
</div>

<style>
  .blurred-placeholder::placeholder {
    color: #bfbfbf;
    opacity: 0.5;
  }

  .input-focused {
    color: red;
  }
</style>
