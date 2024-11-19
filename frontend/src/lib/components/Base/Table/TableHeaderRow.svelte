<script lang="ts">
	import { twMerge } from 'tailwind-merge';
</script>

<row
	class={twMerge(
		'grid w-full min-w-max auto-cols-fr bg-gray-50 grid-flow-col items-center rounded-t-lg border-b border-gray-200  px-6 py-3',
		$$props.class
	)}
>
	<slot />
</row>
