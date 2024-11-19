<script>
	export let data = '';
</script>

<div>
	{new Date(Date.parse(data || '')).toDateString()}
</div>
