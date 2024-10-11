<script>
  let videoElement;
  let processedFrameSrc = "";

  // Start the video stream from the webcam
  async function startVideoStream() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoElement.srcObject = stream;
    } catch (err) {
      console.error("Error accessing webcam:", err);
    }
  }

  // Capture the current video frame and send it to the FastAPI server
  async function captureAndSendFrame() {
    const canvas = document.createElement("canvas");
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;

    const context = canvas.getContext("2d");
    context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

    // Convert canvas content to Blob
    canvas.toBlob(async (blob) => {
      const formData = new FormData();
      formData.append("file", blob, "frame.jpg");

      // Send the frame to the FastAPI endpoint
      const response = await fetch("http://localhost:8000/process-frame", {
        method: "POST",
        body: formData,
      });

      // Get the processed frame back and display it
      const processedBlob = await response.blob();
      processedFrameSrc = URL.createObjectURL(processedBlob);
    }, "image/jpeg");
  }

  // Start streaming frames every second
  function startFrameStreaming() {
    setInterval(captureAndSendFrame, 1000); // Capture and send frame every second
  }
</script>

<main>
  <!-- Video Element -->
  <video bind:this={videoElement} autoplay></video>

  <!-- Start Streaming Button -->
  <button on:click={startFrameStreaming}>Start Streaming</button>

  <!-- Display Processed Frame -->
  {#if processedFrameSrc}
    <img src={processedFrameSrc} alt="Processed frame" />
  {/if}
</main>

<style>
  video,
  img {
    max-width: 100%;
    height: auto;
  }

  button {
    margin-top: 10px;
  }
</style>
