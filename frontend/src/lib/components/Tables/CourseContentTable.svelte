<script lang="ts">
	export let data: any;
</script>

<div class="">
	{#each data.users.users as user}
		<div
			class={`flex items-center  border-y  px-6 py-4  ${user.id % 2 == 0 && 'bg-gray-50'} ${
				user.id % 2 == 0 && 'bg-white'
			}`}
		>
			<div class="flex gap-10">
				<div>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="1.5"
						stroke="currentColor"
						class="h-6 w-6"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
						/>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M15.91 11.672a.375.375 0 0 1 0 .656l-5.603 3.113a.375.375 0 0 1-.557-.328V8.887c0-.286.307-.466.557-.327l5.603 3.112Z"
						/>
					</svg>
				</div>

				<div>
					<span class="font-bold">Physics1:</span>
					<a href="/">{user.company.department}</a>
				</div>
			</div>
		</div>
	{/each}
</div>
