import React from "react";
import "./styles.css";
import "leaflet/dist/leaflet.css";

import {MapContainer, TileLayer} from "react-leaflet";

export default function App() {
  return (
    <MapContainer center={[43.1566, 77.6088]} zoom={13}>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
    </MapContainer>
  );
}