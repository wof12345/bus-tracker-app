<script>
	import { twMerge } from 'tailwind-merge';
</script>

<div class={twMerge('', $$props.class)}>
	<slot />
</div>
