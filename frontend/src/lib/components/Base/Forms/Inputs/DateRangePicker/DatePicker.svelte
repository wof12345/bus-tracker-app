<script>
  // @ts-nocheck

  import Popover from "./Popover.svelte";
  import { dayjs } from "./lib/date-utils";
  import { contextKey, setup } from "./lib/context";
  import { createEventDispatcher, setContext, getContext } from "svelte";
  import { CalendarStyle } from "./calendar-style.js";
  import { createViewContext } from "./lib/view-context.js";
  import View from "./view/View.svelte";
  import { v4 as uuidv4 } from "uuid";
  import { IconCalendar } from "@tabler/icons-svelte";
  import Button from "$components/Base/Buttons/Button.svelte";
  import { datePickerStore, addDates, clearDates } from "./lib/highlight.js";
  import Spinner from "$components/Base/Spinner.svelte";

  export let range = false;
  export let defaultRange = [1, "year"];
  export let placeholder = "Date";
  export let format = "DD / MM / YYYY";
  export let start = dayjs().subtract(1, "year");
  export let end = dayjs().add(1, "year");
  export let trigger = null;
  export let selectableCallback = null;
  export let styling = new CalendarStyle();
  export let selected;
  export let closeOnFocusLoss = true;
  export let time = false;
  export let morning = 7;
  export let night = 19;
  export let minuteStep = 5;

  export let loader = false;

  export let onSelectConfirm = (slected) => {};

  const dispatch = createEventDispatcher();

  let id = uuidv4();

  const startContextKey = {};
  const endContextKey = {};

  const config = {
    start: dayjs(start),
    end: dayjs(end),
    isRangePicker: range,
    defaultRange,
    isTimePicker: time,
    closeOnFocusLoss,
    format,
    morning,
    night,
    selectableCallback,
    minuteStep: minuteStep.toString(),
  };

  setContext(contextKey, setup(selected, config));
  const {
    selectedStartDate,
    selectedEndDate,
    isOpen,
    isClosing,
    highlighted,
    formatter,
    isDateChosen,
    isSelectingFirstDate,
    component,
  } = getContext(contextKey);

  setContext(startContextKey, createViewContext(true, getContext(contextKey)));

  if (config.isRangePicker) {
    setContext(endContextKey, createViewContext(false, getContext(contextKey)));
  }

  let popover;

  let fromDate = "";
  let toDate = "";

  function initialisePicker() {
    highlighted.set($selectedStartDate);
    dispatch("open");
  }

  function dateInStore() {
    let selectedDay = dayjs(selected);

    for (let date in $datePickerStore.dates) {
      let sessionDate = dayjs(date);

      if (dayjs(selectedDay).isSame(dayjs(sessionDate), "date")) {
        return true;
      }
    }

    return false;
  }

  function setRangeValue() {
    selected = [$selectedStartDate, $selectedEndDate];
    dispatch("range-selected", {
      from: $selectedStartDate.toDate(),
      to: $selectedEndDate.toDate(),
    });
  }

  function setDateValue() {
    selected = $selectedStartDate.toDate();
    dispatch("date-selected", {
      date: $selectedStartDate.toDate(),
    });
  }

  function swapDatesIfRequired() {
    if (!config.isRangePicker) {
      return;
    }
    const from = $selectedStartDate;
    const to = $selectedEndDate;
    if (to.isBefore(from)) {
      selectedStartDate.set(to);
      selectedEndDate.set(from);
    }
  }

  function addDate(e) {
    const { date } = e.detail;

    if ($isSelectingFirstDate) {
      selectedStartDate.set(date);
    } else {
      selectedEndDate.set(date);
    }

    swapDatesIfRequired();
    finalise();
    setDateValue();
    config.isRangePicker && isSelectingFirstDate.update((v) => !v);
  }

  $: {
    if ($isDateChosen) {
      config.isRangePicker ? setRangeValue() : setDateValue();
      dispatch("change");
    }
  }

  function finalise() {
    isDateChosen.set(true);
    dispatch("close");
  }

  function progress() {
    isDateChosen.set(false);
    if ($component === "date-view") {
      if (config.isTimePicker) {
        component.set("time-view");
      } else {
        finalise();
      }
    } else if ($component === "time-view") {
      finalise();
    }
  }
</script>

<div
  class="datepicker relative w-full input-{id}"
  class:open={$isOpen}
  class:closing={$isClosing}
  style={styling.toWrapperStyle()}
>
  <div class=" z-10 w-full">
    <Popover
      {trigger}
      {id}
      bind:this={popover}
      on:opened={initialisePicker}
      on:closed={() => dispatch("close")}
    >
      <div slot="trigger" class="hover:cursor-pointer">
        <slot formatted={$formatter}>
          {#if $$slots.trigger}
            <slot name="trigger"></slot>
          {:else}
            <IconCalendar />
          {/if}
        </slot>
      </div>

      <div
        class="contents w-full"
        slot="contents"
        class:is-range-picker={config.isRangePicker}
      >
        <div
          class="view md:flex flex-col items-center md:px-10 px-0 pb-1 w-full max-w-[287px]"
        >
          <View viewContextKey={startContextKey} on:chosen={addDate} />
          {#if config.isRangePicker}
            <div class="range min-w-[30%]">
              <div class="hidden w-full md:block">
                <p class="text-[#1C1C1C] font-normal text-xs mb-2">From</p>
                <input
                  class="text-box border rounded-md py-4 pl-2 lg:max-w-auto w-full"
                  value={$selectedStartDate.format("MM/DD/YYYY")}
                  placeholder="MM/DD/YYYY"
                  type="text"
                  on:change={(e) => {
                    if (e.target) {
                      selectedStartDate.set(
                        dayjs(e.target.value, "MM/DD/YYYY"),
                      );
                    } else {
                      selectedStartDate.set(dayjs(new Date(), "MM/DD/YYYY"));
                    }
                  }}
                  on:keydown={(e) => {
                    if (e.key === "Enter") {
                      if (fromDate) {
                        selectedStartDate.set(dayjs(fromDate, "MM/DD/YYYY"));
                      }
                    }
                  }}
                />
              </div>
              <div class="hidden md:block">
                <p class="text-[#1C1C1C] font-normal text-xs mb-2">To</p>
                <input
                  class="text-box border rounded-md py-4 pl-2 w-full"
                  value={$selectedEndDate.format("MM/DD/YYYY")}
                  placeholder="MM/DD/YYYY"
                  type="text"
                  on:change={(e) => {
                    if (e.target) {
                      selectedEndDate.set(dayjs(e.target.value, "MM/DD/YYYY"));
                    } else {
                      selectedEndDate.set(dayjs(new Date(), "MM/DD/YYYY"));
                    }
                  }}
                  on:keydown={(e) => {
                    if (e.key === "Enter") {
                      if (toDate) {
                        selectedEndDate.set(dayjs(toDate, "MM/DD/YYYY"));
                      }
                    }
                  }}
                />
              </div>
            </div>
          {/if}
          <div class="w-full relative flex gap-2">
            {#if loader}
              <Spinner class="absolute top-0 left-0 scale-50" show={loader} />
            {/if}

            <Button
              class="w-max m-auto"
              onClick={() => onSelectConfirm(selected)}>Continue</Button
            >
          </div>
        </div>
      </div>
    </Popover>
  </div>
</div>

<style>
  @import url("https://fonts.googleapis.com/css2?family=Manrope:wght@200..800&display=swap");

  .range {
    display: flex;
    flex-direction: column;
    gap: 20px;
    text-align: start;
    margin: 0px 2px 0px 16px;
    font-size: 13px;
  }
</style>
