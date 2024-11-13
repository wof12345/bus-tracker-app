<script>
	import { twMerge } from 'tailwind-merge';
</script>

<div class={twMerge('z-10 flex justify-between border-t border-gray-200 px-6 py-4', $$props.class)}>
	<slot />
</div>
