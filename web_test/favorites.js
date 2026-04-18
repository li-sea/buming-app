/**
 * 不认命 App - 收藏功能
 * 使用 localStorage 本地存储
 */

const FAVORITES_KEY = 'buming_favorites';
const HISTORY_KEY = 'buming_history';

/**
 * 获取收藏列表
 */
function getFavorites() {
    const data = localStorage.getItem(FAVORITES_KEY);
    return data ? JSON.parse(data) : [];
}

/**
 * 添加收藏
 */
function addFavorite(temple) {
    const favorites = getFavorites();
    
    // 检查是否已收藏
    const exists = favorites.some(f => f.name === temple.name && f.province === temple.province);
    if (exists) {
        console.log('⚠️ 已收藏过该寺庙');
        return false;
    }
    
    // 添加收藏时间
    temple.favoriteTime = new Date().toISOString();
    favorites.push(temple);
    
    localStorage.setItem(FAVORITES_KEY, JSON.stringify(favorites));
    console.log(`✅ 收藏成功：${temple.name}`);
    
    // 更新 UI
    updateFavoritesUI();
    
    return true;
}

/**
 * 取消收藏
 */
function removeFavorite(templeName, province) {
    const favorites = getFavorites();
    const filtered = favorites.filter(f => !(f.name === templeName && f.province === province));
    
    if (filtered.length === favorites.length) {
        console.log('⚠️ 未找到该收藏');
        return false;
    }
    
    localStorage.setItem(FAVORITES_KEY, JSON.stringify(filtered));
    console.log(`✅ 取消收藏：${templeName}`);
    
    // 更新 UI
    updateFavoritesUI();
    
    return true;
}

/**
 * 检查是否已收藏
 */
function isFavorited(templeName, province) {
    const favorites = getFavorites();
    return favorites.some(f => f.name === templeName && f.province === province);
}

/**
 * 获取收藏数量
 */
function getFavoritesCount() {
    return getFavorites().length;
}

/**
 * 更新收藏 UI
 */
function updateFavoritesUI() {
    const favorites = getFavorites();
    const container = document.getElementById('favoritesList');
    
    if (!container) {
        return;
    }
    
    if (favorites.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: #999; padding: 20px;">暂无收藏</p>';
        return;
    }
    
    container.innerHTML = favorites.map((temple, index) => `
        <div class="temple-card" style="margin-bottom: 10px;">
            <h3>${index + 1}. ${temple.name} ${'⭐'.repeat(Math.floor(temple.rating))}</h3>
            <div class="temple-info">
                <div class="temple-info-item"><strong>类型:</strong> ${temple.type} - ${temple.subtype}</div>
                <div class="temple-info-item"><strong>位置:</strong> ${temple.province}${temple.city}</div>
                <div class="temple-info-item"><strong>地址:</strong> ${temple.address}</div>
            </div>
            <div style="margin-top: 10px;">
                <button onclick="navigateToTemple('${temple.name}', '${temple.province}')" class="btn" style="padding: 5px 10px; font-size: 12px; width: auto;">🧭 导航</button>
                <button onclick="removeFavorite('${temple.name}', '${temple.province}')" class="btn" style="padding: 5px 10px; font-size: 12px; width: auto; background: #dc3545;">❌ 取消收藏</button>
            </div>
        </div>
    `).join('');
    
    // 更新收藏数量显示
    const countEl = document.getElementById('favoritesCount');
    if (countEl) {
        countEl.textContent = favorites.length;
    }
}

/**
 * 添加浏览历史
 */
function addHistory(temple) {
    const history = getHistory();
    
    // 检查是否已存在
    const exists = history.some(h => h.name === temple.name && h.province === temple.province);
    if (exists) {
        // 更新浏览时间
        const item = history.find(h => h.name === temple.name && h.province === temple.province);
        item.lastViewed = new Date().toISOString();
        item.viewCount = (item.viewCount || 1) + 1;
    } else {
        // 添加新记录
        temple.lastViewed = new Date().toISOString();
        temple.viewCount = 1;
        history.unshift(temple);  // 添加到开头
    }
    
    // 只保留最近 50 条
    if (history.length > 50) {
        history.splice(50);
    }
    
    localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
}

/**
 * 获取浏览历史
 */
function getHistory() {
    const data = localStorage.getItem(HISTORY_KEY);
    return data ? JSON.parse(data) : [];
}

/**
 * 清除浏览历史
 */
function clearHistory() {
    localStorage.removeItem(HISTORY_KEY);
    console.log('✅ 清除浏览历史');
    updateHistoryUI();
}

/**
 * 更新历史 UI
 */
function updateHistoryUI() {
    const history = getHistory();
    const container = document.getElementById('historyList');
    
    if (!container) {
        return;
    }
    
    if (history.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: #999; padding: 20px;">暂无浏览历史</p>';
        return;
    }
    
    container.innerHTML = history.map((temple, index) => `
        <div class="temple-card" style="margin-bottom: 10px; opacity: 0.8;">
            <h4>${index + 1}. ${temple.name}</h4>
            <div class="temple-info">
                <div class="temple-info-item"><strong>位置:</strong> ${temple.province}${temple.city}</div>
                <div class="temple-info-item"><strong>浏览时间:</strong> ${new Date(temple.lastViewed).toLocaleString()}</div>
            </div>
        </div>
    `).join('');
}

/**
 * 初始化收藏功能
 */
function initFavorites() {
    updateFavoritesUI();
    updateHistoryUI();
    console.log('✅ 收藏功能初始化完成');
}

// 导出函数
window.Favorites = {
    get: getFavorites,
    add: addFavorite,
    remove: removeFavorite,
    isFavorited,
    getCount: getFavoritesCount,
    updateUI: updateFavoritesUI,
    history: {
        add: addHistory,
        get: getHistory,
        clear: clearHistory,
        updateUI: updateHistoryUI
    },
    init: initFavorites
};

console.log('❤️ 收藏功能模块加载完成');
