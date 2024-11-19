<script>
	import { page } from '$app/stores';
	import Text from '$components/Base/Typography/Text.svelte';

	$: pathName = $page.route.id;

	export let navItems = [];
</script>

<div class="grid grid-cols-9">
	<div class="col-span-2 flex w-full flex-col gap-1 py-8 text-start font-semibold">
		{#each navItems as item}
			<Text
				class="hover:border-primary-600 hover:text-primary-600 block w-full border-l-[2px] px-3 py-2 text-sm transition delay-75 {pathName.includes(
					item.href
				)
					? 'border-primary-600 text-primary-600'
					: 'border-[#fff0]'}"
			>
				<a class="block h-full w-full" href={item.href}>{item.name}</a>
			</Text>
		{/each}
	</div>

	<div class="col-span-7">
		<slot />
	</div>
</div>
