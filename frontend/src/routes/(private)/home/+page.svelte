<script>
  import Section from "$components/Base/Layout/Section.svelte";
  import Tab from "$components/Base/Tab/Tab.svelte";
  import TabBody from "$components/Base/Tab/TabBody.svelte";
  import TabPanel from "$components/Base/Tab/TabPanel.svelte";
  import Table from "$components/Base/Table/Table.svelte";
  import TableHeaderRow from "$components/Base/Table/TableHeaderRow.svelte";
  import TableBodyHeader from "$components/Base/Table/TableBodyHeader.svelte";
  import TableBody from "$components/Base/Table/TableBody.svelte";
  import TableRow from "$components/Base/Table/TableRow.svelte";
  import TableCell from "$components/Base/Table/TableCell.svelte";
  import TableFooter from "$components/Base/Table/TableFooter.svelte";
  import TableFrame from "$components/Base/Table/TableFrame.svelte";
  import Pagination from "$components/Base/Table/Components/Pagination.svelte";

  import { onMount } from "svelte";
  import dayjs from "dayjs";

  export let data;

  $: tutorPayouts = data?.payouts;
</script>

<Section class="flex flex-col gap-0 h-full">
  <div class="flex items-start justify-between">
    <div class="w-full">
      <h1 class="font-semibold text-[#101828] text-3xl">Payouts</h1>
      <p class="font-normal text-[#475467] text-base mt-1">
        Manage your payouts efficiently.
      </p>
    </div>
  </div>

  <Tab class="mt-6">
    <TabBody>
      <TabPanel>
        <Table>
          <TableFrame>
            <TableBody>
              <TableHeaderRow>
                <TableBodyHeader class="col-span-1">Date</TableBodyHeader>
                <TableBodyHeader class="col-span-1">Amount</TableBodyHeader>
              </TableHeaderRow>

              {#each tutorPayouts?.data || [] as item}
                <TableRow class="items-center ">
                  <TableCell
                    class="col-span-1 flex gap-3 font-normal text-sm text-[#475467]"
                    >{dayjs(item?.created_at).format("MMM DD, YYYY")}</TableCell
                  >
                  <TableCell
                    class="col-span-1 flex gap-3 font-normal text-sm text-[#475467]"
                    >{item?.amount}</TableCell
                  >
                </TableRow>
              {/each}
            </TableBody>
          </TableFrame>
          <TableFooter>
            <Pagination
              totalItems={tutorPayouts?.total || 0}
              onPageChange={() => {}}
            />
          </TableFooter>
        </Table>
      </TabPanel>
    </TabBody>
  </Tab>
</Section>
