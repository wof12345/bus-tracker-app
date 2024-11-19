<script>
  import { clamp } from "yootils";

  export let start = 0;
  export let end = 1;

  let leftHandle;
  let body;
  let slider;

  function draggable(node) {
    let x;
    let y;
    function handleMousedown(event) {
      if (event.type === "touchstart") {
        event = event.touches[0];
      }
      x = event.clientX;
      y = event.clientY;
      node.dispatchEvent(
        new CustomEvent("dragstart", {
          detail: { x, y },
        }),
      );
      window.addEventListener("mousemove", handleMousemove);
      window.addEventListener("mouseup", handleMouseup);
      window.addEventListener("touchmove", handleMousemove);
      window.addEventListener("touchend", handleMouseup);
    }
    function handleMousemove(event) {
      if (event.type === "touchmove") {
        event = event.changedTouches[0];
      }
      const dx = event.clientX - x;
      const dy = event.clientY - y;
      x = event.clientX;
      y = event.clientY;
      node.dispatchEvent(
        new CustomEvent("dragmove", {
          detail: { x, y, dx, dy },
        }),
      );
    }
    function handleMouseup(event) {
      x = event.clientX;
      y = event.clientY;
      node.dispatchEvent(
        new CustomEvent("dragend", {
          detail: { x, y },
        }),
      );
      window.removeEventListener("mousemove", handleMousemove);
      window.removeEventListener("mouseup", handleMouseup);
      window.removeEventListener("touchmove", handleMousemove);
      window.removeEventListener("touchend", handleMouseup);
    }
    node.addEventListener("mousedown", handleMousedown);
    node.addEventListener("touchstart", handleMousedown);
    return {
      destroy() {
        node.removeEventListener("mousedown", handleMousedown);
        node.removeEventListener("touchstart", handleMousedown);
      },
    };
  }
  function setHandlePosition(which) {
    return function (evt) {
      const { left, right } = slider.getBoundingClientRect();
      const parentWidth = right - left;
      const p = Math.min(Math.max((evt.detail.x - left) / parentWidth, 0), 1);
      if (which === "start") {
        start = p;
        end = Math.max(end, p);
      } else {
        start = Math.min(p, start);
        end = p;
      }
    };
  }
  function setHandlesFromBody(evt) {
    const { width } = body.getBoundingClientRect();
    const { left, right } = slider.getBoundingClientRect();
    const parentWidth = right - left;
    const leftHandleLeft = leftHandle.getBoundingClientRect().left;
    const pxStart = clamp(
      leftHandleLeft + event.detail.dx - left,
      0,
      parentWidth - width,
    );
    const pxEnd = clamp(pxStart + width, width, parentWidth);
    const pStart = pxStart / parentWidth;
    const pEnd = pxEnd / parentWidth;
    start = pStart;
    end = pEnd;
  }

  const nice = (d) => {
    if (!d && d !== 0) return "";
    return d.toFixed(2);
  };
</script>

<div class=" pb-8 pt-5 px-12 flex flex-col items-center gap-4 w-full">
  <div
    class="flex items-center justify-center text-center gap-2.5 w-full max-w-[185px]"
  >
    <div class="w-full text-[#101828] font-bold text-sm flex gap-1 items-end">
      <h6 class="mb-[3px]">AED</h6>
      <p class="text-lg">{nice(start)}</p>
    </div>

    <p>-</p>

    <div class="w-full text-[#101828] font-bold text-sm flex gap-1 items-end">
      <h6 class="mb-[3px]">AED</h6>
      <p class="text-lg">{nice(end)}</p>
    </div>
  </div>

  <div class="double-range-container">
    <div class="slider" bind:this={slider}>
      <div
        class="body"
        bind:this={body}
        use:draggable
        on:dragmove|preventDefault|stopPropagation={setHandlesFromBody}
        style="
          left: {100 * start}%;
          right: {100 * (1 - end)}%;
        "
      ></div>
      <div
        class="handle ring-black ring-4"
        bind:this={leftHandle}
        data-which="start"
        use:draggable
        on:dragmove|preventDefault|stopPropagation={setHandlePosition("start")}
        style="
          left: {100 * start}%
        "
      ></div>
      <div
        class="handle ring-black ring-4"
        data-which="end"
        use:draggable
        on:dragmove|preventDefault|stopPropagation={setHandlePosition("end")}
        style="
          left: {100 * end}%
        "
      ></div>
    </div>
  </div>
</div>

<style>
  .double-range-container {
    width: 100%;
    height: 20px;
    user-select: none;
    box-sizing: border-box;
    white-space: nowrap;
  }
  .slider {
    position: relative;
    width: 100%;
    height: 8px;
    top: 50%;
    transform: translate(0, -50%);
    background-color: #eaecf0;
    /* box-shadow:
      inset 0 7px 10px -5px #4a4a4a,
      inset 0 -1px 0px 0px #9c9c9c; */
    border-radius: 50px;
  }
  .handle {
    position: absolute;
    top: 50%;
    width: 0;
    height: 0;
  }
  .handle:after {
    content: " ";
    box-sizing: border-box;
    position: absolute;
    border-radius: 50%;
    width: 24px;
    height: 24px;
    background-color: #fdfdfd;
    border: 2px solid #7f56d9;
    transform: translate(-50%, -50%);
  }
  /* .handle[data-which="end"]:after{
		transform: translate(-100%, -50%);
	} */
  .handle:active:after {
    z-index: 9;
    box-shadow: var(--tw-ring-inset) 0 0 0
      calc(4px + var(--tw-ring-offset-width)) var(--tw-ring-color);
    --tw-ring-color: rgb(231, 221, 250);
  }
  .body {
    top: 0;
    position: absolute;
    background-color: #7f56d9;
    bottom: 0;
  }
</style>
