<script lang="ts">
	import Badge from '$components/Base/Badge.svelte';
	import Paragraph from '$components/Base/Typography/Paragraph.svelte';

	export let text: any;
</script>

<Badge class={$$props.class}>
	<Paragraph class="rounded-2xl bg-[#EFF8FF] px-2 py-0.5 font-medium text-[#175CD3] md:text-xs"
		>{text}</Paragraph
	>
</Badge>
