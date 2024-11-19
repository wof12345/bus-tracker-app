<script>
	import { fade } from 'svelte/transition';
</script>

<div
	transition:fade={{ duration: 300 }}
	class="w-full text-ellipsis rounded-lg text-xs text-red-500 md:text-xs"
>
	<slot />
</div>
