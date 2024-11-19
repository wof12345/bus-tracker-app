import { writable } from "svelte/store";

let initialState = {
  state: false,
  pageLoading: false,
};

const spinnerStore = writable(initialState);

async function showSpinner(
  promise: any = undefined,
  isRouteLoader = false,
  delay = 2400,
) {
  spinnerStore.set({ state: true, pageLoading: isRouteLoader ? true : false });

  if (promise) {
    try {
      const res = await promise;

      spinnerStore.set(initialState);
      return res;
    } catch (error) {
      spinnerStore.set(initialState);
      return { message: error.message };
    }
  } else {
    spinnerStore.set(initialState);
    setTimeout(() => {
      spinnerStore.set(initialState);
    }, 4000);
    return { message: "Not a promise" };
  }
}
export { spinnerStore, showSpinner };
