<script>
  import { deserialize } from "$app/forms";
  import { showToaster } from "$lib/store/toaster";
  import { onDestroy, onMount } from "svelte";
  import Button from "./Base/Buttons/Button.svelte";
  import Input from "./Base/Forms/Inputs/Input.svelte";
  import { validateApiResponse } from "./utils/validateApiResponse";
  import { invalidateAll } from "$app/navigation";

  export let popupRef;
  export let coordinates;
  export let placeName;
  export let selectedItem;
  export let item;

  let editState = false;

  let hotspotForm = {
    name: undefined,
    description: undefined,
  };

  async function editHotspot() {
    let form = new FormData();

    form.append("name", item.name);
    form.append("location_name", item.placee_name);
    form.append("description", item.description);
    form.append("coordinates", JSON.stringify(item.coordinates));

    const response = await fetch(`/api/hotspots?/create`, {
      method: "POST",
      body: form,
    });

    const data = deserialize(await response.text());

    if (!validateApiResponse(data)) {
      return;
    }

    showToaster("Hotspot created");
    await invalidateAll();
    editState = false;
  }

  async function saveHotspot() {
    let form = new FormData();

    form.append("name", hotspotForm.name);
    form.append("location_name", placeName);
    form.append("description", hotspotForm.description);
    form.append(
      "coordinates",
      JSON.stringify([coordinates.lat, coordinates.lng]),
    );

    const response = await fetch(`/api/hotspots?/create`, {
      method: "POST",
      body: form,
    });

    const data = deserialize(await response.text());

    console.log(data);

    if (!validateApiResponse(data)) {
      return;
    }

    showToaster("Hotspot created");
    await invalidateAll();

    selectedItem = data.data;
    item = data.data;
    editState = false;
  }
</script>

<div class="hidden">
  <div
    bind:this={popupRef}
    class="popup flex flex-col gap-2 aspect-auto bg-white"
  >
    {#if item}
      <p>
        Selected Coordinates: <br />
        <span class="font-bold"> Latitude:</span>
        {item.coordinates[0]} <br />
        <span class="font-bold"> Longitude:</span>
        {item.coordinates[1]}
      </p>
      <p class="max-w-[200px]">
        <span class="font-bold"> Area Name:</span>
        {item.location_name}
      </p>
    {:else}
      <p>
        Selected Coordinates: <br />
        <span class="font-bold"> Latitude:</span>
        {coordinates.lat} <br />
        <span class="font-bold"> Longitude:</span>
        {coordinates.lng}
      </p>
      <p class="max-w-[200px]">
        <span class="font-bold"> Area Name:</span>
        {placeName}
      </p>
    {/if}

    {#if item}
      <Input
        containerClass="h-[40px]"
        bind:value={item.name}
        placeholder={"Enter custom name"}
        disabled={!editState}
      />
      <Input
        bind:value={item.description}
        placeholder={"Enter description"}
        disabled={!editState}
      />
    {/if}

    {#if !editState}
      <Button
        variant="primary"
        onClick={(e) => {
          editState = true;
          e.stopPropagation();
        }}>{item ? "Edit" : "New"}</Button
      >
    {:else if !item}
      <div class="flex flex-col gap-2">
        <Input
          containerClass="h-[40px]"
          bind:value={hotspotForm.name}
          placeholder={"Enter custom name"}
        />
        <Input
          bind:value={hotspotForm.description}
          placeholder={"Enter description"}
        />
      </div>
    {/if}

    {#if editState}
      <div class="flex gap-2 justify-between">
        <Button
          variant="primary"
          onClick={(e) => {
            if (item) editHotspot();
            else saveHotspot();
            e.stopPropagation();
          }}>Save</Button
        >
        <Button
          variant="primary"
          onClick={(e) => {
            editState = false;
            if (item) item = JSON.parse(JSON.stringify(selectedItem));
            item = item;

            console.log(item);
            e.stopPropagation();
          }}>Cancel</Button
        >
      </div>
    {/if}
  </div>
</div>
