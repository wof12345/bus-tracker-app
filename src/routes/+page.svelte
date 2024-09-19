<script>
  import { onMount } from "svelte";
  import * as cocoSsd from "@tensorflow-models/coco-ssd";
  import * as tf from "@tensorflow/tfjs";
  import Tesseract from "tesseract.js";

  let videoElement;
  let canvasElement;
  let canvasCroppedElement;
  let detectedText = "";
  let isProcessing = false;
  let model;
  let imageData;

  function handleVideoUpload(event) {
    const file = event.target.files[0];
    if (file) {
      const videoURL = URL.createObjectURL(file);
      videoElement.src = videoURL;
      videoElement.load();
    }
  }

  async function captureFrame() {
    if (isProcessing || !model) return;
    isProcessing = true;

    const context = canvasElement.getContext("2d");
    context.drawImage(
      videoElement,
      0,
      0,
      canvasElement.width,
      canvasElement.height
    );

    const imgData = tf.browser.fromPixels(canvasElement);

    let predictions;

    try {
      predictions = await model.detect(canvasElement);
    } catch (error) {
      console.log(error);
    }

    if (!predictions) return;

    const licensePlatePredictions = predictions.filter(
      (prediction) => prediction.class === "car"
    );

    if (licensePlatePredictions.length > 0) {
      console.log(`found ${licensePlatePredictions.length} cars`);

      const plate = licensePlatePredictions[0];

      const x = plate.bbox[0];
      const y = plate.bbox[1];
      const width = plate.bbox[2];
      const height = plate.bbox[3];

      console.log(plate, "plate");
      // Cropping the license plate region from the main canvas
      const croppedImage = context.getImageData(x, y, width, height);

      // Resize the cropped canvas to match the cropped license plate size
      canvasCroppedElement.width = width;
      canvasCroppedElement.height = height;

      // Get the context of the second canvas and draw the cropped image
      let tempContext = canvasCroppedElement.getContext("2d");
      tempContext.putImageData(croppedImage, 0, 0);

      // Convert the cropped canvas content to a data URL
      imageData = canvasCroppedElement.toDataURL("image/png");

      try {
        const result = await Tesseract.recognize(imageData, "eng");
        detectedText = result.data.text.trim();
        console.log(detectedText);
      } catch (error) {
        console.error(error);
      }
    } else {
      console.log("No license plates detected");
    }

    isProcessing = false;
  }

  onMount(async () => {
    model = await cocoSsd.load();

    setInterval(() => {
      if (!videoElement || !canvasElement) return;

      console.log("called");
      captureFrame();
    }, 5000);
  });
</script>

<main>
  <!-- Video Upload -->
  <input type="file" accept="video/*" on:change={handleVideoUpload} />

  <!-- Video Preview -->
  <video bind:this={videoElement} controls></video>

  <!-- Main Canvas for Frame Capture -->
  <canvas bind:this={canvasElement} width="500" height="300"></canvas>

  <!-- Cropped Canvas for Displaying the Detected Region -->
  <canvas bind:this={canvasCroppedElement}></canvas>

  {#if detectedText}
    <div class="detected-text">Detected Text: {detectedText}</div>
  {/if}

  <!-- Display Cropped Image as an Optional Preview -->
  {#if imageData}
    <img src={imageData} alt="Cropped Image" />
  {/if}
</main>

<style>
  video,
  canvas {
    width: 100%;
    max-width: 500px;
  }
  .detected-text {
    margin-top: 10px;
    font-weight: bold;
  }
</style>
