<script lang="ts">
  import { twMerge } from "tailwind-merge";

  export let text: any = undefined;
  export let type: any = "button";
  export let src: any = undefined;
  export let disabled: any = false;
  export let name: any = "";
  type possibleVariants = "primary" | "secondary" | "approve" | "danger";

  export let variant: possibleVariants = "primary";

  export let onClick: any = () => null;

  function getPrimaryStyle(variant: string) {
    if (variant === "primary") {
      return "bg-[#BA24D5] border-[#9F1AB1] text-white hover:bg-[#9F1AB1] focus:ring-4 ring-[#9E77ED3D] shadow-xs border";
    }
    if (variant === "primary-disabled") {
      return "bg-[#BA24D5] border-[#9F1AB1] text-white hover:bg-[#9F1AB1] focus:ring-4 ring-[#9E77ED3D] shadow-xs border disabled";
    }
    if (variant === "approve") {
      return "bg-[#079455] border-[#079455] text-white hover:bg-[#079455] focus:ring-4 ring-[#9E77ED3D] shadow-xs border";
    }

    if (variant === "danger") {
      return "bg-[#D92D20] border-[#D92D20] text-white hover:bg-[#D92D20] focus:ring-4 ring-[#9E77ED3D] shadow-xs border";
    }

    if (variant === "secondary") {
      return "border-gray-300 font-medium bg-white text-gray-700 focus:ring-4 ring-gray-200 hover:bg-gray-50 shadow-xs border";
    }
    if (variant === "borderless") {
      return " font-medium bg-white text-gray-700";
    }
    if (variant === "hover") {
      return " font-medium bg-white text-gray-700 hover:bg-gray-50 bg-transparent border-[1px] border-transparent hover:shadow-xs hover:border hover:border-[#D0D5DD]";
    }

    if (variant === "disabled") {
      return "bg-[#F2F4F7] border-[#EAECF0] border-[1px] text-white text-[#98A2B3]  shadow-xs border-[1px]";
    }
    if (variant === "cancelDisable") {
      return "border-[#EAECF0] font-meddium bg-white text-[#98A2B3] focus:ring-2 ring-gray-200  shadow-xs border-[1px]";
    }
  }
</script>

<button
  {disabled}
  {type}
  {name}
  on:click={(e) => onClick(e)}
  class={twMerge(
    ` hover:cursor-pointer disabled:pointer-events-none disabled:opacity-50 ${getPrimaryStyle(
      variant,
    )} flex h-max w-full min-w-max items-center justify-center gap-2 rounded-lg  px-3.5 py-2.5 text-sm font-semibold transition delay-150`,
    $$props.class,
  )}
>
  {#if src}
    <img class="aspect-square w-5" {src} alt={src} />
  {/if}

  {#if !text}
    <slot />
  {:else}
    <p>{text}</p>
  {/if}
</button>
