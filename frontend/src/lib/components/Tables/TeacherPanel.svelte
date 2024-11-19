<script lang="ts">
	// export let data: any;
</script>

<div class="w-full rounded-lg border-[2px] border-y border-gray-200">
	<div class="flex items-center justify-center">
		<button
			class="w-full rounded-lg bg-[#1553be] px-4 py-2 font-semibold text-white hover:bg-[#104094]"
			>+ Add Course</button
		>
	</div>

	<!-- {#each data.users.users || [] as user}
		<div
			class={`flex  items-center justify-between  rounded-b-lg px-6 py-4  ${
				user.id % 2 == 0 && 'bg-gray-200'
			} ${user.id % 2 == 0 && 'bg-blue-50'}`}
		>
			<a class="w-full cursor-pointer text-center text-[#475467]" href={`/course/${user.id}`}
				>{user.company.department}
			</a>
		</div>
	{/each} -->
</div>
