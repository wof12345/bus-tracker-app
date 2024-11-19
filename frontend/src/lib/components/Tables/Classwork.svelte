<script lang="ts">
	import Pagination from '$components/Base/Table/Components/Pagination.svelte';

	export let data: any;
	let pageSize = 5;
	$: totalItems = data.users.total;
</script>

<div class="drop fixed mt-[20px] w-[980px] rounded-lg border-[1px] border-gray-200">
	{#each data.users.users as user}
		<div
			class={` border-y px-6 py-4  ${user.id % 2 == 0 && 'bg-gray-50'} ${
				user.id % 2 == 0 && 'bg-white'
			}`}
		>
			<p class="w-full pl-7 text-sm text-[#475467]">{user.company.department}</p>
		</div>
	{/each}

	<Pagination {totalItems} {pageSize} onPageChange={(page) => {}} />
</div>

<style>
	.drop {
		box-shadow:
			0px 1px 2px 0px rgba(16, 24, 40, 0.06),
			0px 1px 3px 0px rgba(16, 24, 40, 0.1);
	}
</style>
