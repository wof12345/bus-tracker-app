<script>
  import Section from "$components/Base/Layout/Section.svelte";
  import Tab from "$components/Base/Tab/Tab.svelte";
  import TabBody from "$components/Base/Tab/TabBody.svelte";
  import TabHeader from "$components/Base/Tab/TabHeader.svelte";
  import TabPanel from "$components/Base/Tab/TabPanel.svelte";
  import TabHeaders from "$components/Base/Tab/TabHeaders.svelte";
  import Table from "$components/Base/Table/Table.svelte";
  import TableHeaderRow from "$components/Base/Table/TableHeaderRow.svelte";
  import TableBodyHeader from "$components/Base/Table/TableBodyHeader.svelte";
  import TableBody from "$components/Base/Table/TableBody.svelte";
  import TableRow from "$components/Base/Table/TableRow.svelte";
  import TableCell from "$components/Base/Table/TableCell.svelte";
  import TableFooter from "$components/Base/Table/TableFooter.svelte";
  import TableFrame from "$components/Base/Table/TableFrame.svelte";
  import Pagination from "$components/Base/Table/Components/Pagination.svelte";
  import trialLesson from "$lib/data/transaction_data.json";
  import Modal from "$components/Base/Modal/Modal.svelte";
  import ModalHeader from "$components/Base/Modal/ModalHeader.svelte";
  import ModalBody from "$components/Base/Modal/ModalBody.svelte";
  import Paragraph from "$components/Base/Typography/Paragraph.svelte";
  import Button from "$components/Base/Buttons/Button.svelte";
  import ModalFooter from "$components/Base/Modal/ModalFooter.svelte";
  import Input from "$components/Base/Forms/Inputs/Input.svelte";
  import Text from "$components/Base/Typography/Text.svelte";
  import DropDown from "$components/Base/Forms/Inputs/DropDown.svelte";

  let payoutModal;
</script>

<Section class="flex flex-col gap-0">
  <div class="w-full">
    <h1 class="font-semibold text-[#101828] text-3xl">John Doe</h1>
    <p class="font-normal text-[#475467] text-base mt-1">
      View the details of John Doe.
    </p>
  </div>

  <Tab class="mt-6">
    <TabHeaders>
      <TabHeader>Payout info</TabHeader>
      <TabHeader>Payout history</TabHeader>
      <TabHeader>Tutor’s details</TabHeader>
    </TabHeaders>

    <TabBody>
      <TabPanel>
        <div
          class="w-full mx-auto flex flex-col items-center md:gap-4 gap-2 mt-6"
        >
          <div
            class="md:flex md:gap-8 grid gap-1 md:border-b md:pb-4 w-full max-w-[520px]"
          >
            <Text class="text-[#344054] font-medium text-sm w-full"
              >Bank Name</Text
            >
            <Paragraph class="text-[#475467] w-full"
              >Commercial Bank of Dubai</Paragraph
            >
          </div>

          <div
            class="md:flex md:gap-8 grid gap-1 md:border-b md:pb-4 w-full max-w-[520px]"
          >
            <Text class="text-[#344054] font-medium text-sm w-full">Branch</Text
            >
            <Paragraph class="text-[#475467] w-full">Branch</Paragraph>
          </div>

          <div
            class="md:flex md:gap-8 grid gap-1 md:border-b md:pb-4 w-full max-w-[520px]"
          >
            <Text class="text-[#344054] font-medium text-sm w-full"
              >Account name</Text
            >
            <Paragraph class="text-[#475467] w-full"
              >P.O.Box # 2466, Abu Dhabi, U.A.E</Paragraph
            >
          </div>
          <div
            class="md:flex md:gap-8 grid gap-1 md:border-b md:pb-4 w-full max-w-[520px]"
          >
            <Text class="text-[#344054] font-medium text-sm w-full"
              >Account number</Text
            >
            <Paragraph class="text-[#475467] w-full">John Doe</Paragraph>
          </div>
          <div
            class="md:flex md:gap-8 grid gap-1 md:border-b md:pb-4 w-full max-w-[520px]"
          >
            <Text class="text-[#344054] font-medium text-sm w-full"
              >IBAN No</Text
            >
            <Paragraph class="text-[#475467] w-full">100 200 4000</Paragraph>
          </div>
          <div
            class="md:flex md:gap-8 grid gap-1 md:border-b md:pb-4 w-full max-w-[520px]"
          >
            <Text class="text-[#344054] font-medium text-sm w-full"
              >Swift code</Text
            >
            <Paragraph class="text-[#475467] w-full"
              >AE2536542364353463434</Paragraph
            >
          </div>
        </div>
      </TabPanel>

      <TabPanel>
        <Table>
          <TableFrame>
            <TableBody>
              <TableHeaderRow>
                <TableBodyHeader class="col-span-1">Date</TableBodyHeader>
                <TableBodyHeader class="col-span-1">Time</TableBodyHeader>
                <TableBodyHeader class="col-span-1">Amount</TableBodyHeader>
              </TableHeaderRow>

              {#each trialLesson as item}
                <TableRow class="items-center ">
                  <TableCell
                    class="col-span-1 flex gap-3 font-normal text-sm text-[#475467]"
                    >{item.date}</TableCell
                  >
                  <TableCell
                    class="col-span-1 flex gap-3 font-normal text-sm text-[#475467]"
                    >{item.time}</TableCell
                  >
                  <TableCell
                    class="col-span-1 flex gap-3 font-normal text-sm text-[#475467]"
                    >{item.amount}</TableCell
                  >
                </TableRow>
              {/each}
            </TableBody>
          </TableFrame>
          <TableFooter>
            <Pagination totalItems={4} onPageChange={() => {}} />
          </TableFooter>
        </Table>
      </TabPanel>

      <TabPanel>
        <div class="w-full mx-auto flex flex-col items-center gap-4 mt-6">
          <div
            class="md:flex md:gap-8 grid gap-1 md:border-b md:pb-4 w-full max-w-[520px]"
          >
            <Text
              class="text-[#344054] font-medium text-sm w-full max-w-[120px]"
              >Name</Text
            >
            <Paragraph class="text-[#475467] w-full">John Doe</Paragraph>
          </div>

          <div
            class="md:flex md:gap-8 grid gap-1 md:border-b md:pb-4 w-full max-w-[520px]"
          >
            <Text
              class="text-[#344054] font-medium text-sm w-full max-w-[120px]"
              >Email</Text
            >
            <Paragraph class="text-[#475467] w-full"
              >johndoe@example.com</Paragraph
            >
          </div>

          <div
            class="md:flex md:gap-8 grid gap-1 md:border-b md:pb-4 w-full max-w-[520px]"
          >
            <Text
              class="text-[#344054] font-medium text-sm w-full max-w-[120px]"
              >Phone</Text
            >
            <Paragraph class="text-[#475467] w-full">+971-50-1234567</Paragraph>
          </div>

          <div
            class="md:flex md:gap-8 grid gap-1 md:border-b md:pb-4 w-full max-w-[520px]"
          >
            <Text
              class="text-[#344054] font-medium text-sm w-full max-w-[120px]"
              >Gender</Text
            >
            <Paragraph class="text-[#475467] w-full">Male</Paragraph>
          </div>

          <div
            class="md:flex md:gap-8 grid gap-1 md:border-b md:pb-4 w-full max-w-[520px]"
          >
            <Text
              class="text-[#344054] font-medium text-sm w-full max-w-[120px]"
              >Birth date</Text
            >
            <Paragraph class="text-[#475467] w-full">12/12/1990</Paragraph>
          </div>

          <div
            class="md:flex md:gap-8 grid gap-1 md:border-b md:pb-4 w-full max-w-[520px]"
          >
            <Text
              class="text-[#344054] font-medium text-sm w-full max-w-[120px]"
              >Location</Text
            >
            <Paragraph class="text-[#475467] w-full"
              >Dubai Marina, Dubai, United Arab Emirates</Paragraph
            >
          </div>

          <div class="md:flex md:gap-8 grid gap-1 md:pb-4 w-full max-w-[520px]">
            <Text
              class="text-[#344054] font-medium text-sm w-full max-w-[120px]"
              >Photo</Text
            >
            <div class="w-[120px] h-[120px] bg-gray-200">
              <img src="/tutors.svg" alt="" />
            </div>
          </div>
        </div>
      </TabPanel>
    </TabBody>
  </Tab>

  <Modal bind:this={payoutModal} class="h-auto mx-6 max-h-[80vh] max-w-[400px]">
    <ModalHeader class="border-b-0">
      <img src="/flagIcon.svg" alt="" />
      <div class="space-y-1">
        <Paragraph class="font-semibold text-[18px] mt-4"
          >Add a payout record</Paragraph
        >

        <Paragraph class="text-[#475467] text-sm">
          Insert amount and select tutor to create a new payout record.
        </Paragraph>
      </div>
    </ModalHeader>

    <ModalBody class="space-y-5">
      <div class=" w-full space-y-2">
        <Text class="text-left text-sm font-medium text-[#344054]">Amount</Text>
        <Input
          inputClass="placeholder:text-[#667085] placeholder:font-normal placeholder:text-base"
          class="w-full max-w-[360px]"
          label="Enter amount"
          name="last_name"
        />
      </div>
      <div class=" w-full space-y-2">
        <Text class="text-left text-sm font-medium text-[#344054]">Amount</Text>
        <DropDown
          class="text-base font-normal text-[#667085]"
          label="Select tutor"
        >
          <img src="/tutor.svg" alt="" />
        </DropDown>
      </div>
    </ModalBody>

    <ModalFooter class="border-t-0">
      <div
        class="md:flex flex-nowrap gap-2 space-y-3 md:space-y-0 justify-center mt-[-15px] md:mt-0 w-full relative pb-[55px] md:pb-0"
      >
        <Button
          onClick={() => payoutModal.hide()}
          class="w-full md:static absolute bottom-0 "
          variant={"secondary"}>Cancel</Button
        >
        <Button class="w-full  ">Done</Button>
      </div>
    </ModalFooter>
  </Modal>
</Section>
