<script>
  import IconButton from "$components/Base/Buttons/IconButton.svelte";
  import { digitizeNumber, truncateText } from "$components/utils/textMethods";
  import { IconChevronLeft, IconChevronRight } from "@tabler/icons-svelte";
  import Event from "./Event.svelte";

  export let weekDays = [];
  export let months = [];
  export let hours = [];
  export let minutes = [];
  export let hourClock = [];
  export let openEventModal;
  export let events;
  export let currentDay;
  export let weekDates;
  export let getSingleSessionData;

  function getTimestamp(day, month, year, hour, minute) {
    const date = new Date(year, month, day, hour, minute);
    return date.getTime();
  }
  function getTimestampFromDateString(dateString) {
    const date = new Date(dateString);
    date.setMonth(date.getMonth());
    const newTimestamp = date.getTime();
    return newTimestamp;
  }

  let currentMonth = new Date(currentDay).getMonth();

  export function generateHours(start, end) {
    const hours = [];
    for (let i = start; i < end; i++) {
      hours.push({ alias: `${i}:00`, value: (i == 0 ? 24 : i % 24) + "" });
    }
    return hours;
  }
  const availableHours = generateHours(0, 24);
</script>

<div
  class="main-week-calender grid"
  style="grid-template-columns: repeat({$$props.grid + 1}, 1fr);"
>
  <div class="border-b-2 border-gray-100"></div>

  {#each weekDays as day, index}
    <div
      class="gap-1.5 border border-gray-100 text-center text-sm leading-5 text-gray-500"
    >
      {day} <br />
      <span class="px-0 py-2 text-lg font-medium leading-7 text-gray-900"
        >{weekDates[index].date}</span
      >
    </div>
  {/each}

  {#each availableHours as hour, idx}
    <div
      class="flex items-center justify-center p-2 text-center text-sm leading-5 text-gray-500"
    >
      {hour?.alias || hour}
    </div>

    {#each weekDays as day, idx}
      <button class="relative flex cursor-pointer flex-col">
        <div
          class="flex relative h-14 w-full flex-col items-center justify-center border border-gray-100 hover:bg-gray-50"
        >
          {#each minutes.slice(0, minutes.length / 2) as minute}
            <button
              class="w-full flex-1"
              id={"d-" +
                weekDates[idx].date +
                "-" +
                currentMonth +
                "-" +
                weekDates[idx].year +
                "-" +
                hour?.value +
                "-" +
                minute}
              on:click={() => {
                let date = new Date(
                  weekDates[idx].year,
                  currentMonth,
                  weekDates[idx].date,
                  hour?.value,
                  minute,
                ).getTime();
                openEventModal(
                  weekDates[idx].year,
                  currentMonth,
                  weekDates[idx].date,
                  hour?.value,
                  minute,
                  idx < 12 ? "AM" : "PM",
                );
              }}
            >
              {#each events as event}
                {#if getTimestamp(weekDates[idx].date, currentMonth, weekDates[idx].year, parseInt(hour?.value) + 6, minute) === getTimestampFromDateString(event?.time)}
                  <Event
                    on:click={() => {
                      getSingleSessionData(event.id);
                    }}
                    {event}
                    currentView={"Week"}
                  />
                {/if}
              {/each}
            </button>
          {/each}
        </div>

        <div
          class="flex h-14 w-full flex-col items-center justify-center border border-gray-100 hover:bg-gray-50"
        >
          {#each minutes.slice(minutes.length / 2, minutes.length) as minute}
            <button
              class="w-full flex-1"
              id={"d-" +
                weekDates[idx].date +
                "-" +
                currentMonth +
                "-" +
                weekDates[idx].year +
                "-" +
                hour?.value +
                "-" +
                minute}
              on:click={() => {
                let date = new Date(
                  weekDates[idx].year,
                  currentMonth,
                  weekDates[idx].date,
                  hour?.value,
                  minute,
                ).getTime();
                openEventModal(
                  weekDates[idx].year,
                  currentMonth,
                  weekDates[idx].date,
                  hour?.value,
                  minute,
                  idx >= 12 ? "AM" : "PM",
                );
              }}
            >
              {#each events as event}
                {#if getTimestamp(weekDates[idx].date, currentMonth, weekDates[idx].year, parseInt(hour?.value) + 6, minute) === getTimestampFromDateString(event?.time)}
                  <Event {event} currentView={"Week"} />
                {/if}
              {/each}
            </button>
          {/each}
        </div>
      </button>
    {/each}
  {/each}
</div>
