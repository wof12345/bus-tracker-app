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

const isAdmin = (store: any = initialState) => {
  if (store.user?.role === "admin") return true;
};

const isTeacher = (store: any = initialState) => {
  if (store.user?.role === "tutor") return true;
};

const isStudent = (store: any = initialState) => {
  if (store.user?.role === "student") return true;
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

export { authStore, isAdmin, isTeacher, isStudent, logout };
