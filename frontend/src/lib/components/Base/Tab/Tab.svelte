<script>
  import { onMount, afterUpdate } from "svelte";
  import { twMerge } from "tailwind-merge";

  import { goto, pushState } from "$app/navigation";
  import { v4 as uuidv4 } from "uuid";
  import { addSeachParamToURL } from "$components/utils/routeValidation";

  export const id = uuidv4();
  export let active = 0;
  export let onTabChange = () => {};
  export let invokeLoadOnTabChange = false;

  let clickEventAdded = false;

  function activateTab() {
    const tab = document.querySelector(`.tab-${id}`);

    const tabHeaders = tab?.querySelectorAll(".tab-header");
    const tabPanels = tab?.querySelectorAll(".tab-panel");

    if (!tabPanels || !tabHeaders) return;

    tabPanels?.forEach((elm, idx) => {
      elm.id = `tab-panel-${id}_${idx}`;

      if (active === idx) elm.classList.remove("hidden");
    });

    tabHeaders?.forEach((elm, idx) => {
      elm.id = `tab-header-${id}_${idx}`;
      let value = elm.dataset["value"];

      if (active === idx) {
        elm.classList.add("tab-active");
        elm.classList.remove("tab-inactive");
      }

      if (clickEventAdded) return;

      elm.addEventListener("click", (e) => {
        clickEventAdded = true;

        if (active == idx) {
          updateURL(value ?? idx);

          tabPanels[idx].classList.remove("hidden");
          tabHeaders[idx].classList.remove("tab-inactive");
          tabHeaders[idx].classList.add("tab-active");
          onTabChange(active);
          return;
        }

        tabPanels?.forEach((elm, idx) => {
          tabHeaders[idx].classList.remove("tab-active");
          tabHeaders[idx].classList.add("tab-inactive");
          elm.classList.add("hidden");
        });

        active = idx;
      });
    });

    tabHeaders[active]?.click();
  }

  function updateURL(tabValue) {
    let newUrl = addSeachParamToURL({ key: "tab", value: tabValue });
    if (invokeLoadOnTabChange) {
      goto(newUrl, { keepFocus: true });
    } else {
      pushState(newUrl, {});
    }
  }

  onMount(() => {
    activateTab();
  });

  afterUpdate(() => {
    activateTab();
  });
</script>

<div class={twMerge(`tab-${id} flex flex-col gap-6`, $$props.class)}>
  <slot {id} />
</div>
