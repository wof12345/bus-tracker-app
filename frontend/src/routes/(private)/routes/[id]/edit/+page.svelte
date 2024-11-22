<script>
  import { deserialize } from "$app/forms";
  import { showSpinner } from "$lib/store/spinner.js";
  import { onMount } from "svelte";
  import polyline from "@mapbox/polyline";
  import InputGroup from "$components/Base/Forms/Components/InputGroup.svelte";
  import SearchDropdown from "$components/Base/Forms/Inputs/SearchDropdown.svelte";
  import FormFieldLabel from "$components/Base/Forms/Components/FormFieldLabel.svelte";
  import {
    IconArrowLeft,
    IconArrowRight,
    IconTarget,
    IconX,
  } from "@tabler/icons-svelte";
  import IconButton from "$components/Base/Buttons/IconButton.svelte";
  import Button from "$components/Base/Buttons/Button.svelte";
  import { goto, invalidateAll } from "$app/navigation";
  import Input from "$components/Base/Forms/Inputs/Input.svelte";
  import TableHeader from "$components/Tables/Components/TableHeader.svelte";
  import TextArea from "$components/Base/Forms/Inputs/TextArea.svelte";
  import { validateApiResponse } from "$components/utils/validateApiResponse";
  import { validateInput } from "$components/utils/validation/validation.js";
  import { showToaster } from "$lib/store/toaster";

  export let data;

  let map;
  let leaflet;

  let hotspots = [];
  let hotspotsRef = [];

  let selectedHotspots = [];
  let selectedHotspot;

  let mapData = [];

  let totalLine = [];

  let routeForm = {
    name: "",
    description: "",
    coordinates: undefined,
    lines: undefined,
  };

  function populateData() {
    let route = data.route;

    routeForm.name = route.name;
    routeForm.description = route.description;

    route.hotspots.forEach((elm, idx) => {
      onSelect(idx, { value: elm._id }, false);
    });

    totalLine = route.lines;

    let line = L.polyline(totalLine, {
      color: "blue",
      weight: 4,
    }).addTo(map);

    mapData.push(line);
  }

  function convertToORSFormat(leafletCoords) {
    const [lat, lng] = leafletCoords;
    return [lng, lat];
  }

  async function save() {
    let form = new FormData();

    routeForm.lines = totalLine;
    routeForm.coordinates = selectedHotspots.map((elm) => elm.coordinates);

    if (!validateInput(routeForm)) {
      routeForm = routeForm;

      showToaster("Empty required fields");
      return;
    }

    form.append("_id", data.route._id);
    form.append("name", routeForm.name);
    form.append("description", routeForm.description);
    form.append("coordinates", JSON.stringify(routeForm.coordinates));
    form.append("lines", JSON.stringify(routeForm.lines));
    form.append(
      "hotspots",
      JSON.stringify(
        selectedHotspots.map((elm) =>
          data.hotspots.data.find((ref) => ref._id === elm._id),
        ),
      ),
    );

    const response = await fetch(`?/update`, {
      method: "POST",
      body: form,
    });

    const saveData = deserialize(await response.text());

    if (!validateApiResponse(saveData)) {
      return;
    }

    showToaster("Route updated");
    await invalidateAll();

    goto("/routes");
  }

  async function onSelect(idx, option, callDraw = true) {
    let value = option.value;
    let item;

    let index = hotspotsRef.findIndex((hotspot) => hotspot.value == value);

    if (index > -1) {
      item = hotspotsRef[index];

      selectedHotspots.push(item);
      hotspotsRef.splice(index, 1);
    }

    hotspots = hotspots;
    selectedHotspots = selectedHotspots;

    drawOnMap(selectedHotspots, callDraw);
  }

  function addMarker(coordinates) {
    const customOptions = {
      maxWidth: "800",
      className: "custom",
    };

    let marker = leaflet?.marker(coordinates).addTo(map);
    // .bindPopup(popupRef, customOptions);

    mapData.push(marker);
  }

  async function drawOnMap(array, callDraw = true) {
    totalLine = [];
    mapData.forEach((layer) => {
      map.removeLayer(layer);
    });
    mapData = [];

    let it = 0;
    array.forEach((elm, idx) => {
      addMarker(elm.coordinates);
      map.setView(elm.coordinates);

      if (idx > 0 && callDraw)
        getAndSetPath(array[idx - 1].coordinates, elm.coordinates, it);
    });
  }

  async function getORSRoute(start, end) {
    let form = new FormData();

    form.append("start", JSON.stringify(convertToORSFormat(start)));
    form.append("end", JSON.stringify(convertToORSFormat(end)));

    const response = await showSpinner(
      fetch(`/api/map?/getORSRoute`, {
        method: "POST",
        body: form,
      }),
    );

    const data = deserialize(await response.text());

    if (data.data.routes && data.data.routes[0]) {
      let geometry = data.data.routes[0].geometry;

      const routeCoordinates = polyline.decode(geometry);

      return routeCoordinates;
    } else {
      throw new Error("No route found");
    }
  }

  async function getAndSetPath(start, end, it) {
    try {
      totalLine = [];
      const route = await getORSRoute(start, end);

      totalLine.push(...route);

      let line = L.polyline(totalLine, {
        color: "blue",
        weight: 4,
      }).addTo(map);

      mapData.push(line);
      it++;

      console.log(it, start, end, selectedHotspots);
    } catch (error) {
      console.error("Error fetching directions:", error);
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

    hotspots = data.hotspots.data.map(
      (hotspot) =>
        new Object({
          ...hotspot,
          name: hotspot.name + ` (${hotspot.location_name})`,
          value: hotspot._id,
        }),
    );

    hotspotsRef = JSON.parse(JSON.stringify(hotspots));

    populateData();
  });
</script>

<div class="flex flex-row h-full">
  <div id="map"></div>

  <div class="bg-white rounded-md flex flex-col p-4 gap-4">
    <div class="flex justify-between gap-3">
      <Button
        class="w-max"
        onClick={() => {
          goto("/routes");
        }}><IconArrowLeft size={18} /> Back</Button
      >
      <Button
        class="w-max"
        onClick={() => {
          goto("/hotspots");
        }}><IconTarget size={18} /> Create a new hotspot</Button
      >
    </div>
    <TableHeader title="Edit route" subtitle="Edit existing route " />

    <InputGroup flow="col">
      <FormFieldLabel>Select hotspots to form a route</FormFieldLabel>
      <SearchDropdown
        options={hotspotsRef}
        bind:value={selectedHotspot}
        {onSelect}
      />
    </InputGroup>

    <div
      class="h-max bg-gray-50 min-w-[400px] max-w-[500px] flex flex-wrap gap-2 items-center"
    >
      {#each selectedHotspots as hotspot, idx}
        <button
          on:click={() => {
            map.setView(hotspot.coordinates);
          }}
          class="border border-gray-400 rounded-lg p-2 h-[80px] max-w-[150px] overflow-hidden flex justify-between gap-2"
        >
          <p class="text-ellipsis w-[100px] overflow-hidden text-xs">
            {hotspot.name}
          </p>

          <IconButton
            class="aspect-auto"
            on:click={() => {
              let index = selectedHotspots.findIndex(
                (item) => hotspot.value == item.value,
              );

              let item;

              if (index > -1) {
                item = selectedHotspots[index];

                hotspotsRef.push(item);
                selectedHotspots.splice(index, 1);
              }

              selectedHotspots = selectedHotspots;
              hotspotsRef = hotspotsRef;

              drawOnMap(selectedHotspots);
            }}
          >
            <IconX size={16} />
          </IconButton>
        </button>

        {#if selectedHotspots[idx + 1]}
          <IconArrowRight size={16} />
        {/if}
      {/each}
    </div>

    <InputGroup flow="col">
      <FormFieldLabel>Name*</FormFieldLabel>
      <Input placeholder="Route name" bind:value={routeForm.name} />
    </InputGroup>

    <InputGroup flow="col">
      <FormFieldLabel>Description*</FormFieldLabel>
      <TextArea
        placeholder="Route description"
        bind:value={routeForm.description}
      />
    </InputGroup>

    <div class="flex justify-between gap-3">
      <Button
        onClick={() => {
          save();
        }}>Save</Button
      >
      <Button
        onClick={() => {
          selectedHotspots = [];

          hotspotsRef = JSON.parse(JSON.stringify(hotspots));
        }}>Reset</Button
      >
    </div>
  </div>
</div>

<style>
  #map {
    width: 100%;
    height: 100vh;
  }
</style>
