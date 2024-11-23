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
  import Menu from "$components/Base/Menu/Menu.svelte";
  import Option from "$components/Base/Forms/Components/Option.svelte";

  export let data;

  let map;
  let leaflet;

  let hotspots = [];
  let hotspotsRef = [];

  let selectedHotspots = [];
  let selectedHotspot;

  let mapData = [];
  let mapLines = [];

  let totalLine = [];

  let marker;

  let routeForm = {
    name: "",
    description: "",
    coordinates: undefined,
    lines: undefined,
  };

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

    const response = await fetch(`?/create`, {
      method: "POST",
      body: form,
    });

    const saveData = deserialize(await response.text());

    if (!validateApiResponse(saveData)) {
      return;
    }

    showToaster("Route added");
    await invalidateAll();

    goto("/routes");
  }

  async function onSelect(idx, option) {
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

  async function drawOnMap(array) {
    totalLine = [];

    console.log("called");

    mapData.forEach((layer) => {
      map.removeLayer(layer);
    });
    mapData = [];

    let promisesToResolve = [];

    array.forEach((elm, idx) => {
      addMarker(elm.coordinates);
      map.setView(elm.coordinates);

      mapLines.forEach((layer) => {
        map.removeLayer(layer);
      });
      mapLines = [];

      if (idx > 0) {
        promisesToResolve.push(
          getAndSetPath(array[idx - 1].coordinates, elm.coordinates),
        );
      }
    });

    await Promise.all(promisesToResolve);
  }

  $: drawOnMap(selectedHotspots);

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

  async function getAndSetPath(start, end) {
    try {
      const route = await getORSRoute(start, end);

      mapLines.forEach((layer) => {
        map.removeLayer(layer);
      });
      mapLines = [];

      totalLine.push(...route);
      totalLine = totalLine;
      // totalLine.pop();
      console.log(totalLine.length, route.length);

      let line = L.polyline(totalLine, {
        color: "blue",
        weight: 4,
      }).addTo(map);

      mapLines.push(line);
      mapLines = mapLines;
    } catch (error) {
      console.error("Error fetching directions:", error);
    }
  }

  async function getAreaCoords(search) {
    let form = new FormData();

    form.append("search", search);

    const response = await showSpinner(
      fetch(`/api/map?/forwardGeoCode`, {
        method: "POST",
        body: form,
      }),
    );

    const data = deserialize(await response.text());

    searchResults = data.data;
  }

  let search;
  let searchResults = [];
  let searchTimeOut;
  async function searchQuery(search) {
    if (!search || search === "" || searchTimeOut) return;

    searchTimeOut = setTimeout(async () => {
      getAreaCoords(search);
      clearTimeout(searchTimeOut);
      searchTimeOut = undefined;
    }, 900);
  }

  $: searchQuery(search);

  function addMarkerMap(coordiantes) {
    map.setView(coordiantes);

    if (marker) {
      marker.setLatLng(coordiantes);
    } else {
      marker = leaflet.marker(coordiantes).addTo(map);
    }
  }

  async function invokeInformationLocation(lat, lng) {
    let coordinates_array = [lat, lng];

    addMarkerMap(coordinates_array);
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
  });
</script>

<div class="flex flex-row h-full">
  <div class="w-full relative">
    <div
      class="search_anchor absolute top-10 m-auto left-0 right-0 z-[100] max-w-[300px]"
    >
      <Input bind:value={search} placeholder={"Search a location"} />

      <Menu
        class="max-h-[500px]"
        visible={searchResults.length > 0}
        parentWidth={true}
        anchorEelement={"search_anchor"}
      >
        {#each searchResults as search}
          <Option
            onClick={() => {
              invokeInformationLocation(search.lat, search.lon);
              searchResults = [];
            }}>{search.display_name}</Option
          >
        {/each}
      </Menu>
    </div>

    <div id="map" class="relative z-0"></div>
  </div>

  <div
    class="bg-white rounded-md flex flex-col p-4 gap-4 h-screen w-max- max-w-[500px] overflow-auto"
  >
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
    <TableHeader title="Add route" subtitle="Add a new route to the system" />

    <InputGroup flow="col">
      <FormFieldLabel>Select hotspots to form a route</FormFieldLabel>
      <SearchDropdown
        options={hotspotsRef}
        bind:value={selectedHotspot}
        {onSelect}
      />
    </InputGroup>

    <div
      class="h-max bg-gray-50 min-w-[500px] w-max max-w-[500px] flex flex-wrap gap-2 items-center"
    >
      {#each selectedHotspots as hotspot, idx}
        <button
          on:click={() => {
            map.setView(hotspot.coordinates);
          }}
          class="border border-gray-400 rounded-lg p-2 h-max max-w-[150px] overflow-hidden flex justify-between gap-2"
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
