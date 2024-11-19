<script lang="ts">
	import Paragraph from '$components/Base/Typography/Paragraph.svelte';

	export let onClick = () => {};
</script>

<button
	on:click={onClick}
	class="flex max-h-full items-center gap-1 rounded-lg border-[1px] border-gray-300 bg-white px-3.5 py-2.5 shadow-xs"
>
	<img class="" src="/filter-lines.png" alt="/" />
	<Paragraph class="font-semibold text-[#344054] md:text-sm">Filters</Paragraph>
</button>

<slot />
