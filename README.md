<h1>Alfie - TruckersMP Info Discord Bot</h1>

<h2>Overview</h2>
<p>Alfie is a small yet modern companion for getting <a href="https://truckersmp.com/">TruckersMP</a> information straight to your Discord server.<br>This bot is free to add to your server or if you'd prefer, you can host your own instance.<br><b>Invite to your server:</b> <i><a href="https://discord.com/api/oauth2/authorize?client_id=937859809926074389&permissions=2147485696&scope=bot">Click here!</a></i></p>

<h2>Why Alfie?</h2>
<ul>
<li>Implements Discord's latest features (eg. slash commands, autocomplete)</li>
<li>Requires little permissions (no administrator in Discord)</li>
<li>Nice-looking and clear responses</li>
<li>Simple; just add to your server and it works</li>
<li>Cute name & open source</li>
</ul>

<h2>Features</h2>
<p><b>Dynamic Choices:</b> not quite sure on the server name?</p>
<img alt="Server options list" src="https://i.imgur.com/5sANTt9.png" />
<p><b>Smart Search:</b> not sure how to spell something?</p>
<img alt="Search for location" src="https://i.imgur.com/JhtUB6s.png" />
<p><b>Responses:</b> clean, detailed & modern</p>
<img alt="Servers embed response" src="https://i.imgur.com/iURdUZR.png" />
<img alt="Traffic embed response" src="https://i.imgur.com/v77IseH.png" />
<img alt="Server embed response" src="https://i.imgur.com/Cc53HVK.png" />

<h2>Deployment</h2>
<p>Using the official, hosted version of Alfie bot is the easiest, recommended and my preferred way for you to use the bot. Simply invite the bot to your server using the link in the overview.<br>However, if you still wish to deploy your own instance, please see the instructions below.</p>
 <ol>
  <li>Ensure you are running Python 3.10 or later.</li>
  <li>Set up a virtual environment using venv and install the dependencies.<br>To setup venv: <code>py -m venv venv</code> (See <a href="https://docs.python.org/3/library/venv.html">docs</a> for more)<br>Install dependencies: <code>pip install -U -r requirements.txt</code></li>
  <li>Rename <code>config.py.example</code> to <code>config.py</code> and modify where applicable.</li>
  <li>Rename <code>.env.example</code> to <code>.env</code> and modify where applicable.<br>Get token from the <a href="https://discord.com/developers/applications">Discord Developer Portal</a>.<br>Get a Steam API key <a href="https://steamcommunity.com/dev/apikey">here</a>.<br>Run <code>persistence-generate-key</code> to get persistence key.</li>
  <li>Run the bot using <code>py main.py</code>.</li>
</ol> 

<h2>License</h2>
<p>Released under the <a href="https://www.gnu.org/licenses/gpl-3.0.en.html">GNU GPL v3</a> license.</p>
<p>This project makes use of the following packages, which are distributed under the GPL-3.0 and MIT Licenses:</p>
<ul>
<li><a href="https://github.com/interactions-py/library">interactions.py</a> & <a href="https://github.com/interactions-py/persistence">interactions-persistence</a></li>
<li><a href="https://github.com/mjpieters/aiolimiter">aiolimiter</a></li>
<li><a href="https://github.com/SamNuttall/Async-TruckersMP">Async-TruckersMP</a></li>
</ul>

<h2>Credits</h2>
<p>Alfie relies on the following APIs: </p>
<ul>
<li><a href="https://stats.truckersmp.com/api">TruckersMP</a></li>
<li><a href="https://api.truckyapp.com/">TruckyApp</a></li>
</ul>
