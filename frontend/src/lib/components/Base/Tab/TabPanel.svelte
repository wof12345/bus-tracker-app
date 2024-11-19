<script>
	import { fade } from 'svelte/transition';
	import { twMerge } from 'tailwind-merge';
</script>

<div transition:fade class={twMerge(`tab-panel hidden`, $$props.class)}>
	<slot />
</div>
