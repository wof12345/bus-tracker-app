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

    // Draw the current frame from the video onto the main canvas
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
      const plate = licensePlatePredictions[0];
      const x = plate.bbox[0];
      const y = plate.bbox[1];
      const width = plate.bbox[2];
      const height = plate.bbox[3];

      // Cropping the license plate region from the main canvas
      const croppedImage = context.getImageData(x, y, width, height);

      // Disable image smoothing to avoid blurring
      const tempContext = canvasCroppedElement.getContext("2d");
      tempContext.imageSmoothingEnabled = false; // Disable interpolation/smoothing

      // Set canvas size to match the cropped image's size
      canvasCroppedElement.width = width;
      canvasCroppedElement.height = height;

      // Draw the cropped image onto the second canvas without resizing
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

  function enhanceImage(context, width, height) {
    // Get the pixel data from the canvas
    const imageData = context.getImageData(0, 0, width, height);
    const data = imageData.data;

    // Convert to grayscale
    for (let i = 0; i < data.length; i += 4) {
      const red = data[i];
      const green = data[i + 1];
      const blue = data[i + 2];

      // Average of RGB values
      const grayscale = (red + green + blue) / 3;

      data[i] = data[i + 1] = data[i + 2] = grayscale; // Set all to grayscale
    }

    // Adjust contrast and brightness
    const contrast = 1.2; // Increase contrast (1.0 = no change)
    const brightness = 20; // Increase brightness (+/- value)

    for (let i = 0; i < data.length; i += 4) {
      // Apply contrast
      data[i] = (data[i] - 128) * contrast + 128; // Red
      data[i + 1] = (data[i + 1] - 128) * contrast + 128; // Green
      data[i + 2] = (data[i + 2] - 128) * contrast + 128; // Blue

      // Apply brightness
      data[i] = data[i] + brightness; // Red
      data[i + 1] = data[i + 1] + brightness; // Green
      data[i + 2] = data[i + 2] + brightness; // Blue
    }

    // Put the modified image data back onto the canvas
    context.putImageData(imageData, 0, 0);
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
