// قائمة المتتبعين للمنع الفعلي من الصفحة
const TRACKERS = [
    "google-analytics.com",
    "googletagmanager.com",
    "facebook.com/tr",
    "doubleclick.net",
    "amazon-adsystem.com",
    "outbrain.com",
    "taboola.com",
    "criteo.com",
    "adnxs.com",
    "scorecardresearch.com",
    "hotjar.com",
    "clarity.ms",
    "mixpanel.com",
    "segment.com"
];

// إرسال إشعار للـ background عند اكتشاف متتبع
function notifyTrackerDetected(url) {
    try {
        chrome.runtime.sendMessage({
            action: "trackerDetected",
            url: url
        });
    } catch(e) {
        console.log("خطأ في الإرسال:", e);
    }
}

// حذف Tracking Pixels (صور خفية)
function removeTrackingPixels() {
    const images = document.querySelectorAll('img');
    let removed = 0;
    
    images.forEach(img => {
        const src = img.src.toLowerCase();
        let isTracker = false;
        let trackerUrl = "";
        
        for (let tracker of TRACKERS) {
            if (src.includes(tracker)) {
                isTracker = true;
                trackerUrl = src;
                break;
            }
        }
        
        if (!isTracker && (img.width <= 1 || img.height <= 1 || !img.width || !img.height)) {
            isTracker = true;
            trackerUrl = src;
        }
        
        if (!isTracker && (src.includes('pixel') || src.includes('track') || src.includes('beacon'))) {
            isTracker = true;
            trackerUrl = src;
        }
        
        if (isTracker) {
            img.remove();
            removed++;
            notifyTrackerDetected(trackerUrl);
        }
    });
    
    if (removed > 0) {
        console.log(`🖼️ تم إزالة ${removed} tracking pixel`);
    }
    return removed;
}

// حذف إطارات التتبع المخفية
function removeTrackingFrames() {
    const iframes = document.querySelectorAll('iframe');
    let removed = 0;
    
    iframes.forEach(iframe => {
        const src = iframe.src.toLowerCase();
        let isTracker = false;
        
        for (let tracker of TRACKERS) {
            if (src.includes(tracker)) {
                isTracker = true;
                break;
            }
        }
        
        if (src.includes('track') || src.includes('analytics')) {
            isTracker = true;
        }
        
        if (isTracker) {
            iframe.remove();
            removed++;
            notifyTrackerDetected(src);
        }
    });
    
    if (removed > 0) {
        console.log(`📄 تم إزالة ${removed} iframe متتبع`);
    }
    return removed;
}

// حذف سكريبتات التتبع
function removeTrackingScripts() {
    const scripts = document.querySelectorAll('script');
    let removed = 0;
    
    scripts.forEach(script => {
        const src = script.src.toLowerCase();
        let isTracker = false;
        
        for (let tracker of TRACKERS) {
            if (src.includes(tracker)) {
                isTracker = true;
                break;
            }
        }
        
        if (src.includes('analytics.js') || src.includes('tracking.js')) {
            isTracker = true;
        }
        
        if (isTracker && src) {
            script.remove();
            removed++;
            notifyTrackerDetected(src);
        }
    });
    
    if (removed > 0) {
        console.log(`📜 تم إزالة ${removed} سكريبت متتبع`);
    }
    return removed;
}

// وظيفة رئيسية لتنظيف الصفحة
function cleanPage() {
    console.log("🛡️ Privacy Shield: بدء تنظيف الصفحة...");
    removeTrackingPixels();
    removeTrackingFrames();
    removeTrackingScripts();
    console.log("✅ Privacy Shield: تم الانتهاء من التنظيف");
}

// مراقبة إضافات DOM الجديدة
const observer = new MutationObserver(() => {
    clearTimeout(window.cleanupTimeout);
    window.cleanupTimeout = setTimeout(() => {
        removeTrackingPixels();
        removeTrackingFrames();
        removeTrackingScripts();
    }, 100);
});

// بدء التشغيل
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        cleanPage();
        if (document.body) {
            observer.observe(document.body, { childList: true, subtree: true });
        }
    });
} else {
    cleanPage();
    if (document.body) {
        observer.observe(document.body, { childList: true, subtree: true });
    }
}

window.addEventListener('load', () => cleanPage());

console.log("✅ Privacy Shield content script loaded");