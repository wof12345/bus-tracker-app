<script lang="ts">
	import Pagination from './Components/Pagination.svelte';

	export let data: any;

	let pageSize = 5;
	$: totalItems = data.users.total;
</script>

<div class="rounded-lg border-[1px]">
	<div class="flex items-center justify-between rounded-t-lg bg-white px-6 py-3">
		<p class="w-full"></p>
		<p class="w-full px-10 text-center font-medium text-[#475467]">6/1/2023</p>
		<p class="w-full px-10 text-center font-medium text-[#475467]">5/1/2023</p>
	</div>
	<div class=" flex items-center justify-between rounded-t-lg bg-white px-6 py-3">
		<p class="w-full"></p>
		<p class="w-full px-10 text-center font-medium text-[#475467]">English</p>
		<p class="w-full px-10 text-center font-medium text-[#475467]">Bangla</p>
	</div>

	{#each data.users.users as user}
		<div class="flex items-center justify-between border-y p-4 px-6 odd:bg-gray-50 even:bg-white">
			<div class="w-full">
				<p class="font-medium">{user.firstName} {user.lastName}</p>
				<p class="text-sm text-[#475467]">C193024</p>
			</div>

			<p class="w-full pl-[145px] text-[#475467]">{user.weight}%</p>
			<p class="w-full pr-10 text-center text-[#475467]">{user.weight}%</p>
		</div>
	{/each}

	<Pagination {totalItems} {pageSize} onPageChange={(page) => {}} />
</div>
