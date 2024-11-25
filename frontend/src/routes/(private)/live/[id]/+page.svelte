<script>
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import Button from "$components/Base/Buttons/Button.svelte";
  import TableHeader from "$components/Tables/Components/TableHeader.svelte";
  import { showToaster } from "$lib/store/toaster.ts";
  import { IconArrowLeft } from "@tabler/icons-svelte";
  import { onDestroy, onMount } from "svelte";

  export let data;

  let leaflet;
  let map;

  let busId = $page.params.id;

  let bus = {};

  let markers = {};
  let lines = {};
  let selected = {
    route: undefined,
    vehicle: undefined,
  };

  let popupRef;

  let socket;

  function addMarkerMap(vehicle) {
    let coordinates = vehicle.coordinates;
    let id = vehicle._id;

    const customOptions = {
      maxWidth: "800",
      className: "custom",
    };

    try {
      // map.setView(coordinates);

      if (markers[id]) {
        markers[id].setLatLng(coordinates);
      } else {
        markers[id] = L.circleMarker([51.5, -0.09], {
          color: "blue",
          fillColor: "blue",
          fillOpacity: 1,
          radius: 10,
        })
          .addTo(map)
          .bindPopup(popupRef, customOptions);
      }

      markers[id].on("click", function (e) {
        selected.vehicle = vehicle;
        selected = selected;
      });
    } catch (error) {
      console.log(error);
    }
  }

  function drawVehicle(vehicle) {
    addMarkerMap(vehicle);
  }

  function drawRoutes(vehicle) {
    let routes = vehicle.route.coordinates_visual;
    let id = vehicle._id;

    const customOptions = {
      maxWidth: "800",
      className: "custom",
    };

    if (!lines[id]) {
      for (let route of routes) {
        let line = L.polyline(route, {
          color: "blue",
          weight: 4,
        })
          .addTo(map)
          .bindPopup(popupRef, customOptions);

        line.on("click", function (e) {
          selected.vehicle = vehicle;
          selected = selected;
        });

        lines[id] ??= [];
        lines[id].push(line);
      }
    }
  }

  function drawOnMap(vehicles = []) {
    for (let vehicle of vehicles) {
      drawVehicle(vehicle);
      drawRoutes(vehicle);
    }
  }

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

    socket = new WebSocket("ws://localhost:8001/websocket/ws");

    socket.onopen = () => {
      console.log("WebSocket connection established");
      if (busId) socket.send(JSON.stringify({ _id: busId }));
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if ("_id" in data && data["coordinates"]) {
        bus = data;
        drawOnMap([bus]);
      }
    };

    socket.onclose = function (event) {
      showToaster("Connection lost to stream");
      console.log("Socket closed:", event.code, event.reason);
    };
  });

  onDestroy(() => {
    socket?.close(1000, "Client disconnected");
  });
</script>

<div class="flex flex-row h-full">
  <div id="map"></div>

  <div class="bg-white rounded-md flex flex-col p-4 gap-4 max-w-[400px]">
    <Button
      class="w-max"
      onClick={() => {
        history.back();
      }}><IconArrowLeft size={18} /> Back</Button
    >
    <TableHeader
      subtitle={"Live location view"}
      title={`Live location for bus ${bus?.name || busId}`}
    ></TableHeader>

    <p class="text-xs">
      <span class="text-sm font-bold">Disclaimer:</span> <br />
      This is a proof of concept and a simulation for the time being on how we could
      use GPS technology to track bus in realtime and reveal them to everyone using
      the platform. <br /> The technical idea of it is the same as when using GPS
      as the we would need to send data from GPS to our backend. However the method
      of sending can differ based on the model of the tracking device.
    </p>

    <p class="text-xs">
      <span class="text-sm font-bold">Planned (possible feature):</span> <br />
      The same code can be used to create a tracking interface with all the vehicles
      for the managers.
    </p>
  </div>
</div>

<div class="hidden">
  <div bind:this={popupRef}>
    <div class="flex flex-col gap-2">
      <p style="margin: 0;">
        <span class="font-semibold text-sm"> Bus name:</span>
        {selected.vehicle?.name || "Unnamed"}
      </p>
      <p style="margin: 0;">
        <span class="font-semibold text-sm"> Route name:</span>
        {selected.vehicle?.route.name || "Unnamed"}
      </p>
      <p style="margin: 0;">
        <span class="font-semibold text-sm"> Reserved for:</span>
        {selected.vehicle?.reservation?.name || ""}
      </p>
      <p style="margin: 0;">
        <span class="font-semibold text-sm"> Current bus coordinates:</span>
        {selected.vehicle?.coordinates || ""}
      </p>
    </div>
  </div>
</div>

<style>
  #map {
    width: 100%;
    height: 100vh;
  }
</style>
