<script lang="ts">
  import { onDestroy, onMount } from "svelte";

  export let options: ApexChart = {};

  import { v4 as uuidv4 } from "uuid";

  const id = uuidv4();

  let chart;

  let baseOptions = {
    chart: {
      height: "100%",
      type: "area",
      margin: 0,
      toolbar: {
        show: false,
      },
    },

    toolbar: {
      show: false,
    },

    dataLabels: {
      enabled: false,
    },

    ...options,
  };

  onMount(async () => {
    const ApexCharts = (await import("apexcharts")).default;

    chart = new ApexCharts(document.querySelector(`#chart-${id}`), {
      ...baseOptions,
    });
    chart.render();
  });

  onDestroy(() => {
    chart?.destroy();
  });
</script>

<div class="" id="chart-{id}"></div>

<style>
  .apexcharts-toolbar {
    display: hidden;
  }
</style>
