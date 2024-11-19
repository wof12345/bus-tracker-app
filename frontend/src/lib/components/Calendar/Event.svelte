<script>
  import { IconCircleFilled } from "@tabler/icons-svelte";
  import { getHours } from "date-fns";
  import { twMerge } from "tailwind-merge";

  export let event;
  export let currentView;
  let sessionHour;

  if (event?.time) {
    const sessionDate = new Date(event.time);
    if (!isNaN(sessionDate)) {
      sessionHour = sessionDate.getUTCHours();
    } else {
      console.error("Invalid date format for session_time");
    }
  }

  function formatTime(timestamp) {
  const date = new Date(timestamp);
  let hours = date.getUTCHours(); // Get hours in UTC
  const minutes = date.getUTCMinutes(); // Get minutes
  const ampm = hours >= 12 ? "PM" : "AM";

  // Convert 24-hour time to 12-hour format
  hours = hours % 12;
  hours = hours ? hours : 12; // If hours equals 0, set to 12
  
  // Format hours and minutes to always show two digits
  const formattedHours = String(hours).padStart(2, '0');
  const formattedMinutes = String(minutes).padStart(2, '0');

  // Return the formatted time
  return `${formattedHours}:${formattedMinutes} ${ampm}`;
}
</script>

<button
  on:click|stopPropagation
  class={twMerge(
    `my-1 flex w-max items-center justify-start gap-x-2 rounded-lg px-2 py-0.5 text-sm font-medium leading-[21px] text-primary-800 md:bg-primary-100 hover:bg-slate-200`,
    $$props.class,
  )}
>
  <IconCircleFilled size={10} />
  <span>{event.time ? formatTime(event.time) : 'Not found'}</span>
  <span> {event?.service.category.name ?? 'Unknown'}</span>
</button>
