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
  import { authStore, isAdmin, isManager } from "$lib/store/auth";
  import Title from "$components/Base/Typography/Title.svelte";
  import { digitizeNumber } from "$components/utils/textMethods.js";

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
  let totalLineVisual = [];

  let marker;

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
    totalLineVisual = route.coordinates_visual;

    totalLineVisual.forEach((elm, idx) => {
      let line;

      if (idx === -1)
        line = L.polyline(elm, {
          color: "red",
          weight: 4,
        })
          .addTo(map)
          .bindPopup("Starting route");
      else
        line = L.polyline(elm, {
          color: "blue",
          weight: 4,
        }).addTo(map);

      mapData.push(line);
    });
  }

  function convertToORSFormat(leafletCoords) {
    const [lat, lng] = leafletCoords;
    return [lng, lat];
  }

  function formatTime(time) {
    if (!time) return;

    let str = time.split(":");

    let timeStr = str[0] + ":" + digitizeNumber(str[1]) + " " + str[2];

    return timeStr;
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
    form.append("coordinates_visual", JSON.stringify(totalLineVisual));
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

  function addMarker(coordinates, idx) {
    var redMarker = leaflet?.icon({
      iconUrl: "/red-marker.png",
      shadowUrl: "",

      iconSize: [40, 40],
      shadowSize: [50, 64],
      iconAnchor: [18, 45],
      shadowAnchor: [4, 62],
      popupAnchor: [3, -30],
    });

    let marker;

    if (idx === 0) {
      marker = leaflet
        ?.marker(coordinates, { icon: redMarker })
        .addTo(map)
        .bindPopup("Starting point");
    } else marker = leaflet?.marker(coordinates).addTo(map);

    mapData.push(marker);
  }

  async function drawOnMap(array, callDraw = true) {
    totalLine = [];
    totalLineVisual = [];

    mapData.forEach((layer) => {
      map.removeLayer(layer);
    });
    mapData = [];

    let promisesToResolve = [];

    array.forEach((elm, idx) => {
      addMarker(elm.coordinates, idx);
      map.setView(elm.coordinates);

      mapLines.forEach((layer) => {
        map.removeLayer(layer);
      });
      mapLines = [];

      if (idx > 0 && callDraw) {
        promisesToResolve.push(
          getAndSetPath(array[idx - 1].coordinates, elm.coordinates),
        );
      }
    });

    await Promise.all(promisesToResolve);
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

  async function getAndSetPath(start, end) {
    try {
      const route = await getORSRoute(start, end);

      // const uniqueCoordinates = new Set(
      //   totalLine.map((coord) => coord.join(",")),
      // );

      // route.forEach((coord) => {
      //   const coordStr = coord.join(",");
      //   if (!uniqueCoordinates.has(coordStr)) {
      //     uniqueCoordinates.add(coordStr);
      //     totalLine.push(coord);
      //   }
      // });
      totalLine.push(...route);

      let line = L.polyline(route, {
        color: "blue",
        weight: 4,
      }).addTo(map);

      totalLineVisual.push(route);
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

    populateData();
  });
</script>

<div class="flex flex-col md:flex-row h-max">
  <div class="w-full h-[200px] relative">
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
    class="bg-white rounded-md flex flex-col p-4 w-full lg:max-w-[400px] gap-4 relative z-1 h-screen overflow-y-auto"
  >
    <div class="flex justify-between gap-3">
      <Button
        class="w-max"
        onClick={() => {
          history.back();
        }}><IconArrowLeft size={18} /> Back</Button
      >
      {#if isAdmin($authStore) || isManager($authStore)}
        <Button
          class="w-max"
          onClick={() => {
            goto("/hotspots");
          }}><IconTarget size={18} /> Create a new hotspot</Button
        >
      {/if}
    </div>
    {#if isAdmin($authStore) || isManager($authStore)}
      <TableHeader title="Edit route" subtitle="Edit existing route " />
    {:else}
      <TableHeader title="Route" subtitle="Current path for this route " />
    {/if}

    {#if isAdmin($authStore) || isManager($authStore)}
      <InputGroup flow="col">
        <FormFieldLabel>Select hotspots to form a route</FormFieldLabel>
        <SearchDropdown
          options={hotspotsRef}
          bind:value={selectedHotspot}
          {onSelect}
        />
      </InputGroup>
    {/if}

    <div class="h-max bg-gray-50 flex flex-wrap gap-2 items-center">
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

          {#if isAdmin($authStore) || isManager($authStore)}
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
          {/if}
        </button>

        {#if selectedHotspots[idx + 1]}
          <IconArrowRight size={16} />
        {/if}
      {/each}
    </div>

    <div class="flex flex-col gap-2">
      <Title class="text-md md:text-md">Buses assigned to this route</Title>

      {#each data?.buses?.data || [] as bus}
        <button
          on:click={() => {
            goto(`/buses?selected=${bus._id}`);
          }}
          class="hover:cursor-pointer hover:bg-gray-100 p-2 w-full rounded-sm text-sm text-start flex justify-between flex-wrap"
        >
          <p>{bus.name}</p>

          <p>{formatTime(bus.time)}</p>
        </button>
      {/each}
    </div>

    {#if isAdmin($authStore) || isManager($authStore)}
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
    {/if}
  </div>
</div>

<style>
  #map {
    width: 100%;
    height: 100vh;
  }
</style>
