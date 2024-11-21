import { validateApiResponse } from "$components/utils/validateApiResponse";
import api from "$lib/api/api";


const ENVIRONMENT = import.meta.env.VITE_ENVIRONMENT;


// let PUBLIC_BASE_URL = 'http://backend:8000' //deubug



let PUBLIC_BASE_URL =
  ENVIRONMENT === "dev"
    ? import.meta.env.VITE_PUBLIC_BASE_URL
    : process.env.VITE_PUBLIC_BASE_URL;



export async function handleFetch({ request, fetch }) {
  const url = new URL(request.url);
  const path = url.pathname;

  const queryParams = url.searchParams.toString();

  const fullPath = `${path}${queryParams ? "?" + queryParams : ""}`;

  //logs for debug purpose
  console.log(request.url, url);
  if (request.url.includes('localhost'))
    request = new Request(`${PUBLIC_BASE_URL}${fullPath}`, request);
  // request = new Request(url, request);
  // console.log(request.url, `${PUBLIC_BASE_URL}${fullPath}`, request.url.includes('localhost'), PUBLIC_BASE_URL, ENVIRONMENT);

  return fetch(request);
}

export const handle = async ({ event, resolve }) => {
  let pathName = event.url.pathname;

  //handle persisiting auth
  const verifyUser = async () => {
    let dummy = { first_name: 'test', email: 'example@gmail.com' }
    try {

      const token = event.cookies.get("token");

      const fetch = event.fetch;

      try {
        const res = await api.get("/auth/verify", token, fetch);

        let data = await res.json();

        console.log(data);

        if (!validateApiResponse(data)) return null;
        // if (!validateApiResponse(data)) return dummy

        return data;
      } catch (error) {

        console.log('err', error);
        return dummy
      }



    } catch (error) {
      console.log(error)
      return
    }
  };


  //pass down functions and utils to child server pages
  event.locals.verifyUser = verifyUser;
  event.locals.ENVIRONMENT = ENVIRONMENT

  return await resolve(event);
};
