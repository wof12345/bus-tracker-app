<script>
  import TableHeader from "$components/Tables/Components/TableHeader.svelte";
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
  import { showSpinner } from "$lib/store/spinner.js";
  import { validateApiResponse } from "$components/utils/validateApiResponse.js";
  import { showToaster } from "$lib/store/toaster.ts";
  import { invalidateAll } from "$app/navigation";
  import Input from "$components/Base/Forms/Inputs/Input.svelte";
  import Menu from "$components/Base/Menu/Menu.svelte";
  import Option from "$components/Base/Forms/Components/Option.svelte";

  export let data;

  $: hotspots = data?.hotspots;

  let popupRef;
  let lastPopup;

  $: popupEditState = false;

  let leaflet;
  let map;
  let marker;
  let coordinates = { lat: null, lng: null };
  let placeName = "Click on the map to get the area name";

  let selectedItem;
  let selectedItemRef;

  let selectedLocationData;

  let search;
  let searchResults = [];
  let searchTimeOut;

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

  async function getAreaDetails(lat, lng) {
    selectedItemRef = selectedItem = undefined;

    popupEditState = false;
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

  async function searchQuery(search) {
    if (!search || search === "" || searchTimeOut) return;

    searchTimeOut = setTimeout(async () => {
      getAreaCoords(search);
      clearTimeout(searchTimeOut);
      searchTimeOut = undefined;
    }, 900);
  }

  $: searchQuery(search);

  function selectItem(item) {
    selectedItem = item;
    selectedItemRef = selectedItem
      ? JSON.parse(JSON.stringify(selectedItem))
      : undefined;

    popupEditState = false;

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

  async function invokeInformationLocation(lat, lng) {
    coordinates = { lat, lng };
    await getAreaDetails(lat, lng);
    let coordinates_array = [lat, lng];

    addMarker(coordinates_array);
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

      invokeInformationLocation(lat, lng);
    });
  });
</script>

<div
  class="search_anchor absolute top-10 m-auto left-0 right-0 z-[100] max-w-[300px]"
>
  <Input bind:value={search} placeholder={"Search a location"} />

  <Menu
    class="max-h-[400px]"
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

<div class="info-container">
  <Section class="flex flex-col gap-0 h-full py-3">
    <TableHeader
      class="mb-3"
      title="Hotspots"
      subtitle=" Create or edit hotpots"
    />

    <Table>
      <TableFrame>
        <TableBody>
          <TableHeaderRow>
            <TableBodyHeader class="col-span-1">Name</TableBodyHeader>
            <TableBodyHeader class="col-span-1">Location</TableBodyHeader>
            <TableBodyHeader class="col-span-1">Description</TableBodyHeader>
            <TableBodyHeader class="col-span-1"></TableBodyHeader>
          </TableHeaderRow>

          {#each hotspots?.data || [] as item}
            <TableRow
              class="items-center hover:cursor-pointer hover:bg-slate-100"
              onClick={(e) => {
                selectItem(item);

                e.stopPropagation();
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
                class="col-span-1 flex justify-end gap-3 font-normal text-sm text-[#475467]"
                ><TableButton
                  onClick={(e) => {
                    selectItem(item);
                    popupEditState = true;

                    e.stopPropagation();
                  }}><IconEdit /></TableButton
                >
                <TableButton
                  onClick={async (e) => {
                    e.stopPropagation();

                    let form = new FormData();

                    form.append("_id", item._id);

                    const response = await fetch(`?/delete`, {
                      method: "POST",
                      body: form,
                    });

                    const data = deserialize(await response.text());

                    if (!validateApiResponse(data)) {
                      return;
                    }

                    showToaster("Hotspot deleted");
                    await invalidateAll();
                  }}><IconTrash /></TableButton
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
  bind:selectedItem
  bind:item={selectedItemRef}
  bind:editState={popupEditState}
/>

<style>
  #map {
    height: 400px;
    width: 100%;
  }
</style>
