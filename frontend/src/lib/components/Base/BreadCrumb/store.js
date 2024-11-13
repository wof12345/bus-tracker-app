import { writable } from "svelte/store";

let initialState = {
  pathLookUp: [], //idx, path
};
const breadcrumbStore = writable(initialState);

async function setPathLookUp(pathAlias) {
  breadcrumbStore.set({ pathLookUp: { ...pathAlias } });
}

async function clearPathAlias() {
  breadcrumbStore.set({ pathLookUp: {} });
}

export { breadcrumbStore, setPathLookUp, clearPathAlias };
