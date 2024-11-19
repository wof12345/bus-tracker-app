<script lang="ts">
	export let number: number = 0;

	function currency(number: number) {
		return new Intl.NumberFormat('en-GB', { style: 'currency', currency: 'GBP' }).format(number);
	}
</script>

<div>{currency(number)}</div>
