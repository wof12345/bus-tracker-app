<script lang="ts">
	import { twMerge } from 'tailwind-merge';
</script>

<div class={twMerge('sc-bg-t sc-thumb sc-track sc-w overflow-auto', $$props.class)}>
	<slot />
</div>
