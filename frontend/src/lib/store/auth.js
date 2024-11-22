import { writable } from "svelte/store";
import { deleteCache } from "$lib/components/utils/localstorage";
import { goto } from "$app/navigation";
import { deserialize } from "$app/forms";
import { showSpinner } from "./spinner";

const initialState = {
  isAuthenticated: undefined,
  user: undefined,
  userInfo: undefined,
};

const authStore = writable(initialState);

const isAdmin = (store = initialState) => {
  if (store?.role === "admin") return true;
};

const isCommuter = (store = initialState) => {
  if (store?.role === "commuter") return true;
};
const isDriver = (store = initialState) => {
  if (store?.role === "driver") return true;
};
const isHelper = (store = initialState) => {
  if (store?.role === "helper") return true;
};

const isManager = (store = initialState) => {
  if (store?.role === "manager") return true;
};

const logout = async () => {
  deleteCache("user");
  initialState.user = undefined;

  const res = await showSpinner(
    fetch("/logout?/logout", {
      method: "POST",
      body: new FormData(),
    }),
  );
  const data = deserialize(await res.text());

  if (data.status === 200) {
    goto("/");
    authStore.set({ isAuthenticated: false, user: undefined });
  }
};

export {
  authStore,
  isAdmin,
  isCommuter,
  isDriver,
  isManager,
  isHelper,
  logout,
};
