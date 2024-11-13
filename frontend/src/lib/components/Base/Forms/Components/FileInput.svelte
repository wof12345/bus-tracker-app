<script lang="ts">
	import { IconCloudUpload } from '@tabler/icons-svelte';

	export let handleInput: any;
	export let name: any;
	export let file: any;
	export let accept = '';
	export let required: boolean;

	let ref: any;

	function reset(file: any) {
		if (!ref) return;

		if (!file) ref.value = '';
	}

	$: reset(file);
</script>

<IconCloudUpload class="h-12 w-12 rounded-[28px] border-[6px] border-[#F9FAFB] bg-[#F2F4F7] p-2 text-gray-500" />

<slot />

<input
	bind:this={ref}
	type="file"
	{name}
	{required}
	{accept}
	on:change={handleInput}
	class="absolute left-0 top-0 h-full w-full opacity-0 hover:cursor-pointer"
/>
