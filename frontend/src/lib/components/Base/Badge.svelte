<script>
	import { twMerge } from 'tailwind-merge';
</script>

<div class={twMerge('shadow-xs rounded-2xl px-2  md:text-xs', $$props.class)}>
	<slot />
</div>
