import { useEffect } from "react";
import { useMap } from "react-leaflet";

export function MapController({ bounds, center, zoom }) {
  const map = useMap();

  useEffect(() => {
    if (bounds) {
      // fit the map to the new bounds, with a little padding
      map.fitBounds(bounds, { padding: [20, 20], animate: true, duration: 1.0 });
    } else if (center) {
      // fallback: just pan to the center
      map.flyTo(center, zoom, { animate: true, duration: 1.0 });
    }
  }, [map, bounds, center, zoom]);

  return null;
}