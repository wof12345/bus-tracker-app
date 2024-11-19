import { writable } from "svelte/store";

let initialState = {
  state: false,
  title: undefined as unknown | string,
  message: undefined as unknown | string,
  status: "error" as "error" | "success",
};
const toasterStore = writable(initialState);

function showToaster(title: string = "", message: string = "", isError: "error" | "success" = "success", delay: number = 2400) {
  toasterStore.set({ state: true, title: title || "Error", message: message || "", status: isError });

  setTimeout(() => {
    toasterStore.set(initialState);
  }, delay);
}

export { toasterStore, showToaster };
