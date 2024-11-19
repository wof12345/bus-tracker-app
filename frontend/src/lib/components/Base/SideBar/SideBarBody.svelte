<script>
	import { twMerge } from 'tailwind-merge';
</script>

<div class={twMerge('flex h-full flex-col', $$props.class)}>
	<slot />
</div>
