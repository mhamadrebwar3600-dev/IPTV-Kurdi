import os import requests from flask import Flask, redirect, jsonify, request
app = Flask(name)
لێرەدا لینکی ڕاستەقینەی Raw ی فایلی playlist.m3u لە گیتهاب دادەنێین
بۆ نموونە لینکەکەی خۆت لێرە دابنە
M3U_URL = "https://raw.githubusercontent.com/mhamadrebwar3600-dev/IPTV-Kurdi/refs/heads/main/playlist.m3u"
def get_channels(): channels = [] try: response = requests.get(M3U_URL) if response.status_code == 200: lines = response.text.splitlines() current_channel = {} for line in lines: line = line.strip() if line.startswith('#EXTINF:'): name = line.split(',')[-1] current_channel = {'name': name, 'logo': ''} elif line and not line.startswith('#'): current_channel['url'] = line channels.append(current_channel) current_channel = {} except Exception as e: print(f"Error fetching playlist: {e}") return channels
@app.route('/player_api.php') def player_api(): username = request.args.get('username') password = request.args.get('password')
if username == 'oneplus' and password == 'onekids':
    user_info = {
        "userInfo": {
            "username": "oneplus",
            "password": "onekids",
            "status": "Active",
            "is_trial": "0",
            "active_cons": "1"
        },
        "server_info": {
            "url": request.host.split(':')[0],
            "port": "80",
            "https_port": "443",
            "server_protocol": "https" if request.is_secure else "http"
        }
    }
    
    action = request.args.get('action')
    if action == 'get_live_categories':
        return jsonify([{"category_id": "1", "category_name": "My Channels"}])
        
    if action == 'get_live_streams':
        channels = get_channels()
        streams = []
        for idx, ch in enumerate(channels):
            streams.append({
                "num": idx + 1,
                "name": ch['name'],
                "stream_id": idx + 1,
                "stream_type": "live",
                "stream_icon": ch['logo'],
                "category_id": "1"
            })
        return jsonify(streams)
        
    return jsonify(user_info)
return jsonify({"user_info": {"auth": 0}})
@app.route('/live/<username>/<password>/int:stream_id.ts') def get_stream(username, password, stream_id): if username == 'oneplus' and password == 'onekids': channels = get_channels() if 0 < stream_id <= len(channels): target_url = channels[stream_id - 1]['url'] return redirect(target_url) return "Unauthorized", 401
if name == 'main': port = int(os.environ.get('PORT', 5000)) app.run(host='0.0.0.0', port=port)
