export default function track_display(map) {
    var imageUrl = 'https://earthengine.googleapis.com/v1/projects/earthengine-legacy/thumbnails/2fb4961176a4f727ce38672ffd96012a-000201cc7d8f73c03380c4dcbc1abe25:getPixels';
    var errorOverlayUrl = 'https://cdn-icons-png.flaticon.com/512/110/110686.png';
    var altText = 'Wichita, KS Tornado 2022-04-29 id: 621425';
    var latLngBounds = L.latLngBounds([[37.6262, -97.1930], [37.7830, -97.0820]]);

    var imageOverlay = L.imageOverlay(imageUrl, latLngBounds, {
        opacity: 0.8,
        errorOverlayUrl: errorOverlayUrl,
        alt: altText,
        interactive: true
    }).addTo(map);
}

export default function create_map(start_coord, end_coord) {
    var map = L.map('map').setView([37.8, -96], 4);

    var osm = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);
}