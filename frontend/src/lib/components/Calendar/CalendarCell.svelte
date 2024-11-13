<script>
	import Event from './Event.svelte';

	export let openEventModal = () => {};
	export let boundaryBox = 38;

	const idx = $$props.idx;
	const context = $$props.context;


</script>

<button
	class="relative flex cursor-pointer flex-col items-center hover:bg-gray-50 {(idx + 1) %
		$$props.grid !==
	0
		? 'border-r'
		: ''} {idx + 1 < boundaryBox ? 'border-b' : ''} border-gray-100 {context?.day !== ''
		? ''
		: 'bg-gray-50'}"
	style=""
	on:click={() => context.day && openEventModal(context.day)}
>
	{#if idx < 7}
		<div
			class="max-h-[40px] gap-1.5 border border-gray-100 text-center text-sm leading-5 text-gray-500"
		>
			{$$props.weekDays[idx]} <br />
		</div>
	{/if}

	<div class="mt-2 flex justify-center text-md font-medium text-gray-900">
		{context.day}
	</div>

	<div class="absolute bottom-0 left-0 right-0 top-7 mx-2 mt-2 overflow-y-auto overflow-x-hidden">
		{#each context.events as event}
			<Event {event} />
		{/each}
	</div>
</button>
