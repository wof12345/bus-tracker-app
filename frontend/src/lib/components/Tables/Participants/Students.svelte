<script lang="ts">
	import Pagination from '$components/Base/Table/Components/Pagination.svelte';

	export let data: any;
	let pageSize = 5;
	$: totalItems = data.users.total;
</script>

{#each data.users.users as user}
	<div
		class={`flex items-center justify-between  border-y px-4 py-3  ${
			user.id % 2 == 0 && 'bg-gray-50'
		} ${user.id % 2 == 0 && 'bg-white'}`}
	>
		<div class="w-full items-center gap-x-3">
			<p class=" font-medium">{user.firstName} {user.lastName}</p>

			<p class="text-sm text-[#475467]">C193024</p>
		</div>
	</div>
{/each}
<div class="border-y">
	<Pagination {totalItems} {pageSize} onPageChange={(page) => {}} />
</div>
