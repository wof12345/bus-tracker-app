<script lang="ts">
  // @ts-nocheck
  import { fade } from "svelte/transition";

  import SubHeading from "$components/Base/Typography/SubHeading.svelte";
  import { onMount } from "svelte";
  import Button from "$components/Base/Buttons/Button.svelte";
  import {
    IconChevronLeft,
    IconChevronRight,
    IconDotsVertical,
  } from "@tabler/icons-svelte";
  import IconButton from "$components/Base/Buttons/IconButton.svelte";
  import Header from "$components/Base/Typography/Header.svelte";
  import Modal from "$components/Base/Modal/Modal.svelte";

  import ModalBody from "$components/Base/Modal/ModalBody.svelte";

  import InputGroup from "$components/Base/Forms/Components/InputGroup.svelte";

  import { deserialize } from "$app/forms";
  import WeekCalendar from "$components/Calendar/WeekCalendar.svelte";
  import Event from "$components/Calendar/Event.svelte";

  import { writable } from "svelte/store";

  import DropDown from "$components/Base/Forms/Inputs/DropDown.svelte";

  import { authStore, isStudent, isTeacher } from "$lib/store/auth.ts";

  import { showToaster } from "$lib/store/toaster.ts";

  import dayjs from "dayjs";
  import duration from "dayjs/plugin/duration";
  import { formData } from "$components/utils/formData.js";

  import Title from "$components/Base/Typography/Title.svelte";
  import Paragraph from "$components/Base/Typography/Paragraph.svelte";

  import Badge from "$components/Base/Badge.svelte";
  import BookModal from "$lib/layouts/Services/BookModal.svelte";
  import { validateApiResponse } from "$components/utils/validateApiResponse.js";
  import Spinner from "$components/Base/Spinner.svelte";
  import Menu from "$components/Base/Menu/Menu.svelte";
  import { truncateText } from "$components/utils/textMethods.js";
  dayjs.extend(duration);

  export let data;

  $: sessionsData = [];

  export const eventsStore = writable([]);

  let today = new Date();

  let currentMonth = today.getMonth();
  let currentYear = today.getFullYear();
  let days = [];
  let events = [];
  let status = "";

  let selectedHour;
  let selectedMinute;
  let selectedHourClock = "AM";
  let highlightTodayFlag = false;

  let selectedEvent;

  let grid = 7;
  let cnt = 0;
  let passData = "";

  let selectedCourse = "";

  let isHovered = false;

  $: modalData = {
    id: "",
    title: "",
    time: "",
    hosts: [],
    duration: "",
  };

  let bookModalResult;

  const monthNames = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];

  const weekDays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

  const hours = [
    "00",
    "01",
    "02",
    "03",
    "04",
    "05",
    "06",
    "07",
    "08",
    "09",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
    "21",
    "22",
    "23",
  ];

  const minutes = [];

  const hourClock = ["AM", "PM"];

  let addEventModal;

  let sessionModal;
  let rescheduleModal;
  let cancelModal;

  let session;

  let weekDates = [];

  const aDayInMiliSeconds = 24 * 60 * 60 * 1000;
  const aWeekInMiliSeconds = 7 * aDayInMiliSeconds;

  let currentDay = new Date().getTime();

  const viewOptions = ["Month View", "Week View"];
  let currentView = viewOptions[0];

  async function getSessions(start_time, end_time) {
    const data = new FormData();
    loadingCalendarData = true;

    data.append("start_time", start_time);
    data.append("end_time", end_time);

    const response = await fetch("?/getSessions", {
      method: "POST",
      body: data,
    });

    const result = deserialize(await response.text());

    if (!validateApiResponse(result)) {
      return;
    }

    sessionsData = result?.data?.data || [];

    loadingCalendarData = false;
  }

  function getDaysInMonth(month, year) {
    const date = new Date(year, month, 1);
    const days = [];
    while (date.getMonth() === month) {
      days.push(new Date(date).getDate());
      date.setDate(date.getDate() + 1);
    }
    return days;
  }

  function getFirstDayOfMonth(month, year) {
    return new Date(year, month, 1).getDay();
  }

  async function nextMonth() {
    if (currentMonth === 11) {
      currentMonth = 0;
      currentYear += 1;
    } else {
      currentMonth += 1;
    }
    await fetchEventsAndGenerateCalendar();
  }

  async function prevMonth() {
    if (currentMonth === 0) {
      currentMonth = 11;
      currentYear -= 1;
    } else {
      currentMonth -= 1;
    }
    await fetchEventsAndGenerateCalendar();
  }

  async function fetchEventsAndGenerateCalendar() {
    events = [];
    await getSessions(getStartOfMonth(), getEndOfMonth());
    generateCalendar(currentMonth, currentYear, cnt);
  }

  function getStartOfMonth() {
    return new Date(currentYear, currentMonth, 1).toISOString();
  }

  function getEndOfMonth() {
    return new Date(currentYear, currentMonth + 1, 0, 23, 59, 59).toISOString();
  }

  async function generateCalendar(month, year) {
    let startDate = new Date(year, month, 1);
    let startTime = startDate.toISOString();

    let endDate = new Date(year, month + 1, 0, 23, 59, 59);
    let endTime = endDate.toISOString();

    await getSessions(startTime, endTime);

    events = [];
    sessionsData?.forEach((item) => events.push(item));

    days = [];

    let prevMonth = month - 1;
    let nextMonth = month + 1;

    if (prevMonth < 0) {
      prevMonth = 11;
      year -= 1;
    }

    if (nextMonth > 11) {
      nextMonth = 0;
      year += 1;
    }

    const prevMonthDays = getDaysInMonth(prevMonth, year);
    const nextMonthDays = getDaysInMonth(nextMonth, year);
    const numOfDays = getDaysInMonth(month, year);
    const firstDay = getFirstDayOfMonth(month, year);

    const totalGrid = 6 * grid;

    for (
      let i = 0, prevIterator = prevMonthDays.length - firstDay;
      i < firstDay;
      i++, prevIterator++
    ) {
      days.push({ day: "", dayValue: prevMonthDays[prevIterator], events: [] });
    }

    for (let day of numOfDays) {
      const dayEvents = events.filter((event) => {
        const eventDate = new Date(event.time);
        return (
          eventDate.getDate() === day &&
          eventDate.getMonth() === month &&
          eventDate.getFullYear() === year
        );
      });

      days.push({
        day,
        events: dayEvents,
        hasEvent: dayEvents.length > 0,
        isToday:
          highlightTodayFlag &&
          day === today.getDate() &&
          month === today.getMonth() &&
          year === today.getFullYear(),
      });
    }

    passData = days;

    let remaining = totalGrid - (numOfDays.length - 1 + firstDay);
    for (let i = 0; i < remaining - 1; i++) {
      days.push({ day: "", dayValue: nextMonthDays[i], events: [] });
    }
  }

  async function getAndLaunchMeetingUrl() {
    let form = new FormData();

    if (!modalData.room_id) {
      showToaster("This session does not have any available meeting");
      return;
    }

    form.append("room_id", modalData.room_id);

    try {
      const response = await fetch("?/get_meeting_url", {
        method: "POST",
        body: form,
      });

      const result = deserialize(await response.text());

      if (!validateApiResponse(result)) {
        return;
      }

      let data = result.data.data;

      showToaster("Redirecting...");

      setTimeout(() => {
        window.open(data.url, "_blank");

        sessionModal.hide();
      }, 2000);
    } catch (error) {
      showToaster("There was an error generating room code");
    }
  }

  async function create(e) {
    const data = new FormData(e.currentTarget);

    data.append("session_type", selectedCourse);
    data.append("session_token", "");

    data.append("session_hour", selectedHour);
    data.append("session_minute", selectedMinute);
    data.append("session_clock", selectedHourClock);
    data.append("created_at", formattedDate);
    data.append("time", session);

    const response = await fetch("?/create", {
      method: "POST",
      body: data,
    });

    const result = deserialize(await response.text());

    if (!validateApiResponse(result)) {
      return;
    }

    let liveClassData = result.data.data;

    showToaster("Redirecting...");

    setTimeout(() => {
      window.open(liveClassData.url, "_blank");

      sessionModal.hide();
    }, 2000);
    await showSpinner(invalidateAll());

    addEventModal?.hide();

    generateCalendar(currentMonth, currentYear);

    applyAction(result);
  }

  function getWeekDates(currentDay) {
    const today = new Date(currentDay);
    currentYear = today.getFullYear();
    currentMonth = today.getMonth();

    const first = today.getDate() - today.getDay();
    const firstDayStamp = new Date(currentYear, currentMonth, first).getTime();
    const dates = [];
    status = "";
    const currentMonths = {};
    for (let i = 0; i < 7; i++) {
      const date = new Date(firstDayStamp + i * aDayInMiliSeconds);
      currentMonths[monthNames[date.getMonth()]] = date.getFullYear();
      dates.push({ date: `${date.getDate()}`, year: date.getFullYear() });
    }

    let statusCollection = Object.keys(currentMonths);
    statusCollection.forEach((key, idx) => {
      if (idx > 0) status += " - ";
      status += truncateText(
        `${key} ${currentMonths[key]}`,
        statusCollection.length > 1 && idx == 0 ? 15 : 15,
      );
    });
    weekDates = dates;
  }

  $: getWeekDates(currentDay);

  async function getSingleSessionData(id) {
    try {
      const response = await fetch("?/get_single_session", {
        method: "POST",
        body: formData({ session_id: id }),
      });

      const result = deserialize(await response.text());
      bookModalResult = result?.data;

      if (validateApiResponse(result)) {
        modalData.title = result.data.session.service.category.name;
        modalData["order_id"] = result.data.session.order_id;
        modalData["room_id"] = result.data.session.room_id;
        modalData.id = result.data.session.id;
        modalData.time = result.data.session.time;
        modalData.hosts = result.data.session.hosts;
        modalData.service_id = result.data.session.service.id;
        sessionModal.show();
      } else {
        showToaster("Failed to fetch session data");
      }
    } catch (error) {
      showToaster("There was an error generating room code");
    }
  }

  function highlightToday() {
    currentMonth = today.getMonth();
    currentYear = today.getFullYear();
    highlightTodayFlag = true;

    cnt++;
    if (cnt % 2 == 1) {
      generateCalendar(currentMonth, currentYear, cnt);
    } else {
      generateCalendar(currentMonth, currentYear, cnt);
    }
  }

  let joinSessionMenu: Menu;

  let joinSessionMenuVisible = false;

  function toggleMenuVisibility() {
    joinSessionMenuVisible = !joinSessionMenuVisible;
  }

  function handleJoinSessionMenu() {
    toggleMenuVisibility();
    if (joinSessionMenuVisible) {
      joinSessionMenu.show();
    } else {
      joinSessionMenu.hide();
    }
  }

  function handleDateTimeFormat(dateTimeString) {
    let date = new Date(dateTimeString);

    let options = {
      year: "numeric",
      month: "long",
      day: "numeric",
      hour: "numeric",
      minute: "numeric",
      hour12: true,
      timeZone: "UTC",
    };

    return new Intl.DateTimeFormat("en-US", options).format(date);
  }

  function toPreviousWeek() {
    currentDay -= aWeekInMiliSeconds;
  }

  function toNextWeek() {
    currentDay += aWeekInMiliSeconds;
  }

  let loadingCalendarData;

  onMount(() => {
    for (let i = 0; i <= 59; i++) {
      minutes.push(i < 10 ? "0" + i : i + "");
    }

    generateCalendar(currentMonth, currentYear);
  });
</script>

<div class="flex min-h-screen flex-col gap-4 px-4 py-10 md:px-10">
  <header class="top flex h-max flex-col gap-5">
    <Header class="text-3xl font-semibold leading-9 md:text-3xl"
      >Calendar</Header
    >
    <div
      class="flex h-full w-full flex-col items-center justify-between gap-4 xl:flex-row xl:gap-16"
    >
      <div
        class="flex h-full w-full max-w-[400px] flex-col items-center gap-3 xl:flex-row"
      >
        <div class="w-full xl:flex">
          <div class="w-full flex-col">
            <div class="flex w-full items-center justify-between gap-4">
              <Button
                variant="hover"
                class="w-7 border-none"
                onClick={() =>
                  currentView === "Month View" ? prevMonth() : toPreviousWeek()}
              >
                <IconChevronLeft />
              </Button>

              <SubHeading
                class="xl:text-md w-full text-center text-sm font-semibold text-gray-700 "
              >
                {#if currentView === "Month View"}
                  <span>{monthNames[currentMonth]} {currentYear}</span>
                {:else}
                  {status}
                {/if}
              </SubHeading>
              <Button
                variant="hover"
                class="w-7 border-none"
                onClick={() =>
                  currentView === "Month View" ? nextMonth() : toNextWeek()}
              >
                <IconChevronRight />
              </Button>
            </div>

            <div class="relative mx-auto aspect-square w-7">
              {#if loadingCalendarData}
                <Spinner
                  class="relative top-0 w-full bg-transparent"
                  show={true}
                />
              {/if}
            </div>
          </div>
        </div>
      </div>
      <div class="flex h-full flex-col items-center gap-3 xl:flex-row">
        <div class="flex gap-x-4">
          <InputGroup class="bg-white">
            <DropDown
              class="text-sm"
              menuClass="text-sm"
              options={viewOptions}
              bind:value={currentView}
              down={false}
            />
          </InputGroup>
        </div>
        {#if isTeacher($authStore)}
          <a href="/tutors/update-availability">
            <Button class="min-w-[245px]">
              <img src="/watch.svg" alt="" />
              <SubHeading class="text-white md:text-sm"
                >Update your availability
              </SubHeading>
            </Button>
          </a>
        {/if}
      </div>
    </div>
  </header>

  {#if currentView?.toLocaleLowerCase().includes("month")}
    <div
      class="main relative grid min-h-screen min-w-[600px] rounded-md border border-gray-200"
      style="grid-template-columns: repeat({grid}, 1fr); "
    >
      {#if loadingCalendarData}
        <div
          transition:fade
          class="absolute left-0 top-0 z-20 h-full w-full bg-[#F2F4F7]"
        ></div>
      {/if}
      {#each days as day, idx}
        <button
          class="relative flex w-full cursor-pointer flex-col items-center {(idx +
            1) %
            7 !==
          0
            ? 'border-r'
            : ''} {idx + 1 < 38 ? 'border-b' : ''} border-gray-100 {cnt % 2 ===
            1 && (day.isToday ? 'bg-gray-200' : '')} {day?.day
            ? 'bg-gray-50'
            : 'bg-gray-100 text-gray-400'}"
        >
          {#if idx < 7}
            <div
              class="max-h-[40px] gap-1.5 border border-gray-100 text-center text-sm leading-5 text-gray-500"
            >
              {weekDays[idx]} <br />
            </div>
          {/if}
          <div class="text-md mt-2 flex justify-center font-medium">
            {day.dayValue || day.day}
          </div>
          <div
            class="absolute bottom-0 left-0 right-0 top-12 mx-2 mt-2 overflow-y-auto"
          >
            {#each day.events as event}
              <Event
                on:click={() => {
                  getSingleSessionData(event.id);
                }}
                {event}
                currentView={"Month"}
              />
            {/each}
          </div>
        </button>
      {/each}
    </div>
  {:else}
    <div class="min-w-[600px]">
      <WeekCalendar
        {weekDates}
        {getSingleSessionData}
        {currentDay}
        {grid}
        {weekDays}
        {events}
        months={monthNames}
        opeenEventModal={() => {}}
        {hours}
        {minutes}
        {hourClock}
        courses={sessionsData}
      />
    </div>
  {/if}
</div>

<Modal bind:this={sessionModal} class="mx-4 w-full max-w-[400px] pb-2.5">
  <div class="flex items-start justify-between pl-5 pt-4">
    <div class="featured-icon">
      <img src="/featured.svg" alt="" />
    </div>

    <div class="pr-16">
      <IconButton
        on:mouseenter={() => (isHovered = true)}
        on:mouseleave={() => (isHovered = false)}
        class="h-11 w-11 focus-within:ring-4 focus:ring-[#98A2B324]"
        on:click={handleJoinSessionMenu}
      >
        <IconDotsVertical color={isHovered ? "#667085" : "#98A2B3"} size="20" />
      </IconButton>

      <Menu
        bind:this={joinSessionMenu}
        bind:visible={joinSessionMenuVisible}
        class=" absolute right-24 top-16 border"
      >
        <button on:click={() => rescheduleModal.show()} class="menu-btn">
          Reschedule
        </button>

        <button on:click={() => cancelModal.show()} class="menu-btn">
          Cancel lessons
        </button>
      </Menu>
    </div>
  </div>

  <ModalBody class="mt-1 max-h-[80vh] space-y-5">
    <div class="space-y-1">
      <Badge
        class="mb-1.5 flex max-w-max items-center gap-1.5 rounded-lg border px-1.5 py-[2px] text-xs font-medium text-gray-700"
      >
        <div class="h-1.5 w-1.5 rounded-full bg-gray-500"></div>
        Order: {modalData.id}
      </Badge>

      <Title class="text-lg md:text-lg">{modalData.title}</Title>
      <Paragraph class="text-gray-600">
        {handleDateTimeFormat(modalData.time)}
      </Paragraph>
    </div>

    <div class="flex items-center gap-4">
      <img src="/video.svg" alt="" />
      <Button
        class="max-w-[133px]"
        variant="primary"
        onClick={() => getAndLaunchMeetingUrl()}
        text="Join session"
      />
    </div>

    <div class="flex items-start gap-4">
      <img src="/user.svg" alt="" />

      <div class="flex flex-col gap-3">
        <Title class="text-sm font-medium text-gray-700 md:text-sm">
          Participants:
        </Title>
        <div class="max-h-[100px]">
          {#each modalData.hosts as item}
            <div class="mb-3 flex items-center gap-3">
              <div class="min-h-10 min-w-10 rounded-full bg-gray-100"></div>
              <div class="flex flex-col truncate">
                <Title class=" text-sm text-gray-700 md:text-sm">
                  {item.host.first_name + " " + item.host.last_name}
                </Title>
                <Paragraph class="text-sm font-normal text-gray-600 md:text-sm">
                  {item.host.email}
                </Paragraph>
              </div>
            </div>
          {/each}
        </div>
      </div>
    </div>

    <div class="flex items-center gap-4">
      <img src="/noti.svg" alt="" />
      <Title class="text-sm font-medium text-gray-700 md:text-sm">
        30 minutes before
      </Title>
    </div>
  </ModalBody>
</Modal>

<BookModal
  data={bookModalResult}
  isReSchedule={true}
  selectedService={{
    tutor_id: 2,
    id: modalData.service_id,
    session_id: modalData.id,
    order_id: modalData.order_id,
  }}
  bind:bookModal={rescheduleModal}
/>

<style>
  .featured-icon {
    @apply border-brand-50 bg-brand-100 flex h-14 w-14 items-center justify-center rounded-full border-8;
  }

  .menu-btn {
    @apply flex w-full cursor-pointer items-center gap-2 px-4 py-3 text-[16px] font-medium text-gray-900 hover:bg-slate-100;
  }
</style>
