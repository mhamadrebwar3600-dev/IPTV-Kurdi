import re from flask import Flask, redirect, jsonify, request
app = Flask(name)
def parse_m3u(file_path): channels = [] current_channel = {} with open(file_path, 'r', encoding='utf-8', errors='ignore') as f: for line in f: line = line.strip() if line.startswith('#EXTINF:'): logo_match = re.search(r'tvg-logo="([^"]*)"', line) name = line.split(',')[-1] current_channel = { 'name': name, 'logo': logo_match.group(1) if logo_match else '', } elif line and not line.startswith('#'): current_channel['url'] = line channels.append(current_channel) current_channel = {} return channels
CHANNELS = parse_m3u('playlist.m3u')
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
        streams = []
        for idx, ch in enumerate(CHANNELS):
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
@app.route('/live/<username>/<password>/int:stream_id.ts') def get_stream(username, password, stream_id): if username == 'oneplus' and password == 'onekids': if 0 < stream_id <= len(CHANNELS): target_url = CHANNELS[stream_id - 1]['url'] return redirect(target_url) return "Unauthorized", 401
if name == 'main': app.run(host='0.0.0.0', port=5000)
