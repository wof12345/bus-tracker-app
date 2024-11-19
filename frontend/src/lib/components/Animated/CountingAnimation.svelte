<script>
  import { fly, fade } from "svelte/transition";
  import { onMount } from "svelte";
  import { twMerge } from "tailwind-merge";

  export let number = 0;
  export let initial = 0;
  export let delay = 200;
  export let inbetweenDelay = (400 * 10) / 100;
  export let incrementalDelay = true;

  export let counterSlowdownThreshold = 10;

  export let transitionDuration = 120;

  let iteration = 0;
  let halfIteration = 0;
  let iterationGap = 1;
  let iterationGapIncrementalValue = 15;

  let countingInterval = () => {};

  let numberCurrentVisible = true;
  let numberBeforeVisible = false;

  function determineIncrementalValue(initial = 1) {
    if (number - initial >= (number * 50) / 100 && number > 10000) {
      iterationGapIncrementalValue = 1000;
    } else if (number - initial >= (number * 50) / 100 && number > 1000) {
      iterationGapIncrementalValue = 100;
    } else if (number - initial >= (number * 20) / 100 && number > 500) {
      iterationGapIncrementalValue = 20;
    } else if (number - initial >= (number * 10) / 100 && number > 100) {
      iterationGapIncrementalValue = 10;
    } else if (number - initial >= (number * 1) / 100 && number > 50) {
      iterationGapIncrementalValue = 0;
      iterationGap = 6;
    } else {
      iterationGapIncrementalValue = 0;
      iterationGap = 1;
    }

    iterationGap += iterationGapIncrementalValue;

    if (iterationGap > (number * 2) / 100) {
      iterationGap = Math.ceil((number * 2) / 100);
    }

    if (initial + iterationGap > number) {
      iterationGap = 1;
    }

    return iterationGap;
  }

  function handleIncrementalReduction(initial, iteration) {
    let delayNegateFactor = iteration * 40;

    if (initial > number - counterSlowdownThreshold) {
      halfIteration++;
      delayNegateFactor = 0;
    }

    let totalDelay = delay - delayNegateFactor;

    if (incrementalDelay) return totalDelay > 0 ? totalDelay : 10;
    else return 0;
  }

  onMount(() => {
    function startCounting() {
      if (initial < number) {
        if (initial > 0) {
          numberBeforeVisible = true;
          numberCurrentVisible = false;

          setTimeout(() => {
            numberBeforeVisible = false;

            numberCurrentVisible = true;
          }, inbetweenDelay);
        }

        iteration++;

        initial += determineIncrementalValue(initial);

        countingInterval = setTimeout(
          startCounting,
          handleIncrementalReduction(initial, iteration) + inbetweenDelay,
        );
      } else {
        clearTimeout(countingInterval);
      }
    }

    countingInterval = setTimeout(startCounting, delay);

    return () => clearInterval(countingInterval);
  });
</script>

<div class="relative">
  {#if initial - 1 > 0 && initial != number && numberBeforeVisible}
    <div
      class={twMerge("number-before absolute left-0 top-0 ", $$props.class)}
      transition:fade={{ duration: transitionDuration }}
    >
      {initial}
    </div>
  {/if}
  {#if numberCurrentVisible}
    <div
      class={twMerge("number", $$props.class)}
      out:fly={{ y: 20, duration: transitionDuration }}
    >
      {(initial > number ? number : initial).toLocaleString()}
    </div>
  {/if}
</div>
