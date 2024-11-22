<script lang="ts">
  import { twMerge } from "tailwind-merge";
  import { v4 as uuidv4 } from "uuid";
  import { onMount } from "svelte";

  export let name: any;
  export let error: any;
  export let type: any = undefined;
  export let fileHover = false;
  export let disabled = false;

  const id = uuidv4();
  const classId = `frame-${id}`;

  onMount(() => {
    const frame = document.querySelector("." + classId);

    frame?.addEventListener("click", (e) => {
      let input = frame.querySelector("input");
      input?.focus();
      if ((type || input?.type) == "text") input?.click();

      let textarea = frame.querySelector("textarea");
      textarea?.focus();
    });
  });
</script>

<label
  for={name}
  on:click={() => {
    if ($$props.clickAction) $$props.clickAction();
  }}
  class={twMerge(
    `${classId} input-frame flex h-full w-full flex-1 items-center gap-1 rounded-lg border border-gray-300 bg-white px-2.5  py-2.5 text-md font-medium shadow-xs  outline-none ${disabled ? "bg-gray-100 hover:cursor-not-allowed" : ""} ${fileHover ? "hover:ring-[#BA24D5] hover:ring-2" : "focus-within:ring-4 focus-within:ring-[#9E77ED3D] focus-within:border-[#EEAAFD]"}  ${
      error ? "border border-[#FDA29B] focus-within:ring-red-100" : ""
    }`,
    $$props.class,
  )}
>
  <slot />
</label>
