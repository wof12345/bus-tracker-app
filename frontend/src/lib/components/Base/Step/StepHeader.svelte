<script lang="ts">
  import { twMerge } from "tailwind-merge";
  import { step_active } from "$components/Base/Step/stepStore";

  export let textPrimary = "";
  export let textSecondary = "";
  export let textPrimaryClass = "";
  export let textSecondaryClass = "";
  export let midline = false;

  export let length: boolean = true;

  let header;
</script>

<div
  bind:this={header}
  class={twMerge(
    `step-header step-inactive relative z-20 flex min-w-[150px] items-center justify-center overflow-auto text-sm hover:cursor-pointer `,
    $$props.class,
  )}
>
  <div
    class={`step-container flex overflow-visible ${length ? "flex-row" : "flex-col"} w-full`}
  >
    <div
      class={`flex ${length ? "flex-col items-center justify-center" : "justify-center"} `}
    >
      <div
        class={twMerge(
          "step-circle flex items-center rounded-full",
          $$props.nodeClass,
        )}
      >
        <div
          class="step-circle flex items-center justify-center rounded-full bg-transparent"
        >
          <div class="inactive-state">
            <slot />
          </div>
          {#if $$slots.activeState}
            <div class="active-state">
              <slot name="activeState" />
            </div>
          {:else}
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="active-state active-state-inactive"
              width="32"
              height="32"
              viewBox="0 0 32 32"
              fill="none"
            >
              <rect width="30" height="30" x="1" y="1" fill="#EFF8FF" rx="15"
              ></rect>
              <rect
                width="30"
                height="30"
                x="1"
                y="1"
                stroke="#1570EF"
                stroke-width="2"
                rx="15"
              ></rect>
              <circle cx="16" cy="16" r="5" fill="#1570EF"></circle>
            </svg>
          {/if}
        </div>
      </div>
      <div
        class={`step-progress  ${length ? "ml-[2px] h-12 w-0.5 bg-[#F6D0FE]" : " xs:left-24  absolute left-24   top-5 h-0.5 w-full max-w-lg sm:left-28 md:left-28 md:w-56   "} ${midline ? ($step_active === 1 ? "h-0.5 w-32 bg-[#BA24D5]" : "bg-[#EAECF0]") : "bg-[#EAECF0]"} `}
      ></div>
    </div>

    <div class={twMerge("ml-2.5 mt-1.5", $$props.textClass)}>
      {#if length}
        <div
          class={twMerge(
            "text-base font-semibold text-white",
            $$props.primaryTextClass,
          )}
        >
          {textPrimary}
        </div>
        <div
          class={twMerge(
            "text-base font-normal text-[#EEAAFD]",
            $$props.secondaryTextClass,
          )}
        >
          {textSecondary}
        </div>
      {:else}
        <div class="min-h-[30px]">
          <div
            class={twMerge(
              ` text-base font-semibold md:block ${textPrimaryClass}`,
              $$props.primaryTextClass,
            )}
          >
            {textPrimary}
          </div>
          <div
            class={twMerge(
              `text-base font-normal ${textSecondaryClass}`,
              $$props.secondaryTextClass,
            )}
          >
            {textSecondary}
          </div>
        </div>
      {/if}
    </div>
  </div>
</div>
