<script lang="ts">
	import { twMerge } from 'tailwind-merge';
</script>

<div
	class={twMerge(
		'w-full max-w-[140px] overflow-hidden text-ellipsis px-2 text-xs font-medium leading-[18px] text-gray-600',
		$$props.class
	)}
>
	<slot />
</div>
