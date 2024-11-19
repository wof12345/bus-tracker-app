<script>
  import { deserialize } from "$app/forms";
  import { onMount } from "svelte";
  import TableBody from "$components/Base/Table/TableBody.svelte";
  import TableRow from "$components/Base/Table/TableRow.svelte";
  import TableCell from "$components/Base/Table/TableCell.svelte";
  import TableFooter from "$components/Base/Table/TableFooter.svelte";
  import TableFrame from "$components/Base/Table/TableFrame.svelte";
  import Pagination from "$components/Base/Table/Components/Pagination.svelte";

  import Section from "$components/Layout/Section.svelte";
  import Table from "$components/Base/Table/Table.svelte";
  import TableHeaderRow from "$components/Base/Table/TableHeaderRow.svelte";
  import TableBodyHeader from "$components/Base/Table/TableBodyHeader.svelte";
  import TableButton from "$components/Base/Table/Components/TableButton.svelte";
  import { IconEdit, IconTrash } from "@tabler/icons-svelte";
  import HotspotPopup from "$components/HotspotPopup.svelte";
  import { showSpinner } from "$lib/store/spinner.ts";

  export let data;

  $: hotspots = data?.hotspots;

  let popupRef;
  let lastPopup;

  let leaflet;
  let map;
  let marker;
  let coordinates = { lat: null, lng: null };
  let placeName = "Click on the map to get the area name";

  let selectedItem;

  let selectedLocationData;

  async function getAreaDetails(lat, lng) {
    selectedItem = undefined;
    let form = new FormData();

    form.append("lat", lat);
    form.append("lng", lng);

    const response = await showSpinner(
      fetch(`/api/map?/reverseGeoCode`, {
        method: "POST",
        body: form,
      }),
    );

    const data = deserialize(await response.text());

    if (data.data && data.data.results)
      selectedLocationData = data.data.results[0];

    if (selectedLocationData) {
      placeName = selectedLocationData?.formatted || "Area name not available";
    } else {
      placeName = "Area name not found";
    }
  }

  function selectItem(item) {
    selectedItem = item;

    map.setView(item.coordinates);
    addMarker(item.coordinates);
    addTempPopup(item.coordinates);
  }

  function addMarker(coordiantes) {
    if (marker) {
      marker.setLatLng(coordiantes);
      addTempPopup(coordiantes);
    } else {
      marker = leaflet.marker(coordiantes).addTo(map);
      addTempPopup(coordiantes);
    }
  }

  function addTempPopup(coordinates) {
    if (lastPopup) {
      map.removeLayer(lastPopup);
    }

    var greenIcon = leaflet?.icon({
      iconUrl: "/options/0.svg",
      shadowUrl: "",

      iconSize: [0, 1],
      shadowSize: [50, 64],
      iconAnchor: [17, 45],
      shadowAnchor: [4, 62],
      popupAnchor: [3, -30],
    });

    const customOptions = {
      maxWidth: "800",
      className: "custom",
    };

    let marker = leaflet
      ?.marker(coordinates, { icon: greenIcon })
      .addTo(map)
      .bindPopup(popupRef, customOptions);

    lastPopup = marker;

    marker.openPopup();

    marker.on("popupclose", () => {
      map.removeLayer(marker);
    });
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
      coordinates = { lat, lng };
      let coordinates_array = [lat, lng];

      await getAreaDetails(lat, lng);

      addMarker(coordinates_array);
    });
  });
</script>

<div id="map"></div>

<div class="info-container">
  <Section class="flex flex-col gap-0 h-full py-3">
    <div class="flex items-start justify-between mb-5">
      <div class="w-full">
        <h1 class="font-semibold text-[#101828] text-3xl">Hotspots</h1>
        <p class="font-normal text-[#475467] text-base mt-1">
          Create or edit hotpots
        </p>
      </div>
    </div>

    <Table>
      <TableFrame>
        <TableBody>
          <TableHeaderRow>
            <TableBodyHeader class="col-span-1">Name</TableBodyHeader>
            <TableBodyHeader class="col-span-1">Location</TableBodyHeader>
            <TableBodyHeader class="col-span-1">Description</TableBodyHeader>
            <TableBodyHeader class="col-span-1"></TableBodyHeader>
          </TableHeaderRow>

          {#each hotspots.data || [] as item}
            <TableRow
              class="items-center hover:cursor-pointer hover:bg-slate-100"
              onClick={() => {
                selectItem(item);
              }}
            >
              <TableCell
                class="col-span-1 flex gap-3 font-normal text-sm text-[#475467]"
                >{item?.name}</TableCell
              >
              <TableCell
                class="col-span-1 flex gap-3 font-normal text-sm text-[#475467]"
                >{item?.location_name}</TableCell
              >
              <TableCell
                class="col-span-1 flex gap-3 font-normal text-sm text-[#475467]"
                >{item?.description}</TableCell
              >
              <TableCell
                class="col-span-1 flex gap-3 font-normal text-sm text-[#475467]"
                ><TableButton onClick={() => {}}><IconEdit /></TableButton>
                <TableButton onClick={() => {}}><IconTrash /></TableButton
                ></TableCell
              >
            </TableRow>
          {/each}
        </TableBody>
      </TableFrame>
      <TableFooter>
        <Pagination totalItems={hotspots?.total || 0} onPageChange={() => {}} />
      </TableFooter>
    </Table>
  </Section>
</div>

<HotspotPopup
  bind:popupRef
  {placeName}
  {coordinates}
  {selectedItem}
  item={selectedItem ? JSON.parse(JSON.stringify(selectedItem)) : undefined}
/>

<style>
  #map {
    height: 400px;
    width: 100%;
  }
</style>
