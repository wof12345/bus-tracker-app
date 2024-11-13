import { writable } from "svelte/store";

let initialState = {
    dates: {}
};
const datePickerStore = writable(initialState);

function addDates(newDates) {
    datePickerStore.update(state => {
        return {
            ...state,
            dates: { ...state.dates, ...newDates }
        };
    });
}

function clearDates() {
    datePickerStore.set({ dates: {} });
}


export { datePickerStore, addDates, clearDates };
