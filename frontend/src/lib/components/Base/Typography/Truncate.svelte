<script>
  function truncateText(text, maxLength) {
    if (text.length <= maxLength) {
      return text;
    }
    return text.substring(0, maxLength) + "...";
  }

  // Example usage:
  const originalText =
    "This is a long piece of text that needs to be truncated.";
  const maxLength = 20;
  const truncatedText = truncateText(originalText, maxLength);
</script>

<div>truncate</div>
