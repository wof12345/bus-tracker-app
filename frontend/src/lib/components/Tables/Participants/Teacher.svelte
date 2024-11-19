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
		<div class="flex w-full items-center gap-x-3">
			<img class="h-8 w-8 rounded-full bg-gray-200" src={user.image} alt="" />
			<div class="w-full">
				<p class="text-sm font-medium">{user.firstName} {user.lastName}</p>
			</div>
		</div>
	</div>
{/each}
<div class="border-y">
	<Pagination {totalItems} {pageSize} onPageChange={(page) => {}} />
</div>
