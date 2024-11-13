<script>
  import { IconStar } from "@tabler/icons-svelte";

  export let rating = 0;
  export let blanksrc = "/starIcon.svg";
  export let filledsrc = "/starfillIcon.svg";
  export let star = 0;
  export let maxRating = 5;
  export let onRate = () => {};

  export let disabled = false;

  const setRating = (value) => {
    rating = value;
    onRate(rating);
  };
</script>

<div class="flex items-center gap-1">
  {#each Array(maxRating) as _, index}
    {#if !disabled}
      <button
        class:star
        class:filled={index < rating}
        on:click={() => setRating(index + 1)}
      >
        <img src={index < rating ? filledsrc : blanksrc} alt="" />
      </button>
    {:else}
      <button
        class="cursor-not-allowed"
        class:star
        class:filled={index < rating}
      >
        <img src={index < rating ? filledsrc : blanksrc} alt="" />
      </button>
    {/if}
  {/each}
</div>

<style>
  .star {
    cursor: pointer;
    font-size: 2rem;
    color: gray;
  }
  .star.filled {
    color: gold;
  }
</style>
