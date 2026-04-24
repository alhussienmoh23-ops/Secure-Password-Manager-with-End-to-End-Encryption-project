# import re
# import json
# from datetime import datetime
# from typing import Dict, List, Tuple

# class PrivacyPolicyAnalyzer:
#     def __init__(self):
#         # الكلمات الخطيرة (اللي تقلل درجة الخصوصية)
#         self.bad_keywords = {
#             "sell your data": -15,
#             "share with third parties": -12,
#             "advertising partners": -10,
#             "marketing purposes": -8,
#             "collect personal information": -7,
#             "tracking technologies": -7,
#             "cookies for advertising": -6,
#             "data brokers": -15,
#             "sell to third parties": -15,
#             "share your information": -10,
#             "targeted advertising": -8,
#             "behavioral advertising": -8,
#             "cross-site tracking": -10,
#             "retain your data indefinitely": -5,
#             "no opt-out": -10,
#             "automatic data collection": -5
#         }
        
#         # الكلمات الجيدة (اللي تزيد درجة الخصوصية)
#         self.good_keywords = {
#             "do not sell": +15,
#             "delete your data": +10,
#             "right to be forgotten": +12,
#             "data portability": +8,
#             "opt-out": +10,
#             "encryption": +7,
#             "anonymized": +8,
#             "pseudonymized": +6,
#             "gdpr compliant": +15,
#             "ccpa compliant": +12,
#             "end-to-end encryption": +10,
#             "zero-knowledge": +12,
#             "no third parties": +15,
#             "data minimization": +10,
#             "access your data": +8,
#             "rectification": +5
#         }
        
#         # عناوين GDPR/CCPA المهمة
#         self.rights_keywords = [
#             "right to access",
#             "right to rectification",
#             "right to erasure",
#             "right to restrict processing",
#             "right to data portability",
#             "right to object",
#             "automated decision-making",
#             "profiling"
#         ]
    
#     def extract_text_from_html(self, html_content: str) -> str:
#         """استخراج النص من HTML (إزالة الوسوم)"""
#         # إزالة وسوم HTML
#         text = re.sub(r'<[^>]+>', ' ', html_content)
#         # إزالة المسافات الزائدة
#         text = re.sub(r'\s+', ' ', text)
#         # تحويل للنص الصغير
#         text = text.lower()
#         return text
    
#     def calculate_privacy_score(self, text: str) -> Tuple[int, List[str], List[str]]:
#         """حساب درجة الخصوصية وجمع الإيجابيات والسلبيات"""
#         score = 70  # نبدأ من 70 (متوسط)
#         positives = []
#         negatives = []
        
#         # فحص الكلمات الخطيرة
#         for keyword, points in self.bad_keywords.items():
#             if keyword in text:
#                 score += points
#                 negatives.append(f"⚠️ {keyword}: {abs(points)} نقطة")
        
#         # فحص الكلمات الجيدة
#         for keyword, points in self.good_keywords.items():
#             if keyword in text:
#                 score += points
#                 positives.append(f"✅ {keyword}: +{points} نقطة")
        
#         # التأكد من الحدود (ما بين 0 و 100)
#         score = max(0, min(100, score))
        
#         return score, positives, negatives
    
#     def check_user_rights(self, text: str) -> List[str]:
#         """التحقق من حقوق المستخدم المذكورة"""
#         found_rights = []
#         for right in self.rights_keywords:
#             if right in text:
#                 found_rights.append(right)
#         return found_rights
    
#     def get_privacy_grade(self, score: int) -> Dict:
#         """تحويل الدرجة إلى حرف (A, B, C, D, F)"""
#         if score >= 90:
#             return {
#                 "grade": "A",
#                 "color": "#4CAF50",
#                 "description": "ممتاز - سياسة خصوصية شفافة وتحترم المستخدم",
#                 "icon": "🟢"
#             }
#         elif score >= 75:
#             return {
#                 "grade": "B",
#                 "color": "#8BC34A",
#                 "description": "جيد - معظم الممارسات جيدة مع بعض التحفظات",
#                 "icon": "🔵"
#             }
#         elif score >= 60:
#             return {
#                 "grade": "C",
#                 "color": "#FFC107",
#                 "description": "متوسط - يحتاج لتحسين في بعض النقاط",
#                 "icon": "🟡"
#             }
#         elif score >= 40:
#             return {
#                 "grade": "D",
#                 "color": "#FF9800",
#                 "description": "ضعيف - ممارسات خصوصية مثيرة للقلق",
#                 "icon": "🟠"
#             }
#         else:
#             return {
#                 "grade": "F",
#                 "color": "#F44336",
#                 "description": "خطير - يبيع البيانات ولا يحترم الخصوصية",
#                 "icon": "🔴"
#             }
    
#     def generate_recommendations(self, score: int, negatives: List) -> List[str]:
#         """توليد توصيات للمستخدم"""
#         recommendations = []
        
#         if score >= 80:
#             recommendations.append("✨ الموقع آمن ويمكن استخدامه بثقة")
#         elif score >= 60:
#             recommendations.append("⚠️ كن حذراً - تجنب مشاركة بيانات حساسة")
#             recommendations.append("🔒 استخدم بريداً إلكترونياً مؤقتاً")
#         else:
#             recommendations.append("🚫 تجنب استخدام هذا الموقع تماماً")
#             recommendations.append("🛡️ استخدم VPN وإضافات الخصوصية")
#             recommendations.append("📧 لا تستخدم بريدك الحقيقي")
        
#         if any("sell" in str(n).lower() for n in negatives):
#             recommendations.append("💰 هذا الموقع يبيع بياناتك - تجنبه")
        
#         if not any("right to erasure" in str(r).lower() for r in recommendations):
#             recommendations.append("🗑️ الموقع لا يسمح بحذف بياناتك بسهولة")
        
#         return recommendations
    
#     def analyze(self, html_content: str) -> Dict:
#         """الوظيفة الرئيسية لتحليل سياسة الخصوصية"""
#         # استخراج النص
#         text = self.extract_text_from_html(html_content)
        
#         # حساب الدرجة
#         score, positives, negatives = self.calculate_privacy_score(text)
        
#         # فحص حقوق المستخدم
#         user_rights = self.check_user_rights(text)
        
#         # الحصول على التقييم
#         grade_info = self.get_privacy_grade(score)
        
#         # النتيجة النهائية
#         result = {
#             "score": score,
#             "grade": grade_info["grade"],
#             "color": grade_info["color"],
#             "description": grade_info["description"],
#             "icon": grade_info["icon"],
#             "positives": positives[:5],  # آخر 5 إيجابيات
#             "negatives": negatives[:5],  # آخر 5 سلبيات
#             "user_rights": user_rights[:5],
#             "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "recommendations": self.generate_recommendations(score, negatives)
#         }
        
#         return result


# # 🌐 جزء Flask لإنشاء API (للاتصال من الإضافة)
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import requests

# app = Flask(__name__)
# CORS(app)  # للسماح للإضافة بالاتصال

# analyzer = PrivacyPolicyAnalyzer()

# @app.route('/analyze', methods=['POST'])
# def analyze_privacy():
#     """API لتحليل سياسة الخصوصية"""
#     try:
#         data = request.json
#         url = data.get('url')
        
#         if not url:
#             return jsonify({"error": "URL is required"}), 400
        
#         # محاولة جلب صفحة الخصوصية
#         try:
#             # جلب الصفحة الرئيسية أولاً (أو أي صفحة)
#             response = requests.get(url, timeout=10, headers={
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
#             })
            
#             if response.status_code == 200:
#                 html_content = response.text
#                 result = analyzer.analyze(html_content)
#                 result["analyzed_url"] = url
#                 return jsonify(result)
#             else:
#                 return jsonify({"error": f"Could not fetch website (status {response.status_code})"}), 404
                
#         except requests.exceptions.Timeout:
#             return jsonify({"error": "Website timeout - too slow to respond"}), 408
#         except requests.exceptions.ConnectionError:
#             return jsonify({"error": "Cannot connect to website - check URL"}), 404
#         except Exception as e:
#             return jsonify({"error": f"Network error: {str(e)}"}), 500
    
#     except Exception as e:
#         return jsonify({"error": f"Server error: {str(e)}"}), 500


# @app.route('/analyze-text', methods=['POST'])
# def analyze_text():
#     """تحليل نص مباشر (بدون جلب من الإنترنت)"""
#     try:
#         data = request.json
#         text = data.get('text', '')
        
#         if not text:
#             return jsonify({"error": "Text is required"}), 400
        
#         result = analyzer.analyze(text)
#         return jsonify(result)
    
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @app.route('/health', methods=['GET'])
# def health():
#     """فحص صحة السيرفر"""
#     return jsonify({
#         "status": "healthy", 
#         "analyzer": "ready",
#         "version": "1.0.0"
#     })


# @app.route('/', methods=['GET'])
# def home():
#     """الصفحة الرئيسية"""
#     return jsonify({
#         "name": "Privacy Policy Analyzer API",
#         "version": "1.0.0",
#         "endpoints": {
#             "POST /analyze": "Analyze website privacy policy",
#             "POST /analyze-text": "Analyze raw text",
#             "GET /health": "Health check"
#         }
#     })


# if __name__ == '__main__':
#     print("=" * 50)
#     print("🔍 Privacy Policy Analyzer Server")
#     print("=" * 50)
#     print("📡 Running on http://localhost:5000")
#     print("📋 Available Endpoints:")
#     print("   GET  /           - API Information")
#     print("   GET  /health     - Health check")
#     print("   POST /analyze    - Analyze website privacy policy")
#     print("   POST /analyze-text - Analyze raw text")
#     print("=" * 50)
#     print("✅ Server is ready! Waiting for requests...")
#     print("=" * 50)
#     app.run(debug=True, port=5000, host='localhost')







import re
import json
from datetime import datetime
from typing import Dict, List, Tuple

class PrivacyPolicyAnalyzer:
    def __init__(self):
        # الكلمات الخطيرة (اللي تقلل درجة الخصوصية)
        self.bad_keywords = {
            "sell your data": -15,
            "share with third parties": -12,
            "advertising partners": -10,
            "marketing purposes": -8,
            "collect personal information": -7,
            "tracking technologies": -7,
            "cookies for advertising": -6,
            "data brokers": -15,
            "sell to third parties": -15,
            "share your information": -10,
            "targeted advertising": -8,
            "behavioral advertising": -8,
            "cross-site tracking": -10,
            "retain your data indefinitely": -5,
            "no opt-out": -10,
            "automatic data collection": -5,
            "third party": -8,
            "ad network": -7,
            "data collection": -5,
            "user profiling": -9,
            "cross-device tracking": -8
        }
        
        # الكلمات الجيدة (اللي تزيد درجة الخصوصية)
        self.good_keywords = {
            "do not sell": +15,
            "delete your data": +10,
            "right to be forgotten": +12,
            "data portability": +8,
            "opt-out": +10,
            "encryption": +7,
            "anonymized": +8,
            "pseudonymized": +6,
            "gdpr compliant": +15,
            "ccpa compliant": +12,
            "end-to-end encryption": +10,
            "zero-knowledge": +12,
            "no third parties": +15,
            "data minimization": +10,
            "access your data": +8,
            "rectification": +5,
            "privacy by design": +12,
            "data protection": +7,
            "transparency": +6,
            "user control": +9
        }
        
        # عناوين GDPR/CCPA المهمة
        self.rights_keywords = [
            "right to access",
            "right to rectification",
            "right to erasure",
            "right to restrict processing",
            "right to data portability",
            "right to object",
            "automated decision-making",
            "profiling"
        ]
    
    def extract_text_from_html(self, html_content: str) -> str:
        """استخراج النص من HTML (إزالة الوسوم)"""
        # إزالة وسوم HTML
        text = re.sub(r'<[^>]+>', ' ', html_content)
        # إزالة المسافات الزائدة
        text = re.sub(r'\s+', ' ', text)
        # تحويل للنص الصغير
        text = text.lower()
        return text
    
    def calculate_privacy_score(self, text: str) -> Tuple[int, List[str], List[str]]:
        """حساب درجة الخصوصية بطريقة ديناميكية تعتمد على النص الفعلي"""
        positives = []
        negatives = []
        
        # حساب مجموع النقاط من الكلمات الموجودة
        total_bad_points = 0
        total_good_points = 0
        
        bad_matches_found = []
        good_matches_found = []
        
        # فحص الكلمات الخطيرة
        for keyword, points in self.bad_keywords.items():
            if keyword in text:
                total_bad_points += abs(points)
                bad_matches_found.append(keyword)
                negatives.append(f"⚠️ {keyword}: {abs(points)} نقطة")
        
        # فحص الكلمات الجيدة
        for keyword, points in self.good_keywords.items():
            if keyword in text:
                total_good_points += points
                good_matches_found.append(keyword)
                positives.append(f"✅ {keyword}: +{points} نقطة")
        
        # حساب الدرجة الديناميكية
        # نبدأ من 50 كقاعدة محايدة
        base_score = 50
        
        # نضيف نقاط الكلمات الجيدة ونطرح نقاط الكلمات السيئة
        # مع تطبيع النتيجة لتكون بين 0 و 100
        raw_score = base_score + total_good_points - total_bad_points
        
        # تطبيع إضافي: إذا كان عدد الكلمات المكتشفة كبيراً، نعدل النتيجة
        total_matches = len(bad_matches_found) + len(good_matches_found)
        if total_matches > 0:
            # كل كلمة إضافية تؤثر على النتيجة
            adjustment = min(15, total_matches * 2)
            if len(bad_matches_found) > len(good_matches_found):
                raw_score -= adjustment
            elif len(good_matches_found) > len(bad_matches_found):
                raw_score += adjustment
        
        # التأكد من الحدود (ما بين 0 و 100)
        score = max(0, min(100, raw_score))
        
        # إذا لم يتم العثور على أي كلمات، نعطي درجة محايدة بناءً على طول النص
        if total_matches == 0:
            # نصوص قصيرة جداً تعتبر غير كافية للتحليل
            text_length = len(text.split())
            if text_length < 50:
                score = 40  # نص غير كافٍ للتحليل
                negatives.append("⚠️ نص قصير جداً - تحليل غير دقيق")
            else:
                score = 55  # نص محايد بدون مؤشرات واضحة
        
        return score, positives, negatives
    
    def check_user_rights(self, text: str) -> List[str]:
        """التحقق من حقوق المستخدم المذكورة"""
        found_rights = []
        for right in self.rights_keywords:
            if right in text:
                found_rights.append(right)
        return found_rights
    
    def get_privacy_grade(self, score: int) -> Dict:
        """تحويل الدرجة إلى حرف (A, B, C, D, F)"""
        if score >= 90:
            return {
                "grade": "A",
                "color": "#4CAF50",
                "description": "ممتاز - سياسة خصوصية شفافة وتحترم المستخدم",
                "icon": "🟢"
            }
        elif score >= 75:
            return {
                "grade": "B",
                "color": "#8BC34A",
                "description": "جيد - معظم الممارسات جيدة مع بعض التحفظات",
                "icon": "🔵"
            }
        elif score >= 60:
            return {
                "grade": "C",
                "color": "#FFC107",
                "description": "متوسط - يحتاج لتحسين في بعض النقاط",
                "icon": "🟡"
            }
        elif score >= 40:
            return {
                "grade": "D",
                "color": "#FF9800",
                "description": "ضعيف - ممارسات خصوصية مثيرة للقلق",
                "icon": "🟠"
            }
        else:
            return {
                "grade": "F",
                "color": "#F44336",
                "description": "خطير - يبيع البيانات ولا يحترم الخصوصية",
                "icon": "🔴"
            }
    
    def generate_recommendations(self, score: int, negatives: List, positives: List, user_rights: List) -> List[str]:
        """توليد توصيات للمستخدم بناءً على التحليل الفعلي"""
        recommendations = []
        
        # توصيات حسب الدرجة
        if score >= 85:
            recommendations.append("✨ الموقع آمن ويمكن استخدامه بثقة")
            recommendations.append("👍 خصوصيتك محمية بشكل جيد")
        elif score >= 70:
            recommendations.append("✅ الموقع مقبول لكن اقرأ السياسة كاملة")
            recommendations.append("🔒 تجنب مشاركة بيانات حساسة جداً")
        elif score >= 55:
            recommendations.append("⚠️ كن حذراً - تجنب مشاركة بيانات حساسة")
            recommendations.append("📧 استخدم بريداً إلكترونياً مؤقتاً")
            recommendations.append("🛡️ استخدم VPN وإضافات الخصوصية")
        else:
            recommendations.append("🚫 تجنب استخدام هذا الموقع تماماً")
            recommendations.append("💀 هذا الموقع خطر على خصوصيتك")
            recommendations.append("📧 لا تستخدم بريدك الحقيقي أبداً")
            recommendations.append("🛡️ استخدم محرك بحث خاص مثل DuckDuckGo")
        
        # توصيات إضافية حسب المحتوى المكتشف
        if any("sell" in str(n).lower() for n in negatives):
            recommendations.append("💰 هذا الموقع يبيع بياناتك - تجنبه تماماً")
        
        if any("third" in str(n).lower() for n in negatives):
            recommendations.append("👥 الموقع يشارك بياناتك مع أطراف ثالثة")
        
        if not any("right to erasure" in str(r).lower() or "delete" in str(r).lower() for r in user_rights):
            recommendations.append("🗑️ الموقع لا يسمح بحذف بياناتك بسهولة")
        
        if not any("opt-out" in str(p).lower() for p in positives):
            recommendations.append("🚫 لا يوجد خيار إلغاء الاشتراك (opt-out)")
        
        # إزالة التكرارات
        recommendations = list(dict.fromkeys(recommendations))
        
        return recommendations[:5]  # نرجع آخر 5 توصيات فقط
    
    def analyze(self, html_content: str) -> Dict:
        """الوظيفة الرئيسية لتحليل سياسة الخصوصية"""
        # استخراج النص
        text = self.extract_text_from_html(html_content)
        
        # حساب الدرجة
        score, positives, negatives = self.calculate_privacy_score(text)
        
        # فحص حقوق المستخدم
        user_rights = self.check_user_rights(text)
        
        # الحصول على التقييم
        grade_info = self.get_privacy_grade(score)
        
        # النتيجة النهائية
        result = {
            "score": score,
            "grade": grade_info["grade"],
            "color": grade_info["color"],
            "description": grade_info["description"],
            "icon": grade_info["icon"],
            "positives": positives[:5],  # آخر 5 إيجابيات
            "negatives": negatives[:5],  # آخر 5 سلبيات
            "user_rights": user_rights[:5],
            "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "recommendations": self.generate_recommendations(score, negatives, positives, user_rights),
            "analysis_details": {
                "text_length": len(text.split()),
                "bad_keywords_found": len(negatives),
                "good_keywords_found": len(positives),
                "rights_found": len(user_rights)
            }
        }
        
        return result


# 🌐 جزء Flask لإنشاء API (للاتصال من الإضافة)
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # للسماح للإضافة بالاتصال

analyzer = PrivacyPolicyAnalyzer()

@app.route('/analyze', methods=['POST'])
def analyze_privacy():
    """API لتحليل سياسة الخصوصية"""
    try:
        data = request.json
        url = data.get('url')
        
        if not url:
            return jsonify({"error": "URL is required"}), 400
        
        # محاولة جلب صفحة الخصوصية
        try:
            # جلب الصفحة الرئيسية أولاً (أو أي صفحة)
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            if response.status_code == 200:
                html_content = response.text
                result = analyzer.analyze(html_content)
                result["analyzed_url"] = url
                return jsonify(result)
            else:
                return jsonify({"error": f"Could not fetch website (status {response.status_code})"}), 404
                
        except requests.exceptions.Timeout:
            return jsonify({"error": "Website timeout - too slow to respond"}), 408
        except requests.exceptions.ConnectionError:
            return jsonify({"error": "Cannot connect to website - check URL"}), 404
        except Exception as e:
            return jsonify({"error": f"Network error: {str(e)}"}), 500
    
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@app.route('/analyze-text', methods=['POST'])
def analyze_text():
    """تحليل نص مباشر (بدون جلب من الإنترنت)"""
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "Text is required"}), 400
        
        result = analyzer.analyze(text)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/analyze-batch', methods=['POST'])
def analyze_batch():
    """تحليل عدة نصوص دفعة واحدة"""
    try:
        data = request.json
        texts = data.get('texts', [])
        
        if not texts:
            return jsonify({"error": "Texts array is required"}), 400
        
        results = []
        for text in texts:
            result = analyzer.analyze(text)
            results.append(result)
        
        return jsonify({
            "total": len(results),
            "results": results
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """فحص صحة السيرفر"""
    return jsonify({
        "status": "healthy", 
        "analyzer": "ready",
        "version": "2.0.0",
        "dynamic_scoring": True
    })


@app.route('/', methods=['GET'])
def home():
    """الصفحة الرئيسية"""
    return jsonify({
        "name": "Privacy Policy Analyzer API",
        "version": "2.0.0",
        "description": "Dynamic privacy policy analysis with intelligent scoring",
        "endpoints": {
            "POST /analyze": "Analyze website privacy policy",
            "POST /analyze-text": "Analyze raw text",
            "POST /analyze-batch": "Analyze multiple texts",
            "GET /health": "Health check"
        }
    })


# 🚀 تشغيل السيرفر
if __name__ == '__main__':
    print("=" * 50)
    print("🔍 Privacy Policy Analyzer Server v2.0")
    print("=" * 50)
    print("📡 Running on http://localhost:5000")
    print("📋 Available Endpoints:")
    print("   GET  /              - API Information")
    print("   GET  /health        - Health check")
    print("   POST /analyze       - Analyze website privacy policy")
    print("   POST /analyze-text  - Analyze raw text")
    print("   POST /analyze-batch - Analyze multiple texts")
    print("=" * 50)
    print("✅ Server is ready! (Dynamic Scoring Enabled)")
    print("🎯 Now each analysis gives different results based on content")
    print("=" * 50)
    app.run(debug=True, port=5000, host='localhost')