<script>
  import GroupedInput from "$lib/components/Base/Forms/Components/GroupedInput.svelte";
  import { authStore } from "$lib/store/auth";
  import UserInfo from "$lib/layouts/AdditionalInformation/UserInfo.svelte";
  import StepIconBase from "$components/Assets/StepIconBase.svelte";
  import StepIconCompleted from "$components/Assets/StepIconCompleted.svelte";
  import StepIconCurrent from "$components/Assets/StepIconCurrent.svelte";
  import Button from "$components/Base/Buttons/Button.svelte";

  import Step from "$components/Base/Step/Step.svelte";
  import StepHeader from "$components/Base/Step/StepHeader.svelte";
  import StepHeaders from "$components/Base/Step/StepHeaders.svelte";
  import StepPanel from "$components/Base/Step/StepPanel.svelte";
  import StepPanels from "$components/Base/Step/StepPanels.svelte";
  import Text from "$components/Base/Typography/Text.svelte";
  import Title from "$components/Base/Typography/Title.svelte";

  import { step_active } from "$components/Base/Step/stepStore";
  import StepSteps from "$lib/layouts/Auth/StepSteps.svelte";
  import Radiobox from "$components/Base/Forms/Inputs/Radiobox.svelte";
  import Input from "$components/Base/Forms/Inputs/Input.svelte";
  import TextArea from "$components/Base/Forms/Inputs/TextArea.svelte";
  import CheckBox from "$components/Base/Forms/Inputs/CheckBox.svelte";
  import { goto } from "$app/navigation";
  import Logo from "$components/Nav/Logo.svelte";
  import { deserialize } from "$app/forms";
  import { showToaster } from "$lib/store/toaster";
  import FileUpload from "$components/Base/Forms/Inputs/FileUpload.svelte";
  import Paragraph from "$components/Base/Typography/Paragraph.svelte";
  import { showSpinner } from "$lib/store/spinner.ts";
  import { validateApiResponse } from "$components/utils/validateApiResponse.js";
  import { onMount } from "svelte";
  import { handleUserAndTutorStoreInfo } from "$components/utils/userInfoPopulation.js";
  import { page } from "$app/stores";
  import { validateInput } from "$components/utils/validation/validation.js";

  export let data;

  $: pathName = $page?.route?.id;

  $step_active = 4;

  let tutorForm = {
    years_of_experience: "",
    about_description: "",
    experience_description: "",
    native_lang: "",
    spoken_langs: [],
    preferred_curriculum: [],
    preferred_subjects: [],
    preferred_school_level: [],
    clean_convicted: false,
    available_hr_per_week: "",
    preferred_tutoring_type: "",
  };

  let pricingForm = {
    price: "",
  };

  let online_rate = 15;
  let in_person_rate = 20;

  let tutor_id;

  let nativeLangs = ["English", "Arabic", "French", "Other"];
  let experienceOptions = [
    "I'm a full-time professional teacher at a school/university.",
    "I'm a teacher assistant at a university.",
    "I have occasionally tutored on a part-time basis",
    "I have no experience in tutoring",
  ];

  const curriculums = [
    "French Baccalaureate",
    "International Bacclaureate",
    "Lebanese curriculum",
    "Cambridge International",
    "CBSE",
    "American curriculum",
    "British curriculum",
    "Saudi National curriculum",
    "UAE National curriculum",
    "Canadian curriculum",
  ];

  const subjects = [
    { name: "Mathematics", value: "Mathematics" },
    { name: "Physics", value: "Physics" },
    { name: "Chemistry", value: "Chemistry" },
    { name: "Biology", value: "Biology" },
    { name: "Economics", value: "Economics" },
    { name: "Business", value: "Business" },
    { name: "Geography", value: "Geography" },
    { name: "History", value: "History" },
    { name: "Homework help", value: "Homework help" },
    { name: "English", value: "English" },
    { name: "French", value: "French" },
    { name: "Spanish", value: "Spanish" },
    { name: "Arabic", value: "Arabic" },
    { name: "German", value: "German" },
    { name: "Italian", value: "Italian" },
    { name: "SAT", value: "SAT" },
    { name: "IELTS", value: "IELTS" },
    { name: "IGCSE", value: "IGCSE" },
    { name: "A-level", value: "A-level" },
    { name: "IB Diploma", value: "IB Diploma" },
    { name: "Psychology", value: "Psychology" },
    { name: "Artificial Intelligence", value: "Artificial Intelligence" },
    { name: "Cybersecurity", value: "Cybersecurity" },
    { name: "Python", value: "Python" },
    { name: "Computer Science", value: "Computer Science" },
    { name: "Statistics", value: "Statistics" },
    { name: "Web Development", value: "Web Development" },
  ];

  let selectedRadioButtonValues = {
    experience_description: "",
    native_lang: "",
    pricing: "",
    available_hr_per_week: "",
    preferred_tutoring_type: "",
  };

  let application = {
    id_files: undefined,
    cv_files: undefined,
    police_clearence: undefined,
    tutor_work_permit: undefined,
    proof_of_exp: undefined,
  };

  function handleSelect(set, event) {
    selectedRadioButtonValues[set] = event.detail.value;
    tutorForm[set] = event.detail.value;

    selectedRadioButtonValues = selectedRadioButtonValues;
    tutorForm = tutorForm;
  }

  let otherSpokenLang = "";
  let otherSubject = "";

  let langOther = false;
  let spokenOther = false;
  let subjectOther = false;
  let expOther = false;

  function handleTogglableInputs(e, x, z) {
    tutorForm.spoken_langs =
      tutorForm.spoken_langs.value || tutorForm.spoken_langs;

    if (
      (selectedRadioButtonValues.native_lang &&
        !nativeLangs.find(
          (elm) => elm === selectedRadioButtonValues.native_lang,
        )) ||
      selectedRadioButtonValues.native_lang === "Other"
    ) {
      langOther = true;
    } else {
      langOther = false;
    }

    if (
      (selectedRadioButtonValues.experience_description &&
        !experienceOptions.find(
          (elm) => elm === selectedRadioButtonValues.experience_description,
        )) ||
      selectedRadioButtonValues.experience_description === "Other"
    ) {
      expOther = true;
    } else if (selectedRadioButtonValues.experience_description) {
      expOther = false;
    }

    if (
      tutorForm.spoken_langs?.value?.find((elm) => elm === "Other") ||
      tutorForm.spoken_langs?.find((elm) => elm === "Other")
    ) {
      spokenOther = true;
    } else {
      let toRemove = tutorForm.spoken_langs?.indexOf(otherSpokenLang);

      if (toRemove > -1) tutorForm.spoken_langs.splice(toRemove, 1);

      spokenOther = false;
    }

    if (tutorForm.preferred_subjects?.find((elm) => elm === "Other")) {
      subjectOther = true;
    } else {
      let toRemove = tutorForm.preferred_subjects?.indexOf(otherSubject);

      if (toRemove > -1) tutorForm.preferred_subjects.splice(toRemove, 1);

      subjectOther = false;
    }
  }

  $: handleTogglableInputs(
    selectedRadioButtonValues,
    tutorForm.spoken_langs,
    tutorForm.preferred_subjects,
  );

  function populateUserInfo() {
    if (!$authStore?.tutor) return;

    let tutor = $authStore?.tutor;

    tutor_id = tutor.tutor_id;

    tutorForm.years_of_experience = tutor.years_of_exp;
    tutorForm.about_description = tutor.about_description;

    selectedRadioButtonValues.experience_description =
      tutor.experience_description;
    tutorForm.experience_description = tutor.experience_description;

    if (
      !experienceOptions.find((elm) => elm === tutor.experience_description)
    ) {
      if (experienceOptions.length > 0)
        selectedRadioButtonValues.experience_description = "Other";
      tutorForm.experience_description = tutor.experience_description;
    }

    selectedRadioButtonValues.native_lang = tutor.native_lang;
    tutorForm.native_lang = tutor.native_lang;

    if (!nativeLangs.find((elm) => elm === tutor.native_lang)) {
      if (nativeLangs.length > 0)
        selectedRadioButtonValues.native_lang = "Other";

      tutorForm.native_lang = tutor.native_lang;
    }

    selectedRadioButtonValues.available_hr_per_week =
      tutor.available_hr_per_week;
    selectedRadioButtonValues.preferred_tutoring_type =
      tutor.preferred_tutoring_type;
    tutorForm.available_hr_per_week = tutor.available_hr_per_week;
    tutorForm.preferred_tutoring_type = tutor.preferred_tutoring_type;

    tutorForm.preferred_school_level = tutor.preferred_school_levels;

    tutorForm.spoken_langs = tutor.spoken_langs;
    if (tutorForm.spoken_langs?.find((elm) => elm === "Other")) {
      otherSpokenLang = tutor.spoken_langs[tutor.spoken_langs.length - 1];
    }

    tutorForm.preferred_curriculum = tutor.preferred_curriculum;

    tutorForm.preferred_subjects = tutor.preferred_subjects;
    if (tutorForm.preferred_subjects?.find((elm) => elm === "Other")) {
      otherSubject =
        tutor.preferred_subjects[tutor.preferred_subjects.length - 1];
    }

    tutorForm.clean_convicted = tutor.clean_convicted;

    if (
      tutor.in_person_rate &&
      tutor.online_rate &&
      tutor.in_person_rate != tutor.online_rate
    )
      selectedRadioButtonValues.pricing = "yes";
    else {
      selectedRadioButtonValues.pricing = "no";
      pricingForm.price = tutor.in_person_rate || tutor.online_rate;
    }

    handleTogglableInputs();
  }

  $: populateUserInfo($authStore);

  async function handleGeneralActive() {
    if (!validateInput(tutorForm)) {
      showToaster("Please fill in all required fields.", undefined, "error");
      tutorForm = tutorForm;
      return;
    }

    $step_active = 2;
  }

  async function handleStatusActive() {
    if (!tutorForm.clean_convicted) {
      showToaster("Please fill in all required fields.", undefined, "error");
      return;
    }

    $step_active = 3;
  }

  async function handlePricingActive() {
    if (!selectedRadioButtonValues.pricing || !validateInput(pricingForm)) {
      showToaster("Please fill in all required fields.", undefined, "error");
      pricingForm = pricingForm;
    }

    let form = new FormData();

    form.append("years_of_experience", tutorForm.years_of_experience);
    form.append("about_description", tutorForm.about_description);

    if (selectedRadioButtonValues.experience_description === "Other")
      form.append("experience_description", tutorForm.experience_description);
    else
      form.append(
        "experience_description",
        selectedRadioButtonValues.experience_description,
      );

    if (selectedRadioButtonValues.native_lang === "Other")
      form.append("native_lang", tutorForm.native_lang);
    else form.append("native_lang", selectedRadioButtonValues.native_lang);

    form.append(
      "available_hr_per_week",
      selectedRadioButtonValues.available_hr_per_week,
    );
    form.append(
      "preferred_tutoring_type",
      selectedRadioButtonValues.preferred_tutoring_type,
    );

    form.append(
      "preferred_school_level",
      JSON.stringify(tutorForm.preferred_school_level),
    );

    if (
      tutorForm.spoken_langs.find((elm) => elm === "Other") &&
      otherSpokenLang
    )
      form.append(
        "spoken_langs",
        JSON.stringify([...tutorForm.spoken_langs, otherSpokenLang]),
      );
    else form.append("spoken_langs", JSON.stringify(tutorForm.spoken_langs));

    form.append(
      "preferred_curriculum",
      JSON.stringify(tutorForm.preferred_curriculum),
    );

    if (
      tutorForm.preferred_subjects.find((elm) => elm === "Other") &&
      otherSubject
    )
      form.append(
        "preferred_subjects",
        JSON.stringify([...tutorForm.preferred_subjects, otherSubject]),
      );
    else
      form.append(
        "preferred_subjects",
        JSON.stringify(tutorForm.preferred_subjects),
      );

    form.append("clean_convicted", tutorForm.clean_convicted);

    form.append("tutor_id", tutor_id);

    if (selectedRadioButtonValues.pricing === "yes") {
      form.append("online_rate", online_rate);
      form.append("in_person_rate", in_person_rate);
    } else {
      form.append("online_rate", pricingForm.price);
      form.append("in_person_rate", pricingForm.price);
    }

    let tutorInfoUpdate = await showSpinner(
      fetch("/api/account?/updateTutorInfo", {
        method: "POST",
        body: form,
      }),
    );

    let tutorInfoUpdateResponse = deserialize(await tutorInfoUpdate.text());

    if (!validateApiResponse(tutorInfoUpdateResponse)) return;

    await handleUserAndTutorStoreInfo(
      data,
      authStore,
      deserialize,
      pathName,
      validateApiResponse,
      goto,
    );

    showToaster("Information updated");

    $step_active = 4;
  }

  async function handleApplicationActive() {
    if (!validateInput(application, ["deleted_at"])) {
      application = application;
      showToaster("Please fill in all required fields.", undefined, "error");
      return;
    }

    let form = new FormData();

    let files = {
      id_files: [
        {
          file_id: application.id_files?.id,
          document_type: "identity",
        },
      ],
      cv_files: [
        {
          file_id: application.cv_files?.id,
          document_type: "cv",
        },
      ],
      police_clearence: [
        {
          file_id: application.police_clearence?.id,
          document_type: "police_clearence",
        },
      ],
      proof_of_exp: [
        {
          file_id: application.proof_of_exp?.id,
          document_type: "proof_of_exp",
        },
      ],
    };

    if (application.tutor_work_permit?.id) {
      files["tutor_work_permit"] = [
        {
          file_id: application.tutor_work_permit?.id,
          document_type: "work_permit",
        },
      ];
    }
    form.append("id_files", JSON.stringify(files));

    let tutorInfoUpdate = await showSpinner(
      fetch("/api/account?/updateTutorApplication", {
        method: "POST",
        body: form,
      }),
    );

    let tutorInfoUpdateResponse = deserialize(await tutorInfoUpdate.text());
    if (!validateApiResponse(tutorInfoUpdateResponse)) return;

    await handleUserAndTutorStoreInfo(
      data,
      authStore,
      deserialize,
      pathName,
      validateApiResponse,
      goto,
    );

    showToaster("Information updated");

    goto("/tutor/additional-information/done");
  }

  onMount(async () => {
    await handleUserAndTutorStoreInfo(
      data,
      authStore,
      deserialize,
      pathName,
      validateApiResponse,
      goto,
    );
  });
</script>

<Step
  navigateOnClick={false}
  active={$step_active}
  class="h-screen flex-row overflow-y-hidden"
>
  <StepHeaders
    containerClass="hidden max-w-[400px] lg:flex"
    class=" h-full min-w-[383px] flex-col justify-between bg-[#821890] p-6 pt-8 md:pt-2 "
  >
    <div class="flex flex-col gap-9">
      <div class="mb-0 mt-10 flex items-center">
        <Logo alt={true} />
      </div>

      <div>
        <StepHeader
          textPrimary="About tutor"
          textSecondary="Please provide tutor’s details"
        >
          {#if $step_active == 0}
            <div class="flex h-[44px] w-[44px] items-center justify-center">
              <StepIconCurrent />
            </div>
          {:else if $step_active > 0}
            <div class="flex h-[44px] w-[44px] items-center justify-center">
              <StepIconCompleted />
            </div>
          {/if}
        </StepHeader>

        <StepHeader
          textPrimary="General information"
          textSecondary="Please provide your general information"
        >
          {#if $step_active == 1}
            <div class="flex h-[44px] w-[44px] items-center justify-center">
              <StepIconCurrent />
            </div>
          {:else if $step_active > 1}
            <div class="flex h-[44px] w-[44px] items-center justify-center">
              <StepIconCompleted />
            </div>
          {:else}
            <div class="flex h-[44px] w-[44px] items-center justify-center">
              <StepIconBase />
            </div>
          {/if}
        </StepHeader>

        <StepHeader
          textPrimary="Conviction status"
          textSecondary="Provide your conviction status"
        >
          {#if $step_active == 2}
            <div class="flex h-[44px] w-[44px] items-center justify-center">
              <StepIconCurrent />
            </div>
          {:else if $step_active > 2}
            <div class="flex h-[44px] w-[44px] items-center justify-center">
              <StepIconCompleted />
            </div>
          {:else}
            <div class="flex h-[44px] w-[44px] items-center justify-center">
              <StepIconBase />
            </div>
          {/if}
        </StepHeader>

        <StepHeader
          textPrimary="Pricing"
          textSecondary="Have a look at the pricing"
        >
          {#if $step_active == 3}
            <div class="flex h-[44px] w-[44px] items-center justify-center">
              <StepIconCurrent />
            </div>
          {:else if $step_active > 3}
            <div class="flex h-[44px] w-[44px] items-center justify-center">
              <StepIconCompleted />
            </div>
          {:else}
            <div class="flex h-[44px] w-[44px] items-center justify-center">
              <StepIconBase />
            </div>
          {/if}
        </StepHeader>

        <StepHeader
          textPrimary="Required documents"
          textSecondary="Please provide the documents"
        >
          {#if $step_active == 4}
            <div class="flex h-[44px] w-[44px] items-center justify-center">
              <StepIconCurrent />
            </div>
          {:else if $step_active > 4}
            <div class="flex h-[44px] w-[44px] items-center justify-center">
              <StepIconCompleted />
            </div>
          {:else}
            <div class="flex h-[44px] w-[44px] items-center justify-center">
              <StepIconBase />
            </div>
          {/if}
        </StepHeader>
      </div>
    </div>

    <div
      class=" flex flex-col items-center justify-between bg-transparent lg:flex-row"
    >
      <Text class="text-sm text-[#EEAAFD]">© example 2077</Text>
      <Text class="text-sm text-[#EEAAFD]">help@example.com</Text>
    </div>
  </StepHeaders>

  <div class="flex w-full flex-col bg-[#FFFFFF]">
    <StepPanels class="flex h-full w-full flex-col  ">
      <UserInfo {data} />

      <StepPanel class=" scroll-body h-full overflow-auto px-3 pt-10 lg:px-0">
        <div class="m-auto w-full max-w-3xl">
          <div class="flex flex-col items-center justify-start gap-8">
            <Logo alt={false} />
            <div class="space-y-3">
              <Title>General information</Title>
              <Text class=" text-base font-normal text-[#475467]"
                >Provide your general info to get registered.</Text
              >
            </div>
          </div>

          <div class="mt-8 grid grid-cols-1 lg:grid-cols-2 lg:gap-20">
            <div class="space-y-5">
              <div class="space-y-1.5">
                <Text class="text-left text-sm font-medium text-[#344054]"
                  >Tell us about you and your teaching experiene*</Text
                >
                <TextArea
                  class="h-[154px] "
                  maxLength={true}
                  placeholder="Type here..."
                  bind:value={tutorForm.about_description}
                />
                <Text class="text-left text-sm font-normal text-[#475467]"
                  >Please note that the following are mandatory to mention: the
                  subjects that you can tutor, your teaching experiences, the
                  schools that you taught at, your certifications, your grades,
                  and anything that adds credibility to your profile.</Text
                >
              </div>

              <div class="w-full space-y-1.5">
                <Text class="text-left text-sm font-medium text-[#344054]"
                  >How many years of experience do you have?*</Text
                >
                <Input
                  inputClass="placeholder:text-[#667085] placeholder:font-normal placeholder:text-base"
                  class="w-full max-w-[360px]"
                  label=""
                  name="first_name"
                  bind:value={tutorForm.years_of_experience}
                />
              </div>

              <div class="w-full space-y-2.5">
                <Text class="text-left text-sm font-medium text-[#344054]"
                  >What describes best the teaching experience you have?*</Text
                >
                <div class="space-y-2">
                  {#each experienceOptions as experience}
                    <Radiobox
                      text={experience}
                      value={experience}
                      isSelected={selectedRadioButtonValues.experience_description ===
                        experience}
                      on:select={(e) =>
                        handleSelect("experience_description", e)}
                    />
                  {/each}

                  <Radiobox
                    text="Other, please specify"
                    value="Other"
                    isSelected={selectedRadioButtonValues.experience_description ===
                      "Other"}
                    on:select={(e) => handleSelect("experience_description", e)}
                  />

                  {#if expOther}
                    <div class="grid gap-1">
                      <Input
                        inputClass="placeholder:text-[#667085] placeholder:font-normal placeholder:text-base"
                        class="mt-2 w-full max-w-[360px]"
                        label=""
                        name="city"
                        bind:value={tutorForm.experience_description}
                      />
                      <Text class="text-left text-sm font-normal text-[#475467]"
                        >Please type the other option here</Text
                      >
                    </div>
                  {/if}
                </div>
              </div>

              <div class="w-full space-y-2.5">
                <Text class="text-left text-sm font-medium text-[#344054]"
                  >Select your native language*</Text
                >
                <div class="space-y-2">
                  {#each nativeLangs as lang}
                    <Radiobox
                      text={lang}
                      value={lang}
                      isSelected={selectedRadioButtonValues.native_lang ===
                        lang}
                      on:select={(e) => handleSelect("native_lang", e)}
                    />
                  {/each}

                  {#if langOther}
                    <div class="grid gap-1">
                      <Input
                        inputClass="placeholder:text-[#667085] placeholder:font-normal placeholder:text-base"
                        class="mt-2 w-full max-w-[360px]"
                        bind:value={tutorForm.native_lang}
                        label=""
                        name=""
                      />
                      <Text class="text-left text-sm font-normal text-[#475467]"
                        >Please type the other option here</Text
                      >
                    </div>
                  {/if}
                </div>
              </div>

              <div class="w-full space-y-2.5">
                <Text class="text-left text-sm font-medium text-[#344054]"
                  >Select the languages that you speak with a good level of
                  proficiency*</Text
                >
                <GroupedInput value={tutorForm.spoken_langs}>
                  <div class="space-y-2">
                    <CheckBox
                      text="English"
                      bind:valueArray={tutorForm.spoken_langs}
                    />
                    <CheckBox
                      text="Arabic"
                      bind:valueArray={tutorForm.spoken_langs}
                    />
                    <CheckBox
                      text="Spanish"
                      bind:valueArray={tutorForm.spoken_langs}
                    />
                    <CheckBox
                      text="French"
                      bind:valueArray={tutorForm.spoken_langs}
                    />

                    <CheckBox
                      text="Other"
                      bind:valueArray={tutorForm.spoken_langs}
                    />

                    {#if spokenOther}
                      <div class="space-y-1">
                        <Input
                          inputClass="placeholder:text-[#667085] placeholder:font-normal placeholder:text-base"
                          class="w-full max-w-[360px] "
                          label=""
                          name=""
                          bind:value={otherSpokenLang}
                        />
                        <Text
                          class="text-left text-sm font-normal text-[#475467]"
                          >Please type the other option here</Text
                        >
                      </div>
                    {/if}
                  </div>
                </GroupedInput>
              </div>

              <div
                class="w-full max-w-[360px] items-start justify-start space-y-2.5"
              >
                <Text class="text-left text-sm font-medium text-[#344054]"
                  >How would you like to conduct your private tutoring sessions?
                  (please note that we have a high demand for In-person
                  sessions)*</Text
                >
                <div class="space-y-2">
                  <Radiobox
                    text="Online"
                    value="Online"
                    isSelected={selectedRadioButtonValues.preferred_tutoring_type ===
                      "Online"}
                    on:select={(e) =>
                      handleSelect("preferred_tutoring_type", e)}
                  />
                  <Radiobox
                    text="In-person"
                    value="In-person"
                    isSelected={selectedRadioButtonValues.preferred_tutoring_type ===
                      "In-person"}
                    on:select={(e) =>
                      handleSelect("preferred_tutoring_type", e)}
                  />
                  <Radiobox
                    text="Both"
                    value="Both"
                    isSelected={selectedRadioButtonValues.preferred_tutoring_type ===
                      "Both"}
                    on:select={(e) =>
                      handleSelect("preferred_tutoring_type", e)}
                  />
                </div>
              </div>
            </div>

            <div class="mt-4 space-y-4 md:mt-0">
              <div class="flex flex-col gap-2">
                <GroupedInput value={tutorForm.preferred_curriculum}>
                  <Text class="text-left text-sm font-medium text-[#344054]"
                    >Preferred curriculum to teach*</Text
                  >
                  {#each curriculums as curriculum}
                    <CheckBox
                      text={curriculum}
                      bind:valueArray={tutorForm.preferred_curriculum}
                    />
                  {/each}
                </GroupedInput>
              </div>

              <div class="space-y-2.5">
                <div class="space-y-2.5">
                  <Text class="text-left text-sm font-medium text-[#344054]"
                    >Preferred subjects to teach*</Text
                  >

                  <GroupedInput value={tutorForm.preferred_subjects}>
                    <div class="grid grid-cols-1 gap-2.5 lg:grid-cols-2">
                      {#each subjects as subject}
                        <CheckBox
                          text={subject.value}
                          bind:valueArray={tutorForm.preferred_subjects}
                        />
                      {/each}

                      <CheckBox
                        text={"Other"}
                        bind:valueArray={tutorForm.preferred_subjects}
                      />
                    </div>
                  </GroupedInput>

                  {#if subjectOther}
                    <div class="space-y-1">
                      <Input
                        inputClass="placeholder:text-[#667085] placeholder:font-normal placeholder:text-base"
                        class="w-full max-w-[360px] "
                        label=""
                        name=""
                      />
                      <Text class="text-left text-sm font-normal text-[#475467]"
                        >Please type the other option here</Text
                      >
                    </div>
                  {/if}

                  <div class="space-y-2.5">
                    <Text class="text-left text-sm font-medium text-[#344054]"
                      >Preferred school level*</Text
                    >
                    <GroupedInput value={tutorForm.preferred_school_level}>
                      <div class="space-y-2">
                        <CheckBox
                          text="Elementry School"
                          bind:valueArray={tutorForm.preferred_school_level}
                        />
                        <CheckBox
                          text="Middle School"
                          bind:valueArray={tutorForm.preferred_school_level}
                        />
                      </div>
                    </GroupedInput>
                  </div>

                  <div class="w-full space-y-2.5">
                    <Text class="text-left text-sm font-medium text-[#344054]"
                      >Available hours per week*</Text
                    >

                    <GroupedInput value={tutorForm.available_hr_per_week}>
                      <div class="space-y-2">
                        <Radiobox
                          text="1-5 Hours"
                          value="1-5 Hours"
                          isSelected={selectedRadioButtonValues.available_hr_per_week ===
                            "1-5 Hours"}
                          on:select={(e) =>
                            handleSelect("available_hr_per_week", e)}
                        />
                        <Radiobox
                          text="4-6 Hours"
                          value="4-6 Hours"
                          isSelected={selectedRadioButtonValues.available_hr_per_week ===
                            "4-6 Hours"}
                          on:select={(e) =>
                            handleSelect("available_hr_per_week", e)}
                        />
                        <Radiobox
                          text="6-10 Hours"
                          value="6-10 Hours"
                          isSelected={selectedRadioButtonValues.available_hr_per_week ===
                            "6-10 Hours"}
                          on:select={(e) =>
                            handleSelect("available_hr_per_week", e)}
                        />

                        <Radiobox
                          text="10+"
                          value="10+"
                          isSelected={selectedRadioButtonValues.available_hr_per_week ===
                            "10+"}
                          on:select={(e) =>
                            handleSelect("available_hr_per_week", e)}
                        />
                      </div>
                    </GroupedInput>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="mx-auto mt-8 w-full items-center justify-center">
            <Button
              variant="primary"
              class="mx-auto mb-4 flex  w-full max-w-[360px] justify-center md:mb-10"
              onClick={handleGeneralActive}
            >
              Continue
            </Button>
          </div>

          <div class="sticky bottom-0 w-full bg-white">
            <StepSteps steps={5} {step_active} />
          </div>
        </div></StepPanel
      >

      <StepPanel class="h-full w-full pt-28 md:pt-10">
        <div class="flex h-full flex-col justify-between">
          <div
            class="scroll-body mx-auto flex max-h-full w-full max-w-[360px] flex-col items-center justify-start gap-8 overflow-auto px-4"
          >
            <Logo alt={false} />

            <div class="grid gap-3 text-center">
              <Title>Conviction status</Title>
              <Text class="text-base font-normal text-[#475467]"
                >Provide your conviction status.</Text
              >
            </div>

            <div class="grid gap-6 text-center">
              <div class="grid gap-5">
                <Text class="text-start text-base font-normal text-[#475467]"
                  >I declare that I have NO convictions or current charges under
                  my Local Criminal Code up to and including the date of this
                  declaration including any pardons which may pose a threat to
                  the vulnerable population which seeks services of
                  LearnYourWay.ai *</Text
                >
                <div class="grid gap-1.5">
                  <CheckBox
                    class="text-md text-gray-500"
                    text="Confirm"
                    bind:checked={tutorForm.clean_convicted}
                  />
                </div>
              </div>

              <Button
                variant="primary"
                class=" flex w-full justify-center"
                onClick={handleStatusActive}
              >
                Continue
              </Button>
            </div>
          </div>
          <StepSteps steps={5} {step_active} />
        </div>
      </StepPanel>

      <StepPanel class="h-full pt-28 md:pt-10">
        <div class="flex h-full flex-col justify-between">
          <div
            class="scroll-body mx-auto flex max-h-full w-full max-w-[360px] flex-col items-center justify-start gap-8 overflow-auto px-4"
          >
            <Logo alt={false} />

            <div class="grid gap-3 text-center">
              <Title>Pricing</Title>
              <Text class="text-base font-normal text-[#475467]"
                >Please learn about our pricing scheme.</Text
              >
            </div>

            <div>
              <img src="/money_background_figma.png" alt="" />
            </div>

            <div class="grid gap-6">
              <div class="grid gap-5">
                <Text class="text-base font-normal text-[#475467]"
                  >Based on your profile, we recommend that you opt-in to the
                  following pricing scheme to ensure you get a maximum number of
                  students.
                </Text>
                <Text class="text-base font-normal text-[#475467]">
                  <span class="font-bold">Online:</span>
                  15 AED per hour + up to 13 AED per hour in bonuses.

                  <br />

                  <span class="font-bold">In-Person:</span>
                  20 AED per hour + up to 13 AED per hour in bonuses.
                </Text>

                <div class="grid gap-2.5">
                  <Text class="text-sm font-medium text-[#344054]"
                    >Are you willing to opt into the prices mentioned above?*
                  </Text>

                  <Radiobox
                    class="font-medium text-[#344054]"
                    text="Yes"
                    value="yes"
                    isSelected={selectedRadioButtonValues.pricing === "yes"}
                    on:select={(e) => handleSelect("pricing", e)}
                  />
                  <Radiobox
                    class="font-medium text-[#344054]"
                    text="No"
                    value="no"
                    isSelected={selectedRadioButtonValues.pricing === "no"}
                    on:select={(e) => handleSelect("pricing", e)}
                  />
                </div>
              </div>

              {#if selectedRadioButtonValues.pricing === "no"}
                <div class="flex flex-col justify-center gap-1 py-2">
                  <Input
                    inputClass="placeholder:text-[#667085] placeholder:font-normal placeholder:text-base"
                    class="w-full max-w-[360px]"
                    bind:value={pricingForm.price}
                    label=""
                    name=""
                  />
                  <Text class="text-left text-sm font-normal text-[#475467]"
                    >Please type in the preferred pricing</Text
                  >
                </div>
              {/if}

              <Button
                variant="primary"
                class=" flex w-full justify-center"
                onClick={handlePricingActive}
              >
                Continue
              </Button>
            </div>
          </div>
          <StepSteps steps={5} {step_active} />
        </div>
      </StepPanel>

      <StepPanel class="h-full pt-28 md:pt-10">
        <div class="flex h-full flex-col justify-between">
          <div
            class="scroll-body mx-auto flex max-h-full w-full flex-col items-center justify-start gap-8 overflow-auto px-4"
          >
            <Logo alt={false} />

            <div class="grid gap-3 text-center">
              <Title>Required documents</Title>
              <Text class="text-base font-normal text-[#475467]"
                >Upload required documents.</Text
              >
            </div>

            <div class="gap-24 md:flex">
              <div class="grid max-w-[360px] gap-6">
                <div class="grid gap-3">
                  <Text class="text-sm font-medium text-[#344054]"
                    >Upload your CV*</Text
                  >
                  <FileUpload
                    onSelect={async (file) => {
                      let form = new FormData();

                      form.append("file", file);

                      const fileRes = await fetch(
                        "/api/file-upload?/fileUpload",
                        {
                          method: "POST",
                          body: form,
                        },
                      );

                      const fileResData = deserialize(await fileRes.text());

                      if (!validateApiResponse(fileResData)) {
                        showToaster("There was a problem uploading the file");
                        return;
                      }

                      application.cv_files = fileResData.data;
                    }}
                    value={application.cv_files}
                    fileTitle={false}
                  />
                </div>
                <div class="grid gap-3">
                  <Text class="text-sm font-medium text-[#344054]"
                    >Upload your ID*</Text
                  >

                  <FileUpload
                    onSelect={async (file) => {
                      let form = new FormData();

                      form.append("file", file);

                      const fileRes = await fetch(
                        "/api/file-upload?/fileUpload",
                        {
                          method: "POST",
                          body: form,
                        },
                      );

                      const fileResData = deserialize(await fileRes.text());

                      if (!validateApiResponse(fileResData)) {
                        showToaster("There was a problem uploading the file");
                        return;
                      }

                      application.id_files = fileResData.data;
                    }}
                    value={application.id_files}
                    fileTitle={false}
                  />

                  <Paragraph
                    class=" max-w-[360px] text-sm font-normal text-[#475467]"
                  >
                    ID: Passport or Driving license with an Adult Picture of you
                  </Paragraph>
                </div>

                <div class="grid gap-3">
                  <Text class="text-sm font-medium text-[#344054]"
                    >Upload your university transcripts or proof of experience
                    (if professional tutor)*</Text
                  >

                  <FileUpload
                    onSelect={async (file) => {
                      let form = new FormData();

                      form.append("file", file);

                      const fileRes = await fetch(
                        "/api/file-upload?/fileUpload",
                        {
                          method: "POST",
                          body: form,
                        },
                      );

                      const fileResData = deserialize(await fileRes.text());

                      if (!validateApiResponse(fileResData)) {
                        showToaster("There was a problem uploading the file");
                        return;
                      }

                      application.proof_of_exp = fileResData.data;
                    }}
                    value={application.proof_of_exp}
                    fileTitle={false}
                  />

                  <Paragraph
                    class=" max-w-[360px] text-sm font-normal text-[#475467]"
                  >
                    If you are applying as a Peer Tutor, please upload both your
                    School and University Transcripts. If you are already a
                    School / University Tutor, please upload your Proof of
                    Experience.
                  </Paragraph>
                </div>
              </div>

              <div class="mt-6 flex max-w-[360px] flex-col gap-6 md:mt-0">
                <div class="grid gap-3">
                  <Text class="text-sm font-medium text-[#344054]"
                    >Upload your police clearance</Text
                  >
                  <FileUpload
                    onSelect={async (file) => {
                      let form = new FormData();

                      form.append("file", file);

                      const fileRes = await fetch(
                        "/api/file-upload?/fileUpload",
                        {
                          method: "POST",
                          body: form,
                        },
                      );

                      const fileResData = deserialize(await fileRes.text());

                      if (!validateApiResponse(fileResData)) {
                        showToaster("There was a problem uploading the file");
                        return;
                      }

                      application.police_clearence = fileResData.data;
                    }}
                    value={application.police_clearence}
                    fileTitle={false}
                  />
                </div>

                <div class="grid gap-3">
                  <Text class="text-sm font-medium text-[#344054]"
                    >Private Teacher Work Permit (Only if you reside in the UAE)
                    (Optional)</Text
                  >
                  <FileUpload
                    onSelect={async (file) => {
                      let form = new FormData();

                      form.append("file", file);

                      const fileRes = await fetch(
                        "/api/file-upload?/fileUpload",
                        {
                          method: "POST",
                          body: form,
                        },
                      );

                      const fileResData = deserialize(await fileRes.text());

                      if (!validateApiResponse(fileResData)) {
                        showToaster("There was a problem uploading the file");
                        return;
                      }

                      application.tutor_work_permit = fileResData.data;
                    }}
                    value={application.tutor_work_permit}
                    fileTitle={false}
                  />
                  <Paragraph
                    class=" max-w-[360px] text-sm font-normal text-[#475467]"
                  >
                    The Ministry of Education (MoE) and the Ministry of Human
                    Resources and Emiratisation (MoHRE) have introduced a new
                    FREE license for professional educators, professionals in
                    various sectors, unemployed individuals, and university
                    students to conduct private lessons.This license is valid
                    for two years and is issued free of charge. You can apply
                    for it through the MoHRE's digital platforms, specifically
                    under the 'Private Teacher Work Permit' section in the
                    'Services' tab on their website. As it is mandatory to
                    obtain this license for private tutoring to avoid fines.
                  </Paragraph>
                </div>
              </div>
            </div>
            <Button
              variant="primary"
              class=" mb-4 flex w-full max-w-[360px] justify-center md:mb-10"
              onClick={() => {
                handleApplicationActive();
              }}
            >
              Submit
            </Button>
          </div>
          <StepSteps steps={5} {step_active} />
        </div>
      </StepPanel>
    </StepPanels>
  </div>
</Step>
