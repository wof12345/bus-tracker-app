<script>
  import { deserialize } from "$app/forms";
  import { onMount } from "svelte";

  let leaflet;
  let map;
  let marker;
  let coordinates = { lat: null, lng: null };
  let placeName = "Click on the map to get the area name";

  let selectedLocationData;

  async function getAreaName(lat, lng) {
    let form = new FormData();

    form.append("lat", lat);
    form.append("lng", lng);

    const response = await fetch(`/api/map?/reverseGeoCode`, {
      method: "POST",
      body: form,
    });

    const data = deserialize(await response.text());

    if (data.data && data.data.results)
      selectedLocationData = data.data.results[0];

    console.log(selectedLocationData, data);

    if (selectedLocationData) {
      placeName = selectedLocationData?.formatted || "Area name not available";
    } else {
      placeName = "Area name not found";
    }
  }

  onMount(async () => {
    leaflet = (await import("leaflet")).default;

    map = leaflet.map("map").setView([51.505, -0.09], 13);

    leaflet
      .tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      })
      .addTo(map);

    map.on("click", async function (event) {
      const { lat, lng } = event.latlng;
      coordinates = { lat, lng };

      await getAreaName(lat, lng);

      if (marker) {
        marker.setLatLng([lat, lng]);
      } else {
        marker = leaflet.marker([lat, lng]).addTo(map);
      }
    });
  });
</script>

<div id="map"></div>

<div class="info-container">
  <p>
    Selected Coordinates: <br />
    Latitude: {coordinates.lat} <br />
    Longitude: {coordinates.lng}
  </p>
  <p>
    Area Name: {placeName}
  </p>
</div>

<style>
  #map {
    height: 400px;
    width: 100%;
  }
  .info-container {
    margin-top: 20px;
  }
</style>
