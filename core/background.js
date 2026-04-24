// قائمة المجالات اللي بتجمع بيانات (trackers)
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
    "segment.com",
    "adsrvr.org",
    "exelator.com",
    "rfihub.com",
    "adroll.com",
    "lijit.com",
    "openx.net",
    "pubmatic.com",
    "rubiconproject.com"
];

let blockedCount = 0;
let trackerLog = [];

// تحديث الإحصائيات من content script
function updateStats(trackerUrl) {
    blockedCount++;
    trackerLog.push({
        url: trackerUrl,
        time: new Date().toLocaleTimeString(),
        date: new Date().toISOString()
    });
    
    // الاحتفاظ بآخر 50 فقط
    if (trackerLog.length > 50) {
        trackerLog = trackerLog.slice(-50);
    }
    
    // حفظ الإحصائيات
    chrome.storage.local.set({ 
        blockedCount: blockedCount,
        trackerLog: trackerLog
    });
    
    console.log(`📊 تم اكتشاف متتبع: ${trackerUrl}`);
}

// منع third-party cookies
chrome.cookies.onChanged.addListener(function(changeInfo) {
    const cookie = changeInfo.cookie;
    const domain = cookie.domain;
    
    // إذا كان الكوكي من domain مختلف عن الموقع الرئيسي
    if (changeInfo.removed === false && domain && domain.startsWith('.')) {
        try {
            chrome.cookies.remove({
                url: `https://${domain.substring(1)}`,
                name: cookie.name
            }, () => {
                if (!chrome.runtime.lastError) {
                    console.log(`🍪 تم حذف كوكي تابع: ${cookie.name} from ${domain}`);
                }
            });
        } catch(e) {
            console.log("خطأ في حذف الكوكي:", e);
        }
    }
});

// الاستماع لرسائل من content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "trackerDetected") {
        // تسجيل متتبع تم اكتشافه من content script
        updateStats(request.url);
        sendResponse({ success: true });
    }
    else if (request.action === "getStats") {
        // إرسال الإحصائيات إلى popup
        chrome.storage.local.get(['blockedCount', 'trackerLog'], (result) => {
            sendResponse({
                blockedCount: result.blockedCount || 0,
                trackerLog: result.trackerLog || []
            });
        });
        return true; // مهم للـ async
    }
    else if (request.action === "clearStats") {
        // مسح الإحصائيات
        blockedCount = 0;
        trackerLog = [];
        chrome.storage.local.set({ 
            blockedCount: 0, 
            trackerLog: [] 
        }, () => {
            sendResponse({ success: true });
        });
        return true;
    }
});

// تنبيه بأن الـ background script شغال
console.log("✅ Privacy Shield background script loaded");
console.log("📋 جاهز لحماية خصوصيتك");