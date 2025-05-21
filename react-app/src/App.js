import React, { useEffect, useState, useRef } from "react";
import Select from 'react-select'
import "./styles.css";
import "leaflet/dist/leaflet.css";
import { MapController } from "./MapController";
import {ImageOverlay, MapContainer, TileLayer} from "react-leaflet"; 
import {latLngBounds} from "leaflet";

function get_center(lat1, lon1, lat2, lon2) {
  return [(lat1 + lat2) / 2, (lon1 + lon2) / 2];
}

export default function App() {
  const [tornadoOptions, setOptions] = useState([]);
  const [imageUrl, setImageUrl] = useState("");
  const [mapCenter] = useState([37.7046, -97.13749])
  const [bounds, setBounds] = useState(latLngBounds([37.6262, -97.1930], [37.7830, -97.0820]))
  const mapRef = useRef();

  useEffect(() => {
    fetch("http://localhost:5000/api/get_options")
      .then((res) => res.json())
      .then((data) => {
        setOptions(data); // already in [{value, label}] format
      })
      .catch((error) => {
        console.error("Error fetching tornado data:", error);
      });
  }, []);

  const handleSelect = (selected) => {
    const id = selected.value;
    fetch(`http://localhost:5000/satellite/after/${id}`)
      .then((res) => res.json())
      .then((data) => {
        const [slat, slon] = [data.lat1, data.lon1];
        const [elat, elon] = [data.lat2, data.lon2];

        setImageUrl(data.url);
        setBounds(latLngBounds([slat, slon], [elat, elon]))
        const center = get_center(slat, slon, elat, elon);

        console.error("image fetched and map updated")
        mapRef.current?.flyTo(center, 13, { animate: true, duration: 1.5 });
      })
      .catch((err) => console.error("Error fetching image:", err));
  };

  return (
    <div style={{ position: 'relative', height: '100vh' }}>
      {/* Select overlay container */}
      <div style={{
        position: 'absolute',
        top: 10,
        right: 10,
        zIndex: 1000,
        width: 200
      }}>

        <Select 
          options={tornadoOptions} 
          placeholder="Select a Tornado!"
          onChange={handleSelect}
        />

      </div>

      <div>
        <MapContainer
          center={mapCenter}
          zoom={13}
          whenCreated={(mapInstance) => { mapRef.current = mapInstance; }}
          style={{zIndex: 0 }}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <ImageOverlay
            url={imageUrl}
            bounds={bounds}
            opacity={1}
            zIndex={10}
          />

          <MapController bounds={bounds} center={mapCenter} zoom={13}/>

        </MapContainer>
      </div>
    </div>
  );
}

