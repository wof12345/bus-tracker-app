import { LatLng } from "leaflet";
import { calculateEuclideanDistance } from "./math";

export default class Map {
    constructor(
        mapElement,
        mapData,
        imageData,
        update = () => { },
        resetMode,
        updateData,
        onActive,
        onItemActive,
        onRemove,
        popupContent,
        onMapClick = () => { },
        onMarkerAdd = () => { }
    ) {
        this.map = null;
        this.leaflet = null;
        this.image = null;
        this.mapElement = mapElement;

        this.imageData = imageData;
        this.mapData = mapData;

        this.mode = "";

        this.capture = false;
        this.line = [];
        this.lineVisual = [];
        this.tempLines = [];
        this.lastGeomVisual = null;

        this.activeMarkerID = 0;
        this.active = 0;

        this.update = update;
        this.globalActiveKey = "";

        this.resetMode = resetMode;
        this.updateData = updateData;
        this.onActive = onActive;
        this.onItemActive = onItemActive;
        this.onRemove = onRemove;

        this.popupContent = popupContent;
        this.showPopup = false;
        this.lastPopUpMarker = null;

        this.onMapClick = onMapClick
        this.onMarkerAdd = onMarkerAdd

        this._init();
    }

    async _init() {
        this.leaflet = await import("leaflet");

        this.map = this.leaflet.map(this.mapElement, {
            maxZoom: 5,
            minZoom: -2,
            crs: this.leaflet.CRS.Simple,
            attributionControl: false,
            scrollWheelZoom: true,
            center: this.center,
            zoomAnimation: true,
            fadeAnimation: true,
            markerZoomAnimation: false,
            zoomAnimationThreshold: false,
            animate: false,
        });

        this.leaflet.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            maxZoom: 19,
            attribution:
                '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        }).addTo(this.map);


        // this.map.dragging.disable();
        // this.map.scrollWheelZoom.disable();


        this._addKeyEvents();

        this.addEventListenerMap("mousemove", this.mouseMove);
        this.addEventListenerMap("mousedown", this.mouseDown);
        this.addEventListenerMap("mouseup", this.mouseUp);
        this.addEventListenerMap("click", this.mouseClick);

        this.updateData();
    }

    setMode(mode = "") {
        this.mode = mode;
    }

    addEventListenerMap(event, callback) {
        this.map?.on(event, callback.bind(this));
    }

    mouseDown(e) {
        if (this.mode !== "pin") {
            this.capture = true;
        }
    }

    mouseMove(e) {
        if (this.capture) {
            if (this.lastGeomVisual) this.map.removeLayer(this.lastGeomVisual);

            this.line.push(e.latlng);

            if (this.mode === "draw") {
                this.lineVisual.push(this.leaflet?.polyline(this.line).addTo(this.map));
            } else if (this.mode === "circle") {
                let start = this.line[0];
                let end = this.line[this.line.length - 1];
                const radius = calculateEuclideanDistance(
                    start.lat,
                    start.lng,
                    end.lat,
                    end.lng
                );

                this.lastGeomVisual = this.leaflet
                    ?.circle(start, radius)
                    .addTo(this.map);
            } else if (this.mode === "rectangle") {
                let start = this.line[0];
                let end = this.line[this.line.length - 1];

                this.lastGeomVisual = this.leaflet
                    ?.rectangle([start, end])
                    .addTo(this.map);
            } else if (this.mode === "line") {
                let start = this.line[0];
                let end = this.line[this.line.length - 1];
                this.lastGeomVisual = this.leaflet
                    ?.polyline([start, end])
                    .addTo(this.map);
            }
        }
    }

    mouseUp(e) {
        if (this.capture) {
            this.lineVisual.forEach((elm) => {
                this.map.removeLayer(elm);
            });

            if (this.mode === "circle") {
                this.addCircle(
                    this.lastGeomVisual.getLatLng(),
                    false,
                    this.lastGeomVisual.getRadius()
                );
            } else if (this.mode === "rectangle") {
                const bounds = this.lastGeomVisual.getBounds();
                this.addRectangle([bounds.getNorthEast(), bounds.getSouthWest()]);
            } else if (this.mode === "draw") {
                this.addLine(this.line);
            } else if (this.mode === "line") {
                this.addLine(this.lastGeomVisual.getLatLngs());
            }

            if (this.lastGeomVisual) this.map.removeLayer(this.lastGeomVisual);
            this.lastGeomVisual = null;
            this.capture = false;
            this.line = [];
            this.lineVisual = [];
        }
    }

    mouseClick(e) {
        let coordinates = e.latlng;

        if (this.mode == "pin") this.addMarker(coordinates);
        // else if (this.mode == "circle") this.addCircle(coordinates);

        this.onMapClick(e)
    }

    _clipBounds(bounds) {
        let zoom = -1;

        if (bounds[0] > 1000) zoom = -2;

        return zoom;
    }

    _addKeyEvents() {
        document.addEventListener("keydown", (e) => {
            this.globalActiveKey = e.key;

            if (this.globalActiveKey == "z") {
                e.preventDefault();
                this.map.scrollWheelZoom.enable();
            }

            if (this.globalActiveKey == "Alt") {
                this.map.dragging.enable();
            }
        });

        document.addEventListener("keyup", (e) => {
            this.globalActiveKey = "";

            this.map.dragging.disable();
            this.map.scrollWheelZoom.disable();
        });
    }

    changeContext(work) {
        this.removeAllMarkers();

        this.active = work.id;

        this.updateData([[], []]);

        this.populateMarkers(work);

        this.updateData();
    }

    imageOverlay(imageUrl, bounds) {
        if (this.image) this.map.removeLayer(this.image);

        if (bounds) {
            let zoom = this._clipBounds(bounds);

            let calclulatedBounds = new LatLng(bounds[0] / 2, bounds[1] / 2);

            this.map?.setView(calclulatedBounds, zoom);

            var imageBounds = [new LatLng(bounds[0], 0), new LatLng(0, bounds[1])];

            this.image = this.leaflet?.imageOverlay(imageUrl, imageBounds);

            this.image.addTo(this.map);
        }
        return this.image;
    }

    _updateSerial() {
        this.imageData.forEach((elm, idx) => {
            elm.title = idx + 1;
        });
    }

    activeMarker(e, idx) {
        if (e) this.activeMarkerID = e.target.ID;
        else this.activeMarkerID = this.mapData[idx].type.ID;

        this.mapData.forEach((elm, idx) => {
            if (this.imageData[idx].type !== "marker")
                elm.type.setStyle({ color: "#257ef4" });

            if (this.mapData[idx].type.ID === this.activeMarkerID)
                if (this.imageData[idx].type !== "marker")
                    elm.type.setStyle({ color: "red" });
        });

        this.onActive();
    }

    activeItem(idx) {
        this._updateSerial();

        this.mapData.forEach((elm, idx) => {
            if (this.imageData[idx].type === "marker") elm.type.closePopup();
            else elm.type.setStyle({ color: "#257ef4" });
        });

        if (!this.mapData[idx]) return;

        this.map.removeLayer(this.mapData[idx].type);
        if (this.imageData[idx].hidden) return;

        this.map.addLayer(this.mapData[idx].type);

        if (this.imageData[idx].type === "marker")
            this.mapData[idx].type.openPopup();
        else this.mapData[idx].type.setStyle({ color: "red" });

        this.activeMarkerID = this.mapData[idx].type.ID;

        this.onItemActive();
    }

    removeMarker(idx) {
        if (this.lastPopUpMarker) this.map.removeLayer(this.lastPopUpMarker);

        this.map.removeLayer(this.mapData[idx].type);
        this.mapData.splice(idx, 1);
        this.imageData.splice(idx, 1);

        this.update({ id: this.active }, { data: this.imageData });

        this.updateData();
    }

    removeAllMarker() {
        if (this.lastPopUpMarker) this.map.removeLayer(this.lastPopUpMarker);

        this.mapData.forEach((elm) => {
            this.map.removeLayer(elm.type);
        });

        this.mapData = [];
        this.imageData = [];

        this.updateData();

        this.update({ id: this.active }, { data: this.imageData });
    }

    removeAllMarkers() {
        this.mapData.forEach((element) => {
            this.map.removeLayer(element.type);
        });

        this.updateData([[], []]);
        return [];
    }

    populateMarkers(recieved) {
        this.mapData = [];
        this.imageData = [];

        recieved.data.forEach((element) => {
            if (element.type === "marker") {
                this.addMarker(element.coord, element);
            } else if (element.type === "circle") {
                this.addCircle(element.coord, element, element.extraOptions?.radius);
            } else if (element.type === "polygon") {
                this.addLine(element.coord, element);
            }
        });

        return [this.mapData, this.imageData];
    }

    addTempPopup(coordinates, id) {
        if (coordinates.length) coordinates = coordinates[coordinates.length - 1];

        var greenIcon = this.leaflet?.icon({
            iconUrl: "/options/0.svg",
            shadowUrl: "",

            iconSize: [0, 1],
            shadowSize: [50, 64],
            iconAnchor: [17, 45],
            shadowAnchor: [4, 62],
            popupAnchor: [3, -30],
        });

        const customOptions = {
            maxWidth: "800",
            className: "custom",
        };

        let marker = this.leaflet
            ?.marker(coordinates, { icon: greenIcon })
            .addTo(this.map)
            .bindPopup(this.popupContent, customOptions);

        this.lastPopUpMarker = marker;

        marker.openPopup();

        marker.on("popupclose", () => {
            this.map.removeLayer(marker);
        });
    }

    _formPipeData(obj, coordinates, type, extraOptions = {}) {
        obj.ID = new Date().getTime() + Math.random() * 1000;
        this.mapData.push({ type: obj });
        this.imageData.push({
            coord: coordinates,
            title: this.mapData.length,
            data: "",
            extraOptions,
            type: type,
        });

        this.showPopup = true;

        this.update({ id: this.active }, { data: this.imageData });

        this.addTempPopup(coordinates);

        this.onActive();

        this.updateData();

        this.resetMode("");
    }

    _delegatePipeData(obj, existing) {
        obj.ID = Math.round(new Date().getTime() + Math.random() * 1000);
        this.mapData.push({ type: obj });
        this.imageData.push(existing);
    }

    addMarker(coordinates, existing) {
        //class
        var greenIcon = this.leaflet?.icon({
            iconUrl: "/options/0.svg",
            shadowUrl: "",

            iconSize: [38, 60],
            shadowSize: [50, 64],
            iconAnchor: [17, 45],
            shadowAnchor: [4, 62],
            popupAnchor: [3, -30],
        });

        let marker = this.leaflet
            ?.marker(coordinates, { icon: greenIcon })
            .addTo(this.map)
            .bindPopup(existing ? `${existing.title}` : "pin")
            .on("click", (e) => {
                this.activeMarker(e);
            });

        if (!existing) this._formPipeData(marker, coordinates, "marker");
        else this._delegatePipeData(marker, existing);
    }

    addCircle(coordinates, existing, radius = 40) {
        let circle = this.leaflet
            ?.circle(coordinates, radius)
            .addTo(this.map)
            .on("click", (e) => {
                this.activeMarker(e);
            });

        circle?.setStyle({ fillColor: "#257ef4" });

        if (!existing)
            this._formPipeData(circle, coordinates, "circle", { radius });
        else this._delegatePipeData(circle, existing);
    }

    addRectangle(coordinates, existing) {
        let rectangle = this.leaflet
            ?.rectangle(coordinates)
            .addTo(this.map)
            .on("click", (e) => {
                this.activeMarker(e);
            });

        rectangle?.setStyle({ fillColor: "#257ef4" });

        if (!existing) this._formPipeData(rectangle, coordinates, "rectangle");
        else this._delegatePipeData(rectangle, existing);
    }

    addLine(coordinates, existing) {
        let polyLine = this.leaflet
            ?.polyline(coordinates)
            .addTo(this.map)
            .on("click", (e) => {
                this.activeMarker(e);
            });

        polyLine?.setStyle({ fillColor: "#257ef4" });

        if (!polyLine) return;

        if (!existing) this._formPipeData(polyLine, coordinates, "polygon");
        else this._delegatePipeData(polyLine, existing);
    }
}
