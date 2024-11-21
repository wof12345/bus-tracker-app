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

  $: tutorPayouts = data?.payouts;
</script>

<Section class="flex flex-col gap-0 h-full">
  <TableHeader class="mb-3" title="Home" subtitle="Current app statistics" />

  <div class="grid grid-cols-3 gap-3">
    <Card>
      <Container class="justify-between">
        <Paragraph class="font-medium md:text-sm">Total Bus</Paragraph>
        <div>
          <IconHighlight class="text-gray-400" />
        </div>
      </Container>

      <Header class="flex items-center gap-2 md:text-3xl">
        <CountingAnimation number={100} />
      </Header>
    </Card>

    <Card>
      <Container class="justify-between">
        <Paragraph class="font-medium md:text-sm">Male Bus</Paragraph>
        <div>
          <IconHighlight class="text-gray-400" />
        </div>
      </Container>

      <Header class="flex items-center gap-2 md:text-3xl">
        <CountingAnimation number={100} />
      </Header>
    </Card>

    <Card>
      <Container class="justify-between">
        <Paragraph class="font-medium md:text-sm">Female Bus</Paragraph>
        <div>
          <IconHighlight class="text-gray-400" />
        </div>
      </Container>

      <Header class="flex items-center gap-2 md:text-3xl">
        <CountingAnimation number={100} />
      </Header>
    </Card>

    <Card>
      <Container class="justify-between">
        <Paragraph class="font-medium md:text-sm">Teacher Bus</Paragraph>
        <div>
          <IconHighlight class="text-gray-400" />
        </div>
      </Container>

      <Header class="flex items-center gap-2 md:text-3xl">
        <CountingAnimation number={100} />
      </Header>
    </Card>

    <Card>
      <Container class="justify-between">
        <Paragraph class="font-medium md:text-sm">Eployee Bus</Paragraph>
        <div>
          <IconHighlight class="text-gray-400" />
        </div>
      </Container>

      <Header class="flex items-center gap-2 md:text-3xl">
        <CountingAnimation number={100} />
      </Header>
    </Card>
  </div>
</Section>
