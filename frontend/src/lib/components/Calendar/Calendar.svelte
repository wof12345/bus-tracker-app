<!-- TODO: It will be needed-->

<!-- <script>

	import DropDown from '$components/Base/Forms/Inputs/DropDown.svelte';
	import Input from '$components/Base/Forms/Inputs/Input.svelte';

	import SubHeading from '$components/Base/Typography/SubHeading.svelte';
	import { onMount } from 'svelte';
	import Button from '$components/Base/Buttons/Button.svelte';
	import { IconChevronLeft, IconChevronRight, IconPlus, IconSearch } from '@tabler/icons-svelte';
	import WeekCalendar from './WeekCalendar.svelte';
	import IconButton from '$components/Base/Buttons/IconButton.svelte';
	import Header from '$components/Base/Typography/Header.svelte';
	import Modal from '$components/Base/Modal/Modal.svelte';
	import ModalHeader from '$components/Base/Modal/ModalHeader.svelte';
	import ModalBody from '$components/Base/Modal/ModalBody.svelte';
	import ModalFooter from '$components/Base/Modal/ModalFooter.svelte';

	import SearchDropdown from '$components/Base/Forms/Inputs/SearchDropdown.svelte';
	import DateInput from '$components/Base/Forms/Inputs/DateInput.svelte';
	import { digitizeNumber } from '$components/utils/textMethods';
  import InputGroup from '$components/Base/Forms/Components/InputGroup.svelte';
  import InputIcon from '$components/Base/Forms/Components/InputIcon.svelte';
  import FormFieldLabel from '$components/Base/Forms/Components/FormFieldLabel.svelte';
  import Event from './Event.svelte';
  import { applyAction, deserialize } from '$app/forms';
  import { invalidateAll } from '$app/navigation';

	let today = new Date();

	let currentMonth = today.getMonth();
	let currentYear = today.getFullYear();


	let days = [];
	let events = [];

	let selectedDate = today.getDate();
	let selectedYear = currentYear;
	let selectedMonth = currentMonth;
	let selectedHour = 12;
	let selectedMinute = 0;
	let selectedHourClock = 'AM';

	let dateView = '';
	let eventDescription = '';

	let grid = 7;

	export let courses;

	$:console.log(courses?.courses?.data);


	const monthNames = [
		'January',
		'February',
		'March',
		'April',
		'May',
		'June',
		'July',
		'August',
		'September',
		'October',
		'November',
		'December'
	];

	const weekDays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

	const hours = ['12', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'];

	const minutes = [];

	const hourClock = ['AM', 'PM'];

	let addEventModal;

	const viewOptions = ['Month View', 'Week View'];
	let currentView = viewOptions[0];

	function dateInput(value) {
		const timeCollection = value.split('-');
		selectedYear = +timeCollection[0];
		selectedMonth = +timeCollection[1];
		selectedDate = +timeCollection[2];
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

	function dateObj(stamp) {
		return new Date(stamp);
	}

	function getFirstDayOfMonth(month, year) {
		return new Date(year, month, 1).getDay();
	}

	function generateCalendar(month, year) {
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
			days.push({ day: '', dayValue: prevMonthDays[prevIterator], events: [] });
		}

		for (let day of numOfDays) {
			const dayEvents = events
				.filter(
					(event) =>
						dateObj(event.date).getDate() === day &&
						dateObj(event.date).getMonth() === month &&
						dateObj(event.date).getFullYear() === year
				)
				.map((e) => e.description);

			days.push({ day, events: dayEvents });
		}

		let remaining = totalGrid - (numOfDays.length - 1 + firstDay);

		for (let i = 0; i < remaining - 1; i++) {
			days.push({ day: '', dayValue: nextMonthDays[i], events: [] });
		}
	}

	function addEvent(year, month, day, description) {
		const currentTimeStamp = new Date(year, month, day, selectedHour, selectedMinute).getTime();
		console.log(
			selectedDate,
			selectedMonth,
			selectedYear,
			selectedHour,
			selectedMinute,
			selectedHourClock,
			currentTimeStamp
		);

		events.push({ date: currentTimeStamp, description: description.trim() });

		generateCalendar(currentMonth, currentYear);
	}

	function openEventModal(year, month, day, hour, minute, hourClock) {
		addEventModal.show();

		selectedDate = day || selectedDate;
		selectedMonth = month || selectedMonth;
		selectedYear = year || selectedYear;
		selectedHour = hour || selectedHour;
		selectedMinute = minute || selectedMinute;
		selectedHourClock = hourClock || selectedHourClock;

		dateView = `${selectedYear}-${digitizeNumber(selectedMonth + 1)}-${digitizeNumber(
			selectedDate
		)}`;

		console.log(dateView);
	}

	function nextMonth() {
		if (currentMonth === 11) {
			currentMonth = 0;
			currentYear += 1;
		} else {
			currentMonth += 1;
		}
		generateCalendar(currentMonth, currentYear);
	}

	function prevMonth() {
		if (currentMonth === 0) {
			currentMonth = 11;
			currentYear -= 1;
		} else {
			currentMonth -= 1;
		}
		generateCalendar(currentMonth, currentYear);
	}

	onMount(() => {
		for (let i = 1; i <= 60; i++) {
			minutes.push(i < 10 ? '0' + i : i + '');
		}

		generateCalendar(currentMonth, currentYear);
	});

	let course="";
	let value="";


let courseArray=[] ;

onMount(() => {
  if (!courses) return;

  courseArray = courses?.courses?.data.map(
	(elm) =>
	  new Object({
		name: elm.title,
		value: elm.id,
	  }),
  );

});



async function create(e) {
    const data = new FormData(e.currentTarget);
    console.log(data);
  data.append("course",course);
  data.append("value",value);




    const response = await fetch("?/create", {
      method: "POST",
      body: data,
    });


    console.log(response);

    const result = deserialize(await response.text());

    console.log(result);

    if (result.type === "success") {
  console.log("paichi");
      await invalidateAll();
 
    }

    applyAction(result);
  }

</script>

<div class="flex min-h-screen flex-col gap-4 overflow-auto">
	<header class="top flex h-max flex-col gap-5">
		<Header class="text-3xl font-semibold leading-[38px] md:text-3xl">Calendar</Header>

		<div
			class=" flex h-full w-full flex-col items-center justify-between gap-4 xl:flex-row xl:gap-16"
		>
			<div class="flex h-full w-full max-w-[400px] flex-col items-center gap-3 xl:flex-row">
				<div class="flex w-full items-center justify-between gap-4">
					<IconButton onClick={() => prevMonth()}>
						<IconChevronLeft />
					</IconButton>

					<SubHeading class="xl:text-md  text-center text-sm font-semibold text-gray-700 xl:w-40">
						<span>{monthNames[currentMonth]} {currentYear}</span>
					</SubHeading>

					<IconButton onClick={() => nextMonth()}>
						<IconChevronRight />
					</IconButton>
				</div>

				<InputGroup class="w-full bg-white ">
					<Input class="text-sm" label={'Search for events or tasks '}>
						<InputIcon class="ml-1 text-gray-500"><IconSearch size={20} /></InputIcon>
					</Input>
				</InputGroup>
			</div>

			<div class="flex h-full flex-col items-center gap-3 xl:flex-row">
				<div class="flex gap-x-4">
					<InputGroup class="bg-white">
						<Button variant="secondary">Today</Button>
					</InputGroup>

					<InputGroup class="bg-white">
						<DropDown
							class="text-sm"
							menuClass="text-sm"
							options={viewOptions}
							bind:value={currentView}
						/>
					</InputGroup>
				</div>

				<Button onClick={() => addEventModal.show()} class="w-max">
					<IconPlus size={20} />
					<SubHeading class="text-white md:text-sm">Add new event</SubHeading>
				</Button>
			</div>
		</div>
	</header>

	{#if currentView.toLocaleLowerCase().includes('month')}
		<div
			class="main grid min-h-screen rounded-md border border-gray-200"
			style="grid-template-columns: repeat({grid}, 1fr);"
		>
			{#each days as day, idx}
				<button
					class="relative flex cursor-pointer flex-col items-center hover:bg-gray-50 {(idx + 1) %
						7 !==
					0
						? 'border-r'
						: ''} {idx + 1 < 38 ? 'border-b' : ''} border-gray-100 {day?.day !== ''
						? ''
						: 'bg-gray-50 text-gray-400'}"
					style=""
					on:click={() => day.day && openEventModal(currentYear, currentMonth, day.day)}
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
						class="absolute bottom-0 left-0 right-0 top-12 mx-2 mt-2 overflow-y-auto overflow-x-hidden"
					>
						{#each day.events as event}
							<Event {event} />
						{/each}
					</div>
				</button>
			{/each}
		</div>
	{:else}
		<WeekCalendar
			{grid}
			{weekDays}
			{events}
			{days}
			months={monthNames}
			{openEventModal}
			{hours}
			{minutes}
			{hourClock}
		/>
	{/if}
</div>

<form on:submit|preventDefault={create}>
	<Modal bind:this={addEventModal} class="max-w-[360px]">
		<ModalHeader>Add Event</ModalHeader>
	
		<ModalBody>
			<div class="flex flex-col gap-4">
				<div class="flex flex-col gap-4">
					<FormFieldLabel>Time</FormFieldLabel>
	
					<InputGroup>
						<DateInput bind:value={dateView} inputCallback={dateInput} />
					</InputGroup>
	
					<div class="flex gap-2">
						<InputGroup>
							<SearchDropdown bind:value={selectedHour} options={hours} />
						</InputGroup>
	
						<InputGroup>
							<SearchDropdown bind:value={selectedMinute} options={minutes} />
						</InputGroup>
	
						<InputGroup>
							<DropDown bind:value={selectedHourClock} options={hourClock} />
						</InputGroup>
					</div>
				</div>
	
				<InputGroup>
					<SearchDropdown
					name="course"
					options={courseArray}
					placeholder={"Search for subject"}
					bind:value={value}/>
		  
				</InputGroup>
			</div>
		</ModalBody>
	
		<ModalFooter>
			<Button type="submit"
				onClick={() => {
					addEvent(currentYear, currentMonth, selectedDate, eventDescription);
					addEventModal.hide();
				}}>Add Event</Button
			>
		</ModalFooter>
	</Modal>
</form> -->
