<script>
  import { onMount } from "svelte";

  export let data;

  let leaflet;
  let map;

  onMount(async () => {
    leaflet = (await import("leaflet")).default;

    map = leaflet
      .map("map")
      .setView([22.314507734511825, 91.80171405220673], 13);

    leaflet
      .tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      })
      .addTo(map);

    map.on("click", async function (event) {
      const { lat, lng } = event.latlng;
    });

    const socket = new WebSocket("ws://localhost:8001/websocket/ws");
    socket.onmessage = (event) => {
      const { latitude, longitude } = JSON.parse(event.data);
      gpsCoordinates.set({ latitude, longitude });

      map.setView([latitude, longitude], 13);
      marker.setLatLng([latitude, longitude]);
    };
  });
</script>

<div class="flex flex-row h-full">
  <div id="map"></div>

  <div class="bg-white rounded-md flex flex-col p-4 gap-4"></div>
</div>

<style>
  #map {
    width: 100%;
    height: 100vh;
  }
</style>
