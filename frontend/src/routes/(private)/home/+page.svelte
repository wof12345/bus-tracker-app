<script>
  import Section from "$components/Base/Layout/Section.svelte";

  import Card from "$components/Base/Card.svelte";
  import Paragraph from "$components/Base/Typography/Paragraph.svelte";
  import Container from "$components/Base/Layout/Container.svelte";
  import Header from "$components/Base/Typography/Header.svelte";
  import CountingAnimation from "$components/Animated/CountingAnimation.svelte";
  import TableHeader from "$components/Tables/Components/TableHeader.svelte";
  import { IconHighlight } from "@tabler/icons-svelte";

  export let data;

  $: console.log(data);

  $: statistics = data?.statistics;
</script>

<Section class="flex flex-col gap-0 h-full">
  <TableHeader class="mb-3" title="Home" subtitle="Current app statistics" />

  <div class="grid grid-cols-3 gap-3">
    {#if statistics}
      {#each Object.keys(statistics) as stat}
        <Card>
          <Container class="justify-between">
            <Paragraph class="font-medium md:text-sm">{stat} Bus</Paragraph>
            <div>
              <IconHighlight class="text-gray-400" />
            </div>
          </Container>

          <Header class="flex items-center gap-2 md:text-3xl">
            <CountingAnimation number={statistics[stat]} />
          </Header>
        </Card>
      {/each}
    {/if}
  </div>
</Section>
