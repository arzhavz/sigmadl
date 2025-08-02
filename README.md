<h1>📥 Sigma Downloader</h1>

<p><strong>Sigma Downloader</strong> is a simple terminal tool for effortlessly downloading content from <strong>YouTube</strong> and <strong>Instagram</strong> (Reels & Photos). Designed with rich visual logging and clipboard auto-detection, it's perfect for power users who want to download quickly, cleanly, and efficiently.</p>

<hr>

<h2>🚀 Features</h2>
<ul>
  <li><strong>📋 Clipboard Auto-Detection:</strong> Automatically picks up YouTube or Instagram URLs from your clipboard.</li>
  <li><strong>📹 YouTube Video & Audio:</strong> Downloads 1080p video and 320kbps MP3 audio using <code>yt-dlp</code>.</li>
  <li><strong>📸 Instagram Support:</strong> Supports both Reels (video) and Photo posts, just paste the URL.</li>
  <li><strong>🧠 Smart URL Detection:</strong> Automatically detects if a URL is from YouTube, Instagram Reel, or Instagram Photo.</li>
  <li><strong>🧰 Terminal UI:</strong> Stylish terminal interface powered by <code>rich</code>, with logs, tables, and progress bars.</li>
  <li><strong>🧾 Real-time Logging:</strong> Errors and download progress are shown in terminal layout.</li>
  <li><strong>📂 Organized Output:</strong> Files are saved in timestamped or title-based folders for better organization.</li>
</ul>

<hr>

<h2>🪟 One-Click Convenience!</h2>

<p>If you're using Windows, you don't need to install Python or set up dependencies manually. Just <strong><a href="/releases/tag/1.0.2.8">download the precompiled file</a></strong> from the latest release, it's a standalone executable!</p>

<p>Once downloaded, make sure <code>ffmpeg</code> is available in your system PATH. Then simply copy a YouTube or Instagram URL, run the Sigma Downloader.exe, and you're done. No setup. No fuss. Just a few clicks and your media is ready.</p>

<p><em>Simplicity at its finest. Plug, play, and download.</em></p>

<hr>

<h2>⚙️ Requirements</h2>
<ul>
  <li>Python 3.8 or later</li>
  <li><code>ffmpeg</code> (must be installed and accessible via PATH)</li>
  <li>Google Chrome (for Instagram media scraping via Selenium)</li>
</ul>

<h4>Install dependencies:</h4>
<pre><code>pip install -r requirements.txt</code></pre>

<h4>Ensure ffmpeg is installed:</h4>
<p>Mac</p>
<pre><code>brew install ffmpeg</code></pre>

<p>Ubuntu</p>
<pre><code>sudo apt install ffmpeg</code></pre>

<p>Windows</p>
<a href="https://ffmpeg.org/download.html">https://ffmpeg.org/download.html</a>

<hr>

<h2>💡 How to Use</h2>

<ol>
  <li>Copy a supported URL (YouTube or Instagram Reel/Photo).</li>
  <li>Run the script:
    <pre><code>python main.py</code></pre>
  </li>
  <li>If clipboard detection fails, you will be prompted to enter the URL manually.</li>
  <li>The app:
    <ul>
      <li>Detects the URL type</li>
      <li>Starts the download process</li>
      <li>Shows real-time progress and log messages</li>
    </ul>
  </li>
</ol>

<hr>

<h2>🌐 Supported Platforms</h2>
<ul>
  <li><strong>YouTube:</strong> Videos + Audio (up to 1080p MP4 + MP3)</li>
  <li><strong>Instagram Reels:</strong> Video files</li>
  <li><strong>Instagram Photos:</strong> Single or multiple images in one post</li>
</ul>

<hr>

<h2>🛠 Under the Hood</h2>
<ul>
  <li>Uses <code>yt-dlp</code> for high-quality YouTube downloads</li>
  <li>Scrapes Instagram via headless Selenium browser</li>
  <li>Terminal interface built using <code>rich</code> with panels, tables, and live logging</li>
  <li>Smart URL regex matching for accurate platform detection</li>
</ul>

<hr>

<h2>📄 License</h2>
<p><strong>The Unlicense</strong>. Free to use, modify, and distribute without restriction.</p>

<hr>

<h2>🤝 Contributions</h2>
<p>Have an idea or bug report? PRs and issues are always welcome!</p>

<hr>

<h3>🧠 Built for those who just want to <em>copy, run, and download</em>.</h3>
