/**
 * 不认命 App - 高德地图集成
 * 需要在 HTML 中添加高德地图 SDK
 */

// 高德地图配置
const AMAP_CONFIG = {
    key: '你的高德地图 API Key',  // 需要申请
    version: '2.0',
    plugins: ['AMap.Scale', 'AMap.OverView', 'AMap.ToolBar', 'AMap.MapType']
};

// 地图实例
let map = null;
let markers = [];

/**
 * 初始化地图
 */
function initMap(containerId = 'mapContainer') {
    if (typeof AMap === 'undefined') {
        console.error('高德地图 SDK 未加载');
        return;
    }
    
    map = new AMap.Map(containerId, {
        zoom: 5,
        center: [116.397428, 39.90923],  // 北京
        viewMode: '3D',
        plugins: AMAP_CONFIG.plugins
    });
    
    console.log('✅ 地图初始化成功');
}

/**
 * 在地图上标记寺庙
 */
function markTemple(temple) {
    if (!map) {
        console.error('地图未初始化');
        return;
    }
    
    const marker = new AMap.Marker({
        position: new AMap.LngLat(temple.longitude, temple.latitude),
        title: temple.name,
        label: {
            content: temple.name,
            offset: new AMap.Pixel(0, -30)
        }
    });
    
    // 信息窗口
    const infoWindow = new AMap.InfoWindow({
        content: `
            <div style="padding: 10px;">
                <h3 style="margin: 0 0 10px 0;">${temple.name}</h3>
                <p><strong>类型:</strong> ${temple.type} - ${temple.subtype}</p>
                <p><strong>评级:</strong> ${'⭐'.repeat(Math.floor(temple.rating))}</p>
                <p><strong>地址:</strong> ${temple.address}</p>
                <p><strong>门票:</strong> ${temple.ticket || '免费'}</p>
                <p><strong>祈福:</strong> ${temple.prayer_focus?.join('、') || '全部'}</p>
            </div>
        `,
        offset: new AMap.Pixel(0, -30)
    });
    
    marker.on('click', () => {
        infoWindow.open(map, marker.getPosition());
    });
    
    marker.setMap(map);
    markers.push(marker);
    
    console.log(`✅ 标记寺庙：${temple.name}`);
}

/**
 * 批量标记寺庙
 */
function markTemples(temples) {
    temples.forEach(temple => markTemple(temple));
    
    // 调整视野显示所有标记
    if (markers.length > 0) {
        map.setFitView();
    }
}

/**
 * 清除所有标记
 */
function clearMarkers() {
    markers.forEach(marker => marker.setMap(null));
    markers = [];
    console.log('✅ 清除所有标记');
}

/**
 * 搜索附近寺庙
 */
function searchNearby(latitude, longitude, radius = 5000) {
    if (!map) {
        console.error('地图未初始化');
        return;
    }
    
    // 这里需要调用后端 API 搜索附近寺庙
    console.log(`🔍 搜索附近寺庙：${latitude}, ${longitude}, 半径${radius}米`);
}

/**
 * 导航到寺庙
 */
function navigateToTemple(temple) {
    if (!temple.latitude || !temple.longitude) {
        console.error('寺庙坐标无效');
        return;
    }
    
    const url = `https://uri.amap.com/navigation?from=我的位置&to=${temple.longitude},${temple.latitude}&to_name=${encodeURIComponent(temple.name)}&mode=car`;
    window.open(url, '_blank');
    
    console.log(`🧭 导航到：${temple.name}`);
}

/**
 * 加载高德地图 SDK
 */
function loadAMapScript() {
    return new Promise((resolve, reject) => {
        if (typeof AMap !== 'undefined') {
            resolve();
            return;
        }
        
        const script = document.createElement('script');
        script.src = `https://webapi.amap.com/maps?v=${AMAP_CONFIG.version}&key=${AMAP_CONFIG.key}&plugin=${AMAP_CONFIG.plugins.join(',')}`;
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
    });
}

// 导出函数
window.AMapIntegration = {
    init: initMap,
    markTemple,
    markTemples,
    clearMarkers,
    searchNearby,
    navigateToTemple,
    loadScript: loadAMapScript
};

console.log('🗺️ 地图集成模块加载完成');
