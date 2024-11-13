<script lang="ts">
	import { twMerge } from 'tailwind-merge';

	export let src: any = undefined;
</script>

<div class={twMerge('-ml-2 flex aspect-square w-6 items-center justify-center', $$props.class)}>
	{#if src}
		<img {src} alt={src} />
	{/if}

	<slot />
</div>
