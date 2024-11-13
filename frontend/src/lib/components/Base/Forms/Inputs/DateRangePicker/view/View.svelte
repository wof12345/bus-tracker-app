<script>
	import { contextKey } from '../lib/context';
	import { getContext } from 'svelte';
	import DateView from './date-view/DateView.svelte';

	export let viewContextKey;

	const { config, component } = getContext(contextKey);
</script>

<div class="w-full">
	<div class="calendar" class:is-range-picker={config.isRangePicker}>
		<svelte:component this={DateView} {viewContextKey} on:chosen />
	</div>
</div>

<!-- sm:min-w-[310px] md:min-w-[290px] lg:min-w-[220px] xl:min-w-[245px] -->

<style>
	.calendar {
		box-sizing: border-box;
		position: relative;
		user-select: none;
		width: 100%;
		padding-top: 0;

		height: 325px;
	}
</style>
