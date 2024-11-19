import { getCookie } from "$components/utils/clientCookie";

type ValueType = string | boolean | number;

const ENVIRONMENT = import.meta.env.VITE_ENVIRONMENT;

// let PUBLIC_BASE_URL = process.env.VITE_PUBLIC_BASE_URL;
let PUBLIC_BASE_URL =
  ENVIRONMENT === "dev"
    ? import.meta.env.VITE_PUBLIC_BASE_URL
    : process.env.VITE_PUBLIC_BASE_URL;
interface PostOptions<T> {
  body: T;
  params?: Record<string, ValueType>;
}

async function get(
  pathname: string,
  token: string | undefined,
  nodeFetch: any,
  params?: Record<string, string>,
  stringParam:any=undefined
) {
  const url = new URL(pathname, PUBLIC_BASE_URL);
  url.search = new URLSearchParams(params).toString();

  token = token || getCookie();

  const options: RequestInit = {
    method: "GET",
  };

  if (token) {
    options.headers = {
      Authorization: `Bearer ${token}`,
    };
  }

  //determine fetch (node  || browser)
  let apiFetch = nodeFetch || fetch;

  const response = await apiFetch(url.toString()+(stringParam?"&"+stringParam:""), options);

  return response;
}

async function post(
  pathname: string,
  token: string | undefined,
  nodeFetch: any,
  options: PostOptions<any>,
) {
  const url = new URL(pathname, PUBLIC_BASE_URL);
  url.search = new URLSearchParams(options.params ?? {}).toString();

  token = token || getCookie();

  const fetchOptions: RequestInit = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(options.body),
  };

  if (token) {
    fetchOptions.headers = {
      ...fetchOptions.headers,
      Authorization: `Bearer ${token}`,
    };
  }

  //determine fetch (node  || browser)
  let apiFetch = nodeFetch || fetch;

  const response = await apiFetch(url.toString(), fetchOptions);

  return response;
}

async function patch(
  pathname: string,
  token: string | undefined,
  nodeFetch: any,
  options: PostOptions,
) {
  const url = new URL(pathname, PUBLIC_BASE_URL);
  url.search = new URLSearchParams(options.params ?? {}).toString();

  token = token || getCookie();

  const fetchOptions: RequestInit = {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(options.body),
  };

  if (token) {
    fetchOptions.headers = {
      ...fetchOptions.headers,
      Authorization: `Bearer ${token}`,
    };
  }

  //determine fetch (node  || browser)
  let apiFetch = nodeFetch || fetch;

  const response = await apiFetch(url.toString(), fetchOptions);

  return response;
}

async function put(
  pathname: string,
  token: string | undefined,
  nodeFetch: any,
  options: PostOptions,
) {
  const url = new URL(pathname, PUBLIC_BASE_URL);
  url.search = new URLSearchParams(options.params ?? {}).toString();

  token = token || getCookie();

  const fetchOptions: RequestInit = {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(options.body),
  };

  if (token) {
    fetchOptions.headers = {
      ...fetchOptions.headers,
      Authorization: `Bearer ${token}`,
    };
  }

  //determine fetch (node  || browser)
  let apiFetch = nodeFetch || fetch;

  const response = await apiFetch(url.toString(), fetchOptions);

  return response;
}

async function del(
  pathname: string,
  token: string | undefined,
  nodeFetch: any,
) {
  const url = new URL(pathname, PUBLIC_BASE_URL);

  token = token || getCookie();

  const fetchOptions: RequestInit = {
    method: "DELETE",
  };

  if (token) {
    fetchOptions.headers = {
      Authorization: `Bearer ${token}`,
    };
  }

  //determine fetch (node  || browser)
  let apiFetch = nodeFetch || fetch;

  const response = await apiFetch(url.toString(), fetchOptions);

  return response;
}

async function upload(
  pathname: string,
  token: string | undefined,
  nodeFetch: any,
  file: File,
  method: "POST",
) {
  const formData = new FormData();
  formData.append("file", file);

  const url = new URL(pathname, PUBLIC_BASE_URL);

  token = token || getCookie();

  const fetchOptions: RequestInit = {
    method,
    body: formData,
  };

  if (token) {
    fetchOptions.headers = {
      Authorization: `Bearer ${token}`,
    };
  }

  //determine fetch (node  || browser)
  let apiFetch = nodeFetch || fetch;

  const response = await apiFetch(url.toString(), fetchOptions);

  return response;
}

interface ExportCSVOptions {
  pathname: string;
  params?: Record<string, any>;
  filename: string;
}

const api = {
  get,
  post,
  patch,
  put,
  del,
  upload,
};

export default api;
