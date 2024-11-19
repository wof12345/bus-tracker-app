<script lang="ts">
	import { twMerge } from 'tailwind-merge';
</script>

<row class={twMerge('flex w-full border-t px-6 py-4', $$props.class)}>
	<slot />
</row>
