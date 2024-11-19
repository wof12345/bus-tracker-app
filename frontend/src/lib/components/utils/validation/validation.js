function empty(value = "") {
  if (value === "") {
    return { error: "Cannot be empty.", value: value.value || value };
  }
  if (minimumLength(value, 1)) return minimumLength(value, 1);

  return value;
}

function minimumLength(value = "", len = 3) {
  if (value?.length < len) {
    return {
      error: `Must be a minimum of ${len} characters`,
      value: value.value || value,
    };
  }

  return value;
}

function validateEmail(value = "") {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  return emailRegex.test(value);
}

function validatePhoneNumber(value = "") {
  return !/[a-zA-Z]/.test(value);
}

function password(value = "") {
  if (value.length < 8) {
    return {
      error: "Must be at least 8 characters.",
      value: value.value || value,
    };
  }

  return empty(value);
}

function email(value = "") {
  if (!validateEmail(value)) {
    return {
      error: "Must be a valid email.",
      value: value?.error ? value.value : value,
    };
  }

  return empty(value);
}

function phone(value = "") {
  if (!validatePhoneNumber(value)) {
    return {
      error: "Must be a valid phone number.",
      value: value?.error ? value.value : value,
    };
  }

  return minimumLength(value, 8);
}

export function validateInput(form, exclude = []) {
  let valid = true;

  let formValidity = {};

  // return;
  for (let key in form) {
    let value = form[key];


    if (exclude.find(string => string === key)) {
      continue
    }

    if (key === "email") {
      value = email(value);
    }

    if (key === "password") {
      value = password(value);
    }

    if (key === "phone" || key === "number") {
      value = phone(value);
    }

    if (value && typeof value === "object" && !("error" in value)) {
      if (value?.length !== undefined && value?.length === 0) {

        value = {
          error: "Select at least one",
          value: [],
        };
      } else {
        valid = validateInput(value, exclude);
        value = value;
      }
    }

    form[key] = empty(value);

    if (!value || value.error) formValidity[key] = false;
  }

  for (let key in formValidity) {
    if (!formValidity[key]) {
      valid = false;
      break;
    }
  }

  return valid;
}

export function extractFormDataFromObject(formData = {}) {
  let form = new FormData();

  for (let key in formData) {
    if (typeof formData[key] !== "object") form.append(key, formData[key]);
    else form.append(key, JSON.stringify(formData[key]));
  }

  return form;
}

export function mapObjectFromKeys(object = {}, mapObject = {}, strict = true) {
  for (let key in object) {
    if (strict) {
      if (key in mapObject) mapObject[key] = object[key];
    } else mapObject[key] = object[key];
  }

  return mapObject;
}
