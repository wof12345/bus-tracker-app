<script lang="ts">
	import { twMerge } from 'tailwind-merge';
	export let variant: string = 'default';

	const textVariant: any = {
		xsRegular: 'text-xs leading-[18px] text-gray-600',
		xsMedium: 'text-xs  font-medium leading-[18px]  text-gray-600',
		smRegular: 'text-sm leading-5 text-gray-600',
		smMedium: 'text-sm  font-medium leading-5  text-gray-900',
		smSemibold: 'text-sm  font-semibold leading-5  text-gray-700',
		mdRegular: 'text-md leading-5 text-gray-600',
		mdMedium: 'text-md font-medium leading-5 text-gray-600',
		mdSemibold: 'text-md font-semibold leading-6 text-gray-900',
		lgSemibold: 'text-lg font-semibold text-gray-900 leading-7',
		default: 'text-md leading-6 text-gray-600'
	};

	function getVariant(): string {
		return textVariant[variant] || '';
	}
</script>

<div class={twMerge(` ${getVariant()}`, $$props.class)}>
	<slot />
</div>
