<script>
  import { onMount, afterUpdate, onDestroy } from "svelte";
  import { twMerge } from "tailwind-merge";
  import { step_active } from "$components/Base/Step/stepStore";
  import { v4 as uuidv4 } from "uuid";
  import "./step.css";

  export let active = 0;
  export let navigateOnClick = true;
  export let optionalHiddenFLag = false;

  const id = uuidv4();

  let clickEventAdded = false;

  // Function to activate the appropriate step
  function activateStep() {
    // Get all necessary elements
    const step = document.querySelector(`.step-${id}`);

    if (!step) return;

    const stepHeaders = step.querySelectorAll(".step-header");
    const stepPanels = step.querySelectorAll(".step-panel");
    const activeStates = step.querySelectorAll(".active-state");
    const inactiveStates = step.querySelectorAll(".inactive-state");
    const progress = step.querySelectorAll(".step-progress");

    if (
      !stepHeaders ||
      !stepPanels ||
      !progress ||
      !inactiveStates ||
      !activeStates ||
      !progress[progress.length - 1]
    )
      return;

    // Hide progress bar for the last step
    progress[progress.length - 1].style.display = "none";

    if (optionalHiddenFLag) {
      clickEventAdded = false;
    }

    // Loop through each step
    stepHeaders.forEach((header, i) => {
      // Remove classes from all steps
      header.id = `step-header-${id}_${i}`;
      stepPanels[i].classList.add("step-panel-inactive");
      header.classList.remove("step-active", "step-inactive");
      inactiveStates[i].classList.remove("active-state-inactive");
      activeStates[i].classList.add("active-state-inactive");

      // Add click event listener to each step header

      if (clickEventAdded) return;
      header.addEventListener("click", () => {
        clickEventAdded = true;

        if (!navigateOnClick && active < i) {
          active = active;
          return;
        }

        // Deactivate all steps
        stepHeaders.forEach((h, j) => {
          stepPanels[j].classList.add("step-panel-inactive");
          h.classList.remove("step-active");
          h.classList.add("step-inactive");
          inactiveStates[j].classList.remove("active-state-inactive");
          activeStates[j].classList.add("active-state-inactive");
          if (j < progress.length - 1)
            progress[j].classList.remove("progress-active");
        });

        // Activate the clicked step
        $step_active = i;
        stepPanels[i].classList.remove("step-panel-inactive");
        header.classList.add("step-active");
        header.classList.remove("step-inactive");
        inactiveStates[i].classList.remove("active-state-inactive");
        activeStates[i].classList.add("active-state-inactive");
        for (let j = 0; j <= i; j++) {
          if (j < progress.length - 1)
            progress[j].classList.add("progress-active");
        }

        // Add 'completed' class to previous steps
        for (let k = 0; k < i; k++) {
          stepHeaders[k]?.classList.add("completed");
        }
        // Remove 'completed' class from incomplete steps
        for (let k = i; k < stepPanels.length; k++) {
          stepHeaders[k]?.classList.remove("completed");
        }
      });
    });

    // Activate the initially active step
    stepHeaders[active].click();
  }

  onMount(() => {
    activateStep();
  });

  afterUpdate(() => {
    activateStep();
  });

  onDestroy(() => {
    clickEventAdded = false;
  });
</script>

<div class={twMerge(`step-${id} step flex flex-col gap-2`, $$props.class)}>
  <slot {id} />
</div>
