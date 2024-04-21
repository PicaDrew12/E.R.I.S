def network():
    from flask import Flask, render_template,  request, session, jsonify
    import requests
    
    print("STARTER")
    app = Flask(__name__)

    # Set secret key before defining routes
    app.secret_key = 'heleeep'

    @app.route('/endpoint', methods=['POST'])
    def endpoint():
        data = request.get_json()
        received_text = data.get('text', 'No text received')
        print("Received text:", received_text)
        
        return {'message': 'Text received'}

    @app.route('/')
    def input():
        return render_template('input.html')
    
    @app.route('/volume', methods=['POST'])
    def volume():
        print("RECIVED")
        volume_recived = request.get_json()
        received_text = volume_recived.get('text', 'No text received')
        new_volume = int(received_text)
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        mapped_volume = -65 * math.exp(-new_volume * 0.045)
        
        volume.SetMasterVolumeLevel(mapped_volume, None)
        return "VOLUME CHANGED"
    
    @app.route('/system', methods=['POST'])
    def system_info():
        #uptime
        boot_time = psutil.boot_time()
        current_time = datetime.datetime.now().timestamp()
        uptime_seconds = current_time - boot_time
        uptime = datetime.timedelta(seconds=uptime_seconds)
        
        total_seconds = int(uptime.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        formatted_uptime = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        #battery
        battery = psutil.sensors_battery()
        battery_percentage = battery.percent

        charging = battery.power_plugged

        response = {
            'battery_percentage': battery_percentage,
            'charging': charging,
            'uptime': formatted_uptime
        }
        return jsonify(response)
    
    @app.route('/play-music', methods=['POST'])
    def play():
        data = request.get_json()
        received_text = data.get('text', 'No text received')
        print("Received text:", received_text)
        play_yt_from_app(received_text)
        return {'message': 'Text received'}
    

    if __name__ == '__main__':
        app.run(debug=True, use_reloader=False, port=2000)
