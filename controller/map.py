from PyQt5.QtWidgets import  QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class RealTimeMapApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('通过点击地图实现路线规划')
        self.resize(1000, 700)

        layout = QVBoxLayout()
        self.qwebengine = QWebEngineView(self)
        layout.addWidget(self.qwebengine)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.qwebengine.setHtml(self.generate_map_html(), baseUrl=QUrl.fromLocalFile('.'))

        self.amap_web_key = "3dcea51c39f6c84bac3d50356cc9f39f"

    def generate_map_html(self):
        html = r"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8" />
            <title>Click for Route</title>
            <style>
                html, body, #map {
                    height: 100%;
                    margin: 0;
                }
            </style>
            <!-- Leaflet CSS & JS -->
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
            <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
            <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
        </head>
        <body>
            <div id="map"></div>
            <script>
                // 初始化地图
                var mymap = L.map('map').setView([39.9042, 116.4074], 12); // 默认北京坐标
                L.tileLayer("http://webrd0{s}.is.autonavi.com/appmaptile?lang=zh_cn&size=2&scale=3&style=8&x={x}&y={y}&z={z}", {
                    attribution: '高德地图',
                    maxZoom: 18,
                    minZoom: 3,
                    subdomains: "1234"
                }).addTo(mymap);

                // 用于承载线路、起点、终点等
                var routeLayer = L.layerGroup().addTo(mymap);

                // WebChannel 初始化
                new QWebChannel(qt.webChannelTransport, function(channel) {
                    var bridge = channel.objects.bridge;

                    // 地图点击事件 -> 调用Python的 receive_message(lat, lng)
                    mymap.on('click', function(e) {
                        var lat = e.latlng.lat;
                        var lng = e.latlng.lng;
                        bridge.receive_message(lat, lng);
                    });
                });

                // JS 端用于在地图上绘制路线
                function drawRoute(routePoints) {
                    // 清理旧的层
                    routeLayer.clearLayers();

                    // 绘制路线
                    var polyline = L.polyline(routePoints, {color: 'red'}).addTo(routeLayer);

                    // 在起点和终点添加小圆点或标记
                    if (routePoints.length > 0) {
                        L.circleMarker(routePoints[0], {
                            radius: 6, fillColor: 'green', color: 'green', fillOpacity: 1
                        }).addTo(routeLayer);
                    }
                    if (routePoints.length > 1) {
                        L.circleMarker(routePoints[routePoints.length-1], {
                            radius: 6, fillColor: 'blue', color: 'blue', fillOpacity: 1
                        }).addTo(routeLayer);
                    }

                    // 自动调整视野
                    if (routePoints.length > 1) {
                        var bounds = L.latLngBounds(routePoints);
                        mymap.fitBounds(bounds);
                    }
                }
            </script>
        </body>
        </html>
        """
        return html


    def refresh(self):
        pass
