<script>
  import { twMerge } from "tailwind-merge";
</script>

<div
  class={twMerge(
    "m-1 flex aspect-square max-h-[17px] w-5 flex-col justify-around gap-0.5 [&>*]:h-0.5 [&>*]:rounded-lg [&>*]:bg-primary-100",
    $$props.class,
  )}
>
  <div class="w-full"></div>
  <div class="w-[70%]"></div>
  <div class="w-full"></div>
</div>
