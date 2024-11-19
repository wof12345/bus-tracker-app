export async function handleUserAndTutorStoreInfo(data, authStore, deserialize, pathName, validateApiResponse, goto) {
  const user = data?.user;

  let form = new FormData();

  let userData = user?.user;



  let tutor = {};
  let userInfo = {};

  if (userData?.role === "tutor") {
    const tutorData = await fetch("/api/account?/getTutorInfo", {
      method: "POST",
      body: form,
    });

    let tutorDataRes = deserialize(await tutorData.text());

    tutor = tutorDataRes.data;

    const tutorApplicationData = await fetch(
      "/api/account?/getTutorApplication",
      {
        method: "POST",
        body: form,
      },
    );

    let tutorApplicationResponse = deserialize(
      await tutorApplicationData.text(),
    );

    if (!validateApiResponse(tutorApplicationResponse, false))
      tutor["application"] = undefined;
    else tutor["application"] = tutorApplicationResponse.data;

    if (pathName?.includes("private")) {
      for (let key in tutor) {
        if (!tutor[key] && key !== "areas") {
          if (
            !pathName?.includes("tutor") ||
            !pathName?.includes("student")
          ) {

            goto("/tutor/additional-information");
            break;
          }
        }
      }
    }
    const tutorBankData = await fetch("/api/account?/getTutorBankDetails", {
      method: "POST",
      body: form,
    });

    let tutorBankResponse = deserialize(await tutorBankData.text());

    if (!validateApiResponse(tutorBankResponse, false))
      tutor["bank"] = undefined;
    else tutor["bank"] = tutorBankResponse.data;
  }

  const userInfoData = await fetch("/api/account?/getUserInfo", {
    method: "POST",
    body: form,
  });

  let userInfoDataRes = deserialize(await userInfoData.text());

  if (!validateApiResponse(userInfoDataRes, false)) userInfo = undefined;
  else userInfo = userInfoDataRes.data;

  authStore.set({
    ...user,
    tutor,
    userInfo,
    isAuthenticated: user ? true : false,
  });
}