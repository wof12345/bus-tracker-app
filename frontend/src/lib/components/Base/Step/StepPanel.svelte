<script>
	import { fade } from 'svelte/transition';
	import { twMerge } from 'tailwind-merge';
</script>

<div
	transition:fade
	class={twMerge(`step-panel step-panel-active step-panel-inactive w-full`, $$props.class)}
>
	<slot />
</div>
