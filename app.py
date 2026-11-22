from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-video', methods=['POST'])
def get_video():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'দয়া করে একটি সঠিক ফেসবুক ভিডিও লিংক দিন।'}), 400

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            title = info.get('title', 'Facebook Video')
            return jsonify({'video_url': video_url, 'title': title})
    except Exception as e:
        return jsonify({'error': 'ভিডিওটি পাওয়া যায়নি। লিংকটি পাবলিক কি না তা যাচাই করুন।'}), 400

if __name__ == '__main__':
    app.run(debug=True)
