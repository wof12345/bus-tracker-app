<script lang="ts">
  import { onDestroy, onMount } from "svelte";

  export let options: ApexChart = {};

  import { v4 as uuidv4 } from "uuid";

  const id = uuidv4();

  let chart;

  let baseOptions = {
    chart: {
      height: "100%",
      width: "100%",
      type: "bar",
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
    stroke: {
      curve: "smooth",
    },
    colors: ["#008FFB"], // Solid color for bars
    plotOptions: {
      bar: {
        distributed: true, // If you want each bar to have a unique color, you can remove this line if not needed
        horizontal: false, // Set to true if you want a horizontal bar chart
      },
    },
    ...options,
  };

  onMount(async () => {
    const ApexCharts = (await import("apexcharts")).default;

    var chart = new ApexCharts(document.querySelector(`#chart-${id}`), {
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
