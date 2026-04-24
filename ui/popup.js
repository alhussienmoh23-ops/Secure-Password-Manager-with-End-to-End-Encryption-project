// تحديث الإحصائيات
async function updateStats() {
    chrome.storage.local.get(['blockedCount', 'trackerLog'], (result) => {
        const blockedCount = result.blockedCount || 0;
        document.getElementById('blockedCount').textContent = blockedCount;
        
        const trackerCount = result.trackerLog ? result.trackerLog.length : 0;
        document.getElementById('trackerCount').textContent = trackerCount;
        
        const trackerLogDiv = document.getElementById('trackerLog');
        if (result.trackerLog && result.trackerLog.length > 0) {
            trackerLogDiv.innerHTML = '';
            result.trackerLog.slice(-5).reverse().forEach(tracker => {
                const div = document.createElement('div');
                div.className = 'tracker-item';
                let domain = tracker.url.split('/')[2] || tracker.url;
                if (domain.length > 40) domain = domain.substring(0, 40) + '...';
                div.innerHTML = `🚫 ${domain}<br>⏰ ${tracker.time}`;
                trackerLogDiv.appendChild(div);
            });
        } else {
            trackerLogDiv.innerHTML = '✨ لا يوجد متتبعين حتى الآن<br><span style="font-size: 9px;">افتح موقعاً آخر لتجربة الحظر</span>';
        }
    });
    
    // عرض الموقع الحالي
    try {
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            if (tabs[0] && tabs[0].url) {
                try {
                    const url = new URL(tabs[0].url);
                    let hostname = url.hostname;
                    if (hostname.length > 35) hostname = hostname.substring(0, 35) + '...';
                    document.getElementById('currentSite').innerHTML = `🌐 ${hostname}`;
                } catch(e) {
                    document.getElementById('currentSite').innerHTML = `🌐 ${tabs[0].url.substring(0, 40)}`;
                }
            }
        });
    } catch(e) {
        console.log('خطأ في جلب التبويب:', e);
    }
}

// مسح الإحصائيات
const clearBtn = document.getElementById('clearStats');
if (clearBtn) {
    clearBtn.addEventListener('click', () => {
        chrome.storage.local.set({ blockedCount: 0, trackerLog: [] }, () => {
            updateStats();
            alert('✅ تم مسح جميع الإحصائيات');
        });
    });
}

// تحليل سياسة الخصوصية
const analyzeBtn = document.getElementById('analyzePage');
if (analyzeBtn) {
    analyzeBtn.addEventListener('click', async () => {
        try {
            const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
            const currentUrl = tabs[0].url;
            
            const originalText = analyzeBtn.textContent;
            analyzeBtn.textContent = '⏳ جاري التحليل...';
            analyzeBtn.disabled = true;
            
            const response = await fetch('http://localhost:5000/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: currentUrl })
            });
            
            const result = await response.json();
            
            if (result.error) {
                alert('❌ خطأ: ' + result.error);
            } else {
                let message = `🛡️ ${result.icon} تقرير الخصوصية\n`;
                message += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
                message += `📊 التقييم: ${result.grade}\n`;
                message += `🎯 الدرجة: ${result.score}/100\n`;
                message += `📝 ${result.description}\n\n`;
                
                if (result.positives && result.positives.length > 0) {
                    message += `✅ الإيجابيات:\n`;
                    result.positives.forEach(p => message += `   ${p}\n`);
                    message += `\n`;
                }
                
                if (result.negatives && result.negatives.length > 0) {
                    message += `⚠️ السلبيات:\n`;
                    result.negatives.forEach(n => message += `   ${n}\n`);
                    message += `\n`;
                }
                
                if (result.recommendations && result.recommendations.length > 0) {
                    message += `💡 التوصيات:\n`;
                    result.recommendations.forEach(r => message += `   ${r}\n`);
                }
                
                alert(message);
            }
            
            analyzeBtn.textContent = originalText;
            analyzeBtn.disabled = false;
            
        } catch(error) {
            console.error('خطأ:', error);
            alert(`❌ لا يمكن الاتصال بالسيرفر!\n\n🔧 تأكد من تشغيل السيرفر في Terminal:\n   python privacy_analyzer.py\n\n📍 السيرفر يجب أن يعمل على:\n   http://localhost:5000`);
            
            analyzeBtn.textContent = '🔍 تحليل سياسة الخصوصية';
            analyzeBtn.disabled = false;
        }
    });
}

// التحقق من اتصال السيرفر
async function checkServer() {
    try {
        const response = await fetch('http://localhost:5000/health');
        if (response.ok) {
            const badge = document.querySelector('.status-badge');
            if (badge) badge.style.backgroundColor = '#4CAF50';
        } else {
            const badge = document.querySelector('.status-badge');
            if (badge) badge.style.backgroundColor = '#FF9800';
        }
    } catch(e) {
        const badge = document.querySelector('.status-badge');
        if (badge) badge.style.backgroundColor = '#f44336';
    }
}

// بدء التحديث
updateStats();
setInterval(updateStats, 2000);
checkServer();
setInterval(checkServer, 5000);