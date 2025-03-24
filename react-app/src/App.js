import React from "react";
import Select from 'react-select'
import "./styles.css";
import "leaflet/dist/leaflet.css";

import {ImageOverlay, MapContainer, TileLayer} from "react-leaflet"; 
import {latLngBounds} from "leaflet";
const bounds = new latLngBounds([37.6262, -97.1930], [37.7830, -97.0820])

export default function App() {
  return (
    // replace center coords with get_lat_center(), get_lon_center() functions later
    <MapContainer center={[37.7046, -97.13749]} zoom={13}>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {/* add image overlay */}
      <ImageOverlay
      url="https://earthengine.googleapis.com/v1/projects/earthengine-legacy/thumbnails/f00a5d48ba20556f60e2cacc834e9008-47351915b71b624d77fa4496dbe52648:getPixels"
      bounds={bounds}
      opacity={1}
      zIndex={10}/>
    </MapContainer>
  );
}

